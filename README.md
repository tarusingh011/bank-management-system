# 🏦 Bank Management System

A Python-based Bank Management System with a Streamlit web interface, designed to perform basic banking operations through a simple and user-friendly dashboard.

## 🚀 Features

- **Account Creation:** Register new customers with unique account numbers.
- **Secure Login:** Authenticate users using their account number and PIN.
- **Deposit Money:** Deposit funds into an account.
- **Withdraw Money:** Withdraw funds with balance validation.
- **Account Details:** View personal and account information.
- **Transaction History:** Track deposits and withdrawals.
- **Update Profile:** Update name, email, age and PIN.
- **Delete Account:** Delete an account after verifying credentials and checking the balance.
- **PIN Security:** Store PINs using PBKDF2-HMAC-SHA256 hashing with individual salts.
- **Data Persistence:** Store account records in a JSON file.

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- JSON
- Git and GitHub

## 📁 Project Structure

```text
BankManagement/
│
├── app.py              # Streamlit frontend
├── bank.py             # Backend business logic
├── test_backend.py     # Backend testing
├── requirements.txt    # Project dependencies
├── .gitignore          # Files excluded from Git
└── data.json           # Local account database (not committed)
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
```

### 2. Navigate to the project directory

```bash
cd BankManagement
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Run the application

```bash
python -m streamlit run app.py
```

The application will open in your web browser, usually at:

```text
http://localhost:8501
```

## 🧪 Backend Testing

Run the backend test script using:

```bash
python test_backend.py
```

## 🔐 Security and Limitations

- PINs are hashed instead of being stored as plain text.
- Account-sensitive operations verify user credentials.
- The application uses JSON for local data storage.
- This project is an educational banking simulation, not a production banking platform.
- JSON storage does not provide the transaction safety or concurrent access controls required for real banking systems.

## 👩‍💻 Author

**Taru Singh**

Computer Science Engineering Student

## 📌 Future Improvements

- Integration with PostgreSQL or MySQL.
- Money transfer between accounts.
- Enhanced authentication and session security.
- Transaction analytics and visual dashboards.
- Deployment to a cloud platform.
