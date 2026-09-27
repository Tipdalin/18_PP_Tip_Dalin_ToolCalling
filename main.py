from agent import run_agent

def main():
    print("================================")
    print("Welcome to Phone Shopping Agent ")
    print("================================")
    print("Type 'exit' or 'q' to quit.\n")

    role = input("Enter your role (customer/admin): ").strip().lower()
    print("Your role is : ",role)

    if role not in ["customer", "admin"]:
        print("Invalid role. Using customer.")
        role = "customer"

    while True:

        user_query = input("\nYou: ").strip()

        if user_query.lower() in ["exit", "q"]:
            print("Goodbye!")
            break

        if not user_query:
            print("Please enter a query.")
            continue

        answer = run_agent(
            user_query,
            role
        )

        print(f"\nAgent: {answer}")

if __name__ == "__main__":
    main()

