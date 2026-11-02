
import json
import re
import secrets
import hashlib
import hmac
import os

from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation


class Bank:

    DATABASE = Path(__file__).with_name("data.json")

    # ==================================================
    # 1. INITIALIZATION
    # ==================================================

    def __init__(self):
        self.data = self.load_data()

    # ==================================================
    # 2. DATA HANDLING
    # ==================================================

    def load_data(self):
        """Load account data from JSON."""

        if not self.DATABASE.exists():
            return []

        try:
            with open(self.DATABASE, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                raise ValueError("Invalid database format.")

            return data

        except (json.JSONDecodeError, OSError, ValueError) as error:
            raise RuntimeError(
                f"Unable to load database: {error}"
            ) from error

    def save_data(self):
        """Save data safely using a temporary file."""

        temp_file = self.DATABASE.with_suffix(".tmp")

        try:
            with open(temp_file, "w", encoding="utf-8") as file:
                json.dump(self.data, file, indent=4)

            os.replace(temp_file, self.DATABASE)

        except OSError as error:
            if temp_file.exists():
                temp_file.unlink(missing_ok=True)

            raise RuntimeError(
                f"Unable to save database: {error}"
            ) from error

    # ==================================================
    # 3. INPUT VALIDATION
    # ==================================================

    @staticmethod
    def valid_name(name):

        return (
            isinstance(name, str)
            and bool(name.strip())
        )

    @staticmethod
    def valid_email(email):

        if not isinstance(email, str):
            return False

        pattern = r"^[\w.+-]+@[\w-]+\.[\w.-]+$"

        return bool(re.fullmatch(pattern, email.strip()))

    @staticmethod
    def valid_pin(pin):

        return (
            isinstance(pin, str)
            and bool(re.fullmatch(r"\d{4}", pin))
        )

    @staticmethod
    def valid_age(age):

        return (
            isinstance(age, int)
            and not isinstance(age, bool)
            and 18 <= age <= 120
        )

    @staticmethod
    def parse_amount(amount):
        """Validate and convert amount into Decimal."""

        try:
            value = Decimal(str(amount))

        except (InvalidOperation, ValueError, TypeError):
            raise ValueError("Please enter a valid amount.")

        if not value.is_finite():
            raise ValueError("Amount must be a finite number.")

        if value <= 0:
            raise ValueError("Amount must be greater than zero.")

        if value.as_tuple().exponent < -2:
            raise ValueError(
                "Maximum two decimal places are allowed."
            )

        return value.quantize(Decimal("0.01"))

    # ==================================================
    # 4. PIN SECURITY
    # ==================================================

    @staticmethod
    def hash_pin(pin, salt=None):
        """Hash PIN using PBKDF2-HMAC-SHA256."""

        if salt is None:
            salt = secrets.token_hex(16)

        hashed_pin = hashlib.pbkdf2_hmac(
            "sha256",
            pin.encode("utf-8"),
            bytes.fromhex(salt),
            200_000
        ).hex()

        return salt, hashed_pin

    @classmethod
    def verify_pin(cls, entered_pin, account):
        """Verify entered PIN against stored hash."""

        salt, entered_hash = cls.hash_pin(
            entered_pin,
            account["pin_salt"]
        )

        return hmac.compare_digest(
            entered_hash,
            account["pin_hash"]
        )

    # ==================================================
    # 5. ACCOUNT NUMBER GENERATION
    # ==================================================

    def generate_account_no(self):
        """Generate a unique 12-digit account number."""

        existing_numbers = {
            account["account_no"]
            for account in self.data
        }

        while True:

            account_no = "".join(
                secrets.choice("0123456789")
                for _ in range(12)
            )

            if account_no not in existing_numbers:
                return account_no

    # ==================================================
    # 6. FIND ACCOUNT
    # ==================================================

    def find_account(self, account_no):
        """Find account using account number."""

        return next(
            (
                account for account in self.data
                if account["account_no"] == str(account_no)
            ),
            None
        )

    # ==================================================
    # 7. AUTHENTICATION
    # ==================================================

    def authenticate(self, account_no, pin):
        """Authenticate using account number and PIN."""

        if not self.valid_pin(pin):
            return None

        account = self.find_account(account_no)

        if account and self.verify_pin(pin, account):
            return account

        return None

    def verify_account_access(self, account_no, pin):
        """Common account verification method."""

        return self.authenticate(account_no, pin)

    # ==================================================
    # 8. TRANSACTION HISTORY
    # ==================================================

    @staticmethod
    def add_transaction(account, transaction_type, amount, balance):
        """Add transaction record."""

        transaction = {
            "transaction_id": secrets.token_hex(6).upper(),
            "type": transaction_type,
            "amount": str(amount),
            "balance_after": str(balance),
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat()
        }

        account.setdefault("transactions", []).append(
            transaction
        )

    # ==================================================
    # 9. CREATE ACCOUNT
    # ==================================================

    def create_account(self, name, age, email, pin):

        name = name.strip() if isinstance(name, str) else ""
        email = email.strip().lower() if isinstance(email, str) else ""

        if not self.valid_name(name):
            return False, "Please enter a valid name."

        if not self.valid_age(age):
            return False, "Age must be between 18 and 120."

        if not self.valid_email(email):
            return False, "Please enter a valid email."

        if not self.valid_pin(pin):
            return False, "PIN must contain exactly four digits."

        if any(
            account["email"].lower() == email
            for account in self.data
        ):
            return False, "Email is already registered."

        salt, hashed_pin = self.hash_pin(pin)

        account = {
            "name": name,
            "age": age,
            "email": email,
            "account_no": self.generate_account_no(),
            "pin_salt": salt,
            "pin_hash": hashed_pin,
            "balance": "0.00",
            "created_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "transactions": []
        }

        self.data.append(account)

        try:
            self.save_data()

        except RuntimeError:
            self.data.remove(account)
            raise

        return True, {
            "message": "Account created successfully!",
            "account_no": account["account_no"],
            "name": account["name"]
        }

    # ==================================================
    # 10. DEPOSIT MONEY
    # ==================================================

    def deposit(self, account_no, pin, amount):

        account = self.verify_account_access(
            account_no, pin
        )

        if not account:
            return False, "Invalid account number or PIN."

        try:
            amount = self.parse_amount(amount)

        except ValueError as error:
            return False, str(error)

        if amount > Decimal("100000"):
            return False, "Maximum deposit limit is ₹1,00,000."

        old_balance = Decimal(account["balance"])
        new_balance = old_balance + amount

        account["balance"] = str(new_balance)

        self.add_transaction(
            account,
            "DEPOSIT",
            amount,
            new_balance
        )

        try:
            self.save_data()

        except RuntimeError:
            account["balance"] = str(old_balance)
            account["transactions"].pop()
            raise

        return True, {
            "message": "Amount deposited successfully!",
            "deposited": str(amount),
            "balance": str(new_balance)
        }

    # ==================================================
    # 11. WITHDRAW MONEY
    # ==================================================

    def withdraw(self, account_no, pin, amount):

        account = self.verify_account_access(
            account_no, pin
        )

        if not account:
            return False, "Invalid account number or PIN."

        try:
            amount = self.parse_amount(amount)

        except ValueError as error:
            return False, str(error)

        if amount > Decimal("50000"):
            return False, "Maximum withdrawal limit is ₹50,000."

        old_balance = Decimal(account["balance"])

        if amount > old_balance:
            return False, "Insufficient account balance."

        new_balance = old_balance - amount

        account["balance"] = str(new_balance)

        self.add_transaction(
            account,
            "WITHDRAWAL",
            amount,
            new_balance
        )

        try:
            self.save_data()

        except RuntimeError:
            account["balance"] = str(old_balance)
            account["transactions"].pop()
            raise

        return True, {
            "message": "Amount withdrawn successfully!",
            "withdrawn": str(amount),
            "balance": str(new_balance)
        }

    # ==================================================
    # 12. ACCOUNT DETAILS
    # ==================================================

    def get_account_details(self, account_no, pin):

        account = self.verify_account_access(
            account_no, pin
        )

        if not account:
            return None

        return {
            "name": account["name"],
            "age": account["age"],
            "email": account["email"],
            "account_no": account["account_no"],
            "balance": account["balance"],
            "created_at": account["created_at"]
        }

    # ==================================================
    # 13. TRANSACTION HISTORY
    # ==================================================

    def get_transaction_history(self, account_no, pin):

        account = self.verify_account_access(
            account_no, pin
        )

        if not account:
            return None

        return list(
            reversed(account.get("transactions", []))
        )

    # ==================================================
    # 14. UPDATE PROFILE
    # ==================================================

    def update_profile(
        self,
        account_no,
        pin,
        name=None,
        email=None,
        age=None,
        new_pin=None
    ):

        account = self.verify_account_access(
            account_no, pin
        )

        if not account:
            return False, "Invalid account number or PIN."

        updated_fields = {}

        if name is not None:

            name = name.strip()

            if not self.valid_name(name):
                return False, "Please enter a valid name."

            updated_fields["name"] = name

        if email is not None:

            email = email.strip().lower()

            if not self.valid_email(email):
                return False, "Please enter a valid email."

            duplicate = any(
                other["email"].lower() == email
                and other["account_no"] != account_no
                for other in self.data
            )

            if duplicate:
                return False, "Email is already registered."

            updated_fields["email"] = email

        if age is not None:

            if not self.valid_age(age):
                return False, "Age must be between 18 and 120."

            updated_fields["age"] = age

        if new_pin is not None:

            if not self.valid_pin(new_pin):
                return False, "New PIN must contain exactly four digits."

            salt, hashed_pin = self.hash_pin(new_pin)

            updated_fields["pin_salt"] = salt
            updated_fields["pin_hash"] = hashed_pin

        if not updated_fields:
            return False, "No changes were provided."

        old_values = {
            key: account[key]
            for key in updated_fields
        }

        account.update(updated_fields)

        try:
            self.save_data()

        except RuntimeError:
            account.update(old_values)
            raise

        return True, "Account details updated successfully!"

    # ==================================================
    # 15. DELETE ACCOUNT
    # ==================================================

    def delete_account(self, account_no, pin):

        account = self.verify_account_access(
            account_no, pin
        )

        if not account:
            return False, "Invalid account number or PIN."

        if Decimal(account["balance"]) != Decimal("0.00"):
            return False, (
                "Please withdraw your remaining balance "
                "before deleting your account."
            )

        self.data.remove(account)

        try:
            self.save_data()

        except RuntimeError:
            self.data.append(account)
            raise

        return True, "Account deleted successfully!"
