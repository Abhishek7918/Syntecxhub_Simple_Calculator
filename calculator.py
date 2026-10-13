def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error: Division by zero is not allowed."
    return a / b

def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input! Please enter a valid number.")

def main():
    while True:
        print("\n=== Simple CLI Calculator ===")
        print("1. Addition (+)")
        print("2. Subtraction (-)")
        print("3. Multiplication (*)")
        print("4. Division (/)")
        print("5. Exit")

        choice = input("Select an option (1-5): ").strip()

        if choice == "5":
            print("Exiting calculator. Goodbye!")
            break

        if choice not in ["1", "2", "3", "4"]:
            print("Invalid choice! Please select between 1 and 5.")
            continue

        num1 = get_number("Enter first number: ")
        num2 = get_number("Enter second number: ")

        if choice == "1":
            print(f"Result: {num1} + {num2} = {add(num1, num2)}")
        elif choice == "2":
            print(f"Result: {num1} - {num2} = {subtract(num1, num2)}")
        elif choice == "3":
            print(f"Result: {num1} * {num2} = {multiply(num1, num2)}")
        elif choice == "4":
            result = divide(num1, num2)
            print(f"Result: {result}")

if __name__ == "__main__":
    main()