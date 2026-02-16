# **Python Calculator - User Guide**

## **📌 Quick Start**
1. Save the code in a file named `calculator.py`
2. Open terminal/command prompt
3. Run: `python calculator.py`

## **📋 How to Use**

### **Main Menu Options:**
```
1. Addition (+)       → Adds two numbers
2. Subtraction (-)    → Subtracts second number from first
3. Multiplication (*) → Multiplies two numbers
4. Division (/)      → Divides first number by second
5. Exit              → Closes the calculator
```

### **Step-by-Step Instructions:**
1. **Run the program**
2. **Type a number 1-5** to choose an operation
3. **Enter first number** (can be decimal or negative)
4. **Enter second number**
5. **See the result** in format: `number1 operator number2 = result`
6. **Repeat** or press `5` to exit

## **✅ Example Session**
```
=== Python Calculator ===

Select operation:
1. Addition (+)
2. Subtraction (-)
3. Multiplication (*)
4. Division (/)
5. Exit
Enter choice (1-5): 1
Enter first number: 10
Enter second number: 5
10 + 5 = 15
```

## **⚠️ Error Messages & Solutions**

| Error Message | Cause | Solution |
|--------------|-------|----------|
| `"Invalid choice"` | Entered number not 1-5 | Type only 1, 2, 3, 4, or 5 |
| `"Error: Please enter valid numbers"` | Entered text instead of numbers | Enter numeric values (e.g., 5, 3.14, -2) |
| `"Error: Cannot divide by zero"` | Tried to divide by 0 | Use any number except 0 as second number |

## **🔧 Features**
- ✅ Addition, Subtraction, Multiplication, Division
- ✅ Handles decimal numbers
- ✅ Handles negative numbers
- ✅ Error prevention for division by zero
- ✅ Continuous operation until you exit
- ✅ Clear, formatted output
