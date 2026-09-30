while True:
    print("\n--- Simple Calculator Menu ---")
    print("1. Add (+)")
    print("2. Subtract (-)")
    print("3. Multiply (*)")
    print("4. Divide (/)")
    print("5. Power (**) - Challenge")
    print("6. Exit")
    
    choice = input("Choose an operation (1-6): ")
    
    if choice == '6':
        print("Exiting calculator. Goodbye!")
        break
        
    if choice in ('1', '2', '3', '4', '5'):
        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
        except ValueError:
            print("Error: Please enter valid numbers.")
            continue
            
        if choice == '1':
            result = num1 + num2
            print(f"Result: {num1} + {num2} = {result}")
        elif choice == '2':
            result = num1 - num2
            print(f"Result: {num1} - {num2} = {result}")
        elif choice == '3':
            result = num1 * num2
            print(f"Result: {num1} * {num2} = {result}")
        elif choice == '4':
            if num2 == 0:
                print("Error: Division by zero")
            else:
                result = num1 / num2
                print(f"Result: {num1} / {num2} = {result}")
        elif choice == '5':
            exp_input = input("Enter exponent (press Enter to use default = 2): ")
            if exp_input.strip() == "":
                exponent = 2
            else:
                exponent = float(exp_input)
            result = num1 ** exponent
            print(f"Result: {num1} ** {exponent} = {result}")
    else:
        print("Invalid choice. Please choose between 1 and 6.")