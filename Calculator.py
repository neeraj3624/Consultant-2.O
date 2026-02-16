def menu_calculator():
    print("=== Python Calculator ===")
    
    while True:
        print("\nSelect operation:")
        print("1. Addition (+)")
        print("2. Subtraction (-)")
        print("3. Multiplication (*)")
        print("4. Division (/)")
        print("5. Exit")
        
        choice = input("Enter choice (1-5): ")
        
        if choice == '5':
            print("Goodbye!")
            break
        
        if choice not in ['1', '2', '3', '4']:
            print("Invalid choice")
            continue
        
        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            
            if choice == '1':
                result = num1 + num2
                operator = "+"
            elif choice == '2':
                result = num1 - num2
                operator = "-"
            elif choice == '3':
                result = num1 * num2
                operator = "*"
            elif choice == '4':
                if num2 == 0:
                    print("Error: Cannot divide by zero")
                    continue
                result = num1 / num2
                operator = "/"
            
            print(f"{num1} {operator} {num2} = {result}")
            
        except ValueError:
            print("Error: Please enter valid numbers")
        except Exception as e:
            print(f"Error: {e}")

# Run the calculator
if __name__ == "__main__":
    menu_calculator() 