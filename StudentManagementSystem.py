"""Student Management System"""
import json
from datetime import datetime
from tabulate import tabulate
import uuid
import os 
import csv

class Student:
    def __init__(self, student_id, name, age, grade, department, email, phone):
        """Initializes a student object 
        
        Args:
            student_id: unique student id 
            name: student's full name
            age: student's age
            grade: student's grade/score
            department: student's department
            email: student's email id
            phone: contact number
        """
        
        self.student_id = student_id
        self.name = name
        self.age = age
        self.grade = grade
        self.department = department
        self.email = email
        self.phone = phone
        self.enrollment_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def to_dict(self):
        '''Convert student object to dictionary'''
        return {
            'student_id': self.student_id,
            'name': self.name,
            'age': self.age,
            'grade': self.grade,
            'department': self.department,
            'email': self.email,
            'phone': self.phone,
            'enrollment_date': self.enrollment_date
        }
        
    def display_info(self):
        '''Display student information in formatted way '''
        print('\n' + "=" * 50)
        print(f"STUDENT ID: {self.student_id}")
        print(f"NAME: {self.name}")
        print(f"AGE: {self.age}")
        print(f"GRADE: {self.grade}")
        print(f"DEPARTMENT: {self.department}")
        print(f"EMAIL: {self.email}")
        print(f"PHONE: {self.phone}")
        print(f"ENROLLMENT DATE: {self.enrollment_date}")
        print("=" * 50) 


class StudentManagementSystem:
    '''Main class for managing student records'''
    
    def __init__(self, data_file='students_data.json'):
        '''Initialize the management system'''
        self.data_file = data_file
        self.students = {}
        self.load_students()
        
    def generate_student_id(self):
        '''Generate unique student ID'''
        return "STU" + str(uuid.uuid4().hex[:6].upper())
    
    def load_students(self):
        '''Load student data from JSON file'''
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as file:
                    data = json.load(file)
                    for student_id, student_data in data.items():
                        if 'department' not in student_data:
                            student_data['department'] = student_data.get('deparment', 'Unknown')
                        student = Student(**student_data)
                        self.students[student.student_id] = student
                print(f"Loaded {len(self.students)} students from database")
            else:
                print('No existing database found. Starting fresh...')
        except Exception as e:
            print(f"Error loading data: {e}")
            self.students = {}

    def save_students(self):
        '''Save student data to JSON file'''
        try:
            data = {}
            for sid, student in self.students.items():
                data[sid] = student.to_dict()
            with open(self.data_file, 'w') as file:
                json.dump(data, file, indent=4)
            print('Data saved successfully')
        except Exception as e:
            print(f"Error saving data: {e}")
            
    def add_student(self):
        '''Add a new student to the system'''
        print("\n" + "=" * 50)
        print("ADD NEW STUDENT")
        print("=" * 50)
        
        try:
            name = input("Enter student name: ").strip()
            if not name:
                print('Name cannot be empty')
                return 
                
            age = int(input('Enter age: '))
            if age < 15 or age > 60:
                print('Age must be between 15 and 60!') 
                return

            grade = input('Enter grade (A/B/C/D/F): ').upper().strip()
            if grade not in ['A', 'B', 'C', 'D', 'F']:
                print('Invalid grade! Use A, B, C, D or F')
                return

            department = input('Enter department: ').strip()
            email = input('Enter email: ').strip()
            phone = input('Enter phone number: ').strip()
            
            student_id = self.generate_student_id()
            student = Student(student_id, name, age, grade, department, email, phone)
            self.students[student_id] = student
            self.save_students()
            
            print(f"\nStudent added successfully!")
            print(f"Student ID: {student_id}")
            
        except ValueError:
            print("Invalid input! Please enter correct data types.")
        except Exception as e:
            print(f"Error: {e}")
            
    def view_all_students(self):
        '''Display all students in a table format '''
        if not self.students:
            print('No students found in the database')
            return 
        
        print("\n" + "=" * 80)
        print('ALL STUDENTS')
        print('=' * 80)
        
        table_data = []
        for student in self.students.values():
            table_data.append([
                student.student_id,
                student.name,
                student.age,
                student.grade,
                student.department,
                student.email,
                student.phone
            ])
            
        headers = ['ID', 'Name', 'Age', 'Grade', 'Department', 'Email', 'Phone']
        print(tabulate(table_data, headers=headers, tablefmt='grid'))
        print(f"\nTotal Students: {len(self.students)}")
    
    def search_student(self):
        '''Search for a student by ID, name, or department'''
        print("\n" + "=" * 50)
        print("SEARCH STUDENT")
        print("=" * 50)
        
        print("1. Search by Student ID")
        print("2. Search by Name")
        print("3. Search by Department")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        results = []
        
        if choice == '1':
            student_id = input("Enter Student ID: ").strip().upper()
            if student_id in self.students:
                results.append(self.students[student_id])
            else:
                print(f"Student with ID {student_id} not found!")
                
        elif choice == '2':
            name = input("Enter student name: ").strip().lower()
            for student in self.students.values():
                if name in student.name.lower():
                    results.append(student)
            if not results:
                print(f"No student found with name containing '{name}'")
                
        elif choice == '3':
            department = input("Enter department: ").strip().lower()
            for student in self.students.values():
                if department in student.department.lower():
                    results.append(student)
            if not results:
                print(f"No student found in department '{department}'")
        else:
            print("Invalid choice!")
            return
        
        if results:
            print(f"\nFound {len(results)} student(s):")
            for student in results:
                student.display_info()
    
    def update_student(self):
        '''Update student information'''
        print("\n" + "=" * 50)
        print("UPDATE STUDENT INFORMATION")
        print("=" * 50)
        
        student_id = input("Enter Student ID to update: ").strip().upper()
        
        if student_id not in self.students:
            print(f"Student with ID {student_id} not found!")
            return
        
        student = self.students[student_id]
        student.display_info()
        
        print("\nWhat would you like to update?")
        print("1. Name")
        print("2. Age")
        print("3. Grade")
        print("4. Department")
        print("5. Email")
        print("6. Phone")
        print("7. Cancel")
        
        choice = input("\nEnter choice (1-7): ").strip()
        
        try:
            if choice == '1':
                new_name = input("Enter new name: ").strip()
                if new_name:
                    student.name = new_name
                    print("Name updated successfully!")
            elif choice == '2':
                new_age = int(input("Enter new age: "))
                if 15 <= new_age <= 60:
                    student.age = new_age
                    print("Age updated successfully!")
                else:
                    print("Age must be between 15 and 60!")
                    return
            elif choice == '3':
                new_grade = input("Enter new grade (A/B/C/D/F): ").upper().strip()
                if new_grade in ['A', 'B', 'C', 'D', 'F']:
                    student.grade = new_grade
                    print("Grade updated successfully!")
                else:
                    print("Invalid grade!")
                    return
            elif choice == '4':
                student.department = input("Enter new department: ").strip()
                print("Department updated successfully!")
            elif choice == '5':
                student.email = input("Enter new email: ").strip()
                print("Email updated successfully!")
            elif choice == '6':
                student.phone = input("Enter new phone: ").strip()
                print("Phone updated successfully!")
            elif choice == '7':
                print("Update cancelled.")
                return
            else:
                print("Invalid choice!")
                return
            
            self.save_students()
            print("\nStudent information updated successfully!")
            student.display_info()
            
        except ValueError:
            print("Invalid input!")
        except Exception as e:
            print(f"Error: {e}")
    
    def delete_student(self):
        '''Delete a student from the system'''
        print("\n" + "=" * 50)
        print("DELETE STUDENT")
        print("=" * 50)
        
        student_id = input("Enter Student ID to delete: ").strip().upper()
        
        if student_id not in self.students:
            print(f"Student with ID {student_id} not found!")
            return
        
        student = self.students[student_id]
        student.display_info()
        
        confirm = input(f"\nAre you sure you want to delete {student.name}? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            del self.students[student_id]
            self.save_students()
            print(f"Student {student_id} deleted successfully!")
        else:
            print("Deletion cancelled.")
    
    def generate_report(self):
        '''Generate statistical report of students'''
        if not self.students:
            print('No students found in the database')
            return 
        
        print("\n" + "=" * 50)
        print("STATISTICAL REPORT")
        print("=" * 50)
        
        total_students = len(self.students)
        
        grade_count = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
        departments = {}
        total_age = 0
        
        for student in self.students.values():
            grade_count[student.grade] += 1
            total_age += student.age
            dept = student.department
            departments[dept] = departments.get(dept, 0) + 1
        
        avg_age = total_age / total_students if total_students > 0 else 0
        
        print(f"\nTOTAL STUDENTS: {total_students}")
        print(f"AVERAGE AGE: {avg_age:.1f} years")
        
        print("\nGRADE DISTRIBUTION:")
        for grade, count in grade_count.items():
            percentage = (count / total_students * 100) if total_students > 0 else 0
            print(f"   {grade}: {count} students ({percentage:.1f}%)")
        
        print("\nDEPARTMENT DISTRIBUTION:")
        for dept, count in sorted(departments.items()):
            percentage = (count / total_students * 100) if total_students > 0 else 0
            print(f"   {dept}: {count} students ({percentage:.1f}%)")
    
    def export_to_csv(self):
        '''Export student data to CSV file'''
        if not self.students:
            print('No students to export')
            return
        
        filename = f"students_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        try:
            with open(filename, 'w', newline='') as csvfile:
                fieldnames = ['student_id', 'name', 'age', 'grade', 'department', 
                            'email', 'phone', 'enrollment_date']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for student in self.students.values():
                    writer.writerow(student.to_dict())
            
            print(f"Data exported to {filename}")
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
    
    def display_menu(self):
        '''Display the main menu'''
        print("\n" + "=" * 60)
        print("STUDENT MANAGEMENT SYSTEM")
        print("=" * 60)
        print("1. Add New Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student Information")
        print("5. Delete Student")
        print("6. Generate Report")
        print("7. Export to CSV")
        print("8. Exit")
        print("=" * 60)


def main():
    '''Main function to run the Student Management System'''
    print("\n" + "=" * 60)
    print("WELCOME TO STUDENT MANAGEMENT SYSTEM")
    print("Final Year College Project")
    print("=" * 60)
    
    try:
        from tabulate import tabulate
    except ImportError:
        print("\n'tabulate' module not found.")
        install = input("Do you want to install it? (yes/no): ").strip().lower()
        if install == 'yes':
            import subprocess
            import sys
            subprocess.check_call([sys.executable, "-m", "pip", "install", "tabulate"])
            print("'tabulate' installed successfully!")
            from tabulate import tabulate
        else:
            print("'tabulate' is required for table display. Exiting...")
            return
    
    system = StudentManagementSystem()
    
    while True:
        system.display_menu()
        
        try:
            choice = input("\nEnter your choice (1-8): ").strip()
            
            if choice == '1':
                system.add_student()
            elif choice == '2':
                system.view_all_students()
            elif choice == '3':
                system.search_student()
            elif choice == '4':
                system.update_student()
            elif choice == '5':
                system.delete_student()
            elif choice == '6':
                system.generate_report()
            elif choice == '7':
                system.export_to_csv()
            elif choice == '8':
                print("\n" + "=" * 60)
                print("Thank you for using Student Management System!")
                print("Data saved automatically")
                print("=" * 60)
                break
            else:
                print("Invalid choice! Please enter a number between 1-8")
            
            input("\nPress Enter to continue...")
            
        except KeyboardInterrupt:
            print("\n\nProgram interrupted. Saving data...")
            system.save_students()
            print("Goodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()