from bank import Bank

bank = Bank()

# Create account
success, result = bank.create_account(
    "Taru Singh",
    20,
    "taru@example.com",
    "1234"
)

print(success, result)

if success:
    account_no = result["account_no"]

    # Deposit
    print(bank.deposit(account_no, "1234", 5000))

    # Withdraw
    print(bank.withdraw(account_no, "1234", 1000))

    # Account details
    print(bank.get_account_details(account_no, "1234"))

    # Transaction history
    print(bank.get_transaction_history(account_no, "1234"))

    # Update profile
    print(bank.update_profile(
        account_no,
        "1234",
        name="Taru S."
    ))