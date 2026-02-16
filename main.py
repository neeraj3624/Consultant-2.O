from fastapi import FastAPI, Depends, HTTPException, WebSocket, status, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import auth, models, schemas
from typing import List, Dict, Set
import asyncio
import json

import dependencies
from database import engine, Base, SessionLocal
from dependencies import get_db, get_current_user

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    from fastapi.responses import FileResponse
    return FileResponse("static/index.html")

@app.get("/tasks/", response_model=List[schemas.Task])
def get_tasks(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    tasks = db.query(models.Task).filter(models.Task.owner_id == current_user.id).all()
    return tasks

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, Set[WebSocket]] = {}
        
    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        self.active_connections[user_id].add(websocket)
        
    def disconnect(self, websocket: WebSocket, user_id: int):
        if user_id in self.active_connections:
            self.active_connections[user_id].discard(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
            
    async def send_personal_message(self, message: dict, user_id: int):
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except WebSocketDisconnect:
                    pass

manager = ConnectionManager()

@app.post('/register', response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post('/token', response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/tasks/", response_model=schemas.Task)
async def create_task(
    task: schemas.TaskCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_task = models.Task(**task.model_dump(), owner_id=current_user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    # Notify via WebSocket
    await manager.send_personal_message({
        "type": "task_created",
        "task": schemas.Task.model_validate(db_task).model_dump()
    }, current_user.id)

    return db_task

@app.get('/tasks/{task_id}', response_model=schemas.Task)
def read_task(task_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put('/tasks/{task_id}', response_model=schemas.Task)
async def update_task(task_id: int, task_update: schemas.TaskUpdate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    for var, value in vars(task_update).items():
        if value is not None:
            setattr(task, var, value)
    
    db.commit()
    db.refresh(task)

    # Notify via WebSocket
    await manager.send_personal_message({
        "type": "task_updated",
        "task": schemas.Task.model_validate(task).model_dump()
    }, current_user.id)

    return task

@app.delete('/tasks/{task_id}')
def delete_task(task_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"detail": "Task deleted successfully"}

@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket, token: str = None):
    '''WebSocket connection requires a valid JWT token as query parameter'''
    
    await websocket.accept()
    
    if not token:
        await websocket.send_json({"type": "error", "message": "Token required"})
        await websocket.close(code=1008)
        return
    
    db = SessionLocal()
    user = None
    try:
        token_data = auth.decode_token(token)
        if not token_data or not token_data.username:
            await websocket.send_json({"type": "error", "message": "Invalid token"})
            await websocket.close(code=1008)
            return
        user = db.query(models.User).filter(models.User.username == token_data.username).first()
        if not user:
            await websocket.send_json({"type": "error", "message": "User not found"})
            await websocket.close(code=1008)
            return
        
        await manager.connect(websocket, user.id)
        print(f"WebSocket connected for user: {user.username}")
        
        # Send initial tasks
        tasks = db.query(models.Task).filter(models.Task.owner_id == user.id).all()
        await websocket.send_json({
            "type": "initial_tasks", 
            "tasks": [schemas.Task.model_validate(task).model_dump() for task in tasks]
        })
        
        # Keep connection alive with ping
        while True:
            try:
                # Wait for message with timeout
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
                # Echo back or handle ping
                if data == "ping":
                    await websocket.send_text("pong")
            except asyncio.TimeoutError:
                # Send ping to keep connection alive
                await websocket.send_text("ping")
            except WebSocketDisconnect:
                print(f"WebSocket disconnected for user: {user.username}")
                break
            except Exception as e:
                print(f"WebSocket receive error: {e}")
                break
                
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.send_json({"type": "error", "message": f"WebSocket error: {str(e)}"})
    finally:
        if user:
            manager.disconnect(websocket, user.id)
        db.close()
# Force reload
# Force reload 2
