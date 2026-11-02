
import streamlit as st
from bank import Bank
import pandas as pd


# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="My Bank | Banking System",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# 2. INITIALIZATION
# =====================================================

if "bank" not in st.session_state:
    st.session_state.bank = Bank()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "account_no" not in st.session_state:
    st.session_state.account_no = None

bank = st.session_state.bank


# =====================================================
# 3. CUSTOM STYLING
# =====================================================


# =====================================================
# 3. CUSTOM STYLING
# =====================================================

st.markdown("""
<style>

/* Main application */
.stApp {
    background-color: #F4F7FB;
    color: #172B4D;
}

/* Main content area */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #142B4A;
}

/* Sidebar text */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: white !important;
}

/* Main headings */
h1, h2, h3 {
    color: #142B4A !important;
}

/* Normal text */
.stApp p,
.stApp label,
.stApp .stMarkdown {
    color: #334155;
}

/* Input fields */
.stTextInput input,
.stNumberInput input {
    background-color: white !important;
    color: #172B4D !important;
    border: 1px solid #CBD5E1 !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: white !important;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #E2E8F0;
}

/* Metric text */
[data-testid="stMetricLabel"],
[data-testid="stMetricValue"] {
    color: #142B4A !important;
}

/* Buttons */
.stButton button,
.stFormSubmitButton button {
    background-color: #2563EB !important;
    color: white !important;
    border: none !important;
    border-radius: 8px;
    font-weight: 600;
    min-height: 42px;
}

/* Button hover */
.stButton button:hover,
.stFormSubmitButton button:hover {
    background-color: #1D4ED8 !important;
}

/* Form containers */
[data-testid="stForm"] {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #E2E8F0;
}

/* Data tables */
[data-testid="stDataFrame"] {
    background-color: white;
    border-radius: 10px;
}

/* Dividers */
hr {
    border-color: #DCE3ED;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# 4. COMMON FUNCTIONS
# =====================================================

def logout():
    st.session_state.logged_in = False
    st.session_state.account_no = None
    st.rerun()


def show_title(title, subtitle=None):
    st.title(title)

    if subtitle:
        st.caption(subtitle)


def verify_pin():
    """Ask for PIN before performing sensitive operations."""

    return st.text_input(
        "Enter your 4-digit PIN",
        type="password",
        max_chars=4
    )


# =====================================================
# 5. SIDEBAR NAVIGATION
# =====================================================

st.sidebar.title("🏦 MY BANK")

st.sidebar.caption("Bank Management System")

st.sidebar.divider()

if st.session_state.logged_in:

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Deposit Money",
            "Withdraw Money",
            "Transaction History",
            "Update Profile",
            "Delete Account",
            "Logout"
        ]
    )

    st.sidebar.divider()

    st.sidebar.success("You are logged in.")

    st.sidebar.write(
        f"Account: {st.session_state.account_no}"
    )

else:

    page = st.sidebar.radio(
        "Navigation",
        [
            "Home",
            "Create Account",
            "Login"
        ]
    )

    st.sidebar.divider()

    st.sidebar.info("Please login to access banking services.")


# =====================================================
# 6. HOME PAGE
# =====================================================

if page == "Home":

    st.title("🏦 Welcome to My Bank")

    st.subheader("Simple. Secure. Digital Banking.")

    st.write(
        """
        Welcome to our Bank Management System.

        Manage your account, deposit money, withdraw funds,
        view transaction history and update your profile
        through a simple digital banking interface.
        """
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric("Account Services", "24/7")
    col2.metric("PIN Security", "Enabled")
    col3.metric("Transactions", "Tracked")

    st.divider()

    st.subheader("Our Services")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### 📝 Create Account")
        st.write("Open a new bank account.")

        st.markdown("### 💰 Deposit Money")
        st.write("Add money to your account.")

        st.markdown("### 📊 Transaction History")
        st.write("View your previous transactions.")

    with c2:
        st.markdown("### 🔐 Secure Login")
        st.write("Access your account securely.")

        st.markdown("### 💸 Withdraw Money")
        st.write("Withdraw money from your account.")

        st.markdown("### 👤 Manage Profile")
        st.write("Update your account information.")


# =====================================================
# 7. CREATE ACCOUNT
# =====================================================

elif page == "Create Account":

    show_title(
        "Create Your Bank Account",
        "Enter your details to register a new account."
    )

    with st.form("create_account_form"):

        name = st.text_input("Full Name")

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=20
        )

        email = st.text_input("Email Address")

        pin = st.text_input(
            "Create 4-digit PIN",
            type="password",
            max_chars=4
        )

        confirm_pin = st.text_input(
            "Confirm PIN",
            type="password",
            max_chars=4
        )

        submitted = st.form_submit_button(
            "Create Account",
            use_container_width=True
        )

        if submitted:

            if pin != confirm_pin:

                st.error("PINs do not match.")

            else:

                try:
                    success, result = bank.create_account(
                        name,
                        int(age),
                        email,
                        pin
                    )

                    if success:

                        st.success(result["message"])

                        st.subheader("Account Created Successfully!")

                        st.write("Name:", result["name"])

                        st.code(
                            result["account_no"],
                            language=None
                        )

                        st.warning(
                            "Save your account number safely. "
                            "You will need it to log in."
                        )

                    else:

                        st.error(result)

                except RuntimeError as error:

                    st.error(str(error))


# =====================================================
# 8. LOGIN
# =====================================================

elif page == "Login":

    show_title(
        "Customer Login",
        "Enter your account credentials."
    )

    with st.form("login_form"):

        account_no = st.text_input(
            "Account Number"
        )

        pin = st.text_input(
            "4-digit PIN",
            type="password",
            max_chars=4
        )

        submitted = st.form_submit_button(
            "Login",
            use_container_width=True
        )

        if submitted:

            account = bank.authenticate(
                account_no.strip(),
                pin
            )

            if account:

                st.session_state.logged_in = True

                st.session_state.account_no = account_no.strip()

                st.success("Login successful!")

                st.rerun()

            else:

                st.error(
                    "Invalid account number or PIN."
                )


# =====================================================
# 9. DASHBOARD / ACCOUNT DETAILS
# =====================================================

elif page == "Dashboard":

    show_title(
        "My Dashboard",
        "View your account information and balance."
    )

    account_no = st.session_state.account_no

    st.info(f"Logged in account: {account_no}")

    pin = verify_pin()

    if st.button(
        "View Account Details",
        use_container_width=True
    ):

        details = bank.get_account_details(
            account_no,
            pin
        )

        if details:

            st.success("Account details verified.")

            st.divider()

            col1, col2 = st.columns(2)

            col1.metric(
                "Account Balance",
                f"₹ {details['balance']}"
            )

            col2.metric(
                "Account Holder",
                details["name"]
            )

            st.subheader("Personal Information")

            col1, col2 = st.columns(2)

            col1.write("**Account Number:**")
            col1.write(details["account_no"])

            col1.write("**Email:**")
            col1.write(details["email"])

            col2.write("**Age:**")
            col2.write(details["age"])

            col2.write("**Account Created:**")
            col2.write(details["created_at"])

        else:

            st.error("Invalid PIN or account details.")


# =====================================================
# 10. DEPOSIT MONEY
# =====================================================

elif page == "Deposit Money":

    show_title(
        "Deposit Money",
        "Add money to your bank account."
    )

    account_no = st.session_state.account_no

    with st.form("deposit_form"):

        st.write(f"Account Number: {account_no}")

        pin = st.text_input(
            "Enter PIN",
            type="password",
            max_chars=4
        )

        amount = st.text_input(
            "Enter Deposit Amount (₹)",
            placeholder="Example: 5000 or 5000.50"
        )

        submitted = st.form_submit_button(
            "Deposit Money",
            use_container_width=True
        )

        if submitted:

            try:
                success, result = bank.deposit(
                    account_no,
                    pin,
                    amount
                )

                if success:

                    st.success(result["message"])

                    col1, col2 = st.columns(2)

                    col1.metric(
                        "Deposited Amount",
                        f"₹ {result['deposited']}"
                    )

                    col2.metric(
                        "Updated Balance",
                        f"₹ {result['balance']}"
                    )

                else:

                    st.error(result)

            except RuntimeError as error:

                st.error(str(error))


# =====================================================
# 11. WITHDRAW MONEY
# =====================================================

elif page == "Withdraw Money":

    show_title(
        "Withdraw Money",
        "Withdraw money from your bank account."
    )

    account_no = st.session_state.account_no

    with st.form("withdraw_form"):

        st.write(f"Account Number: {account_no}")

        pin = st.text_input(
            "Enter PIN",
            type="password",
            max_chars=4
        )

        amount = st.text_input(
            "Enter Withdrawal Amount (₹)",
            placeholder="Example: 1000 or 1000.50"
        )

        submitted = st.form_submit_button(
            "Withdraw Money",
            use_container_width=True
        )

        if submitted:

            try:
                success, result = bank.withdraw(
                    account_no,
                    pin,
                    amount
                )

                if success:

                    st.success(result["message"])

                    col1, col2 = st.columns(2)

                    col1.metric(
                        "Withdrawn Amount",
                        f"₹ {result['withdrawn']}"
                    )

                    col2.metric(
                        "Remaining Balance",
                        f"₹ {result['balance']}"
                    )

                else:

                    st.error(result)

            except RuntimeError as error:

                st.error(str(error))


# =====================================================
# 12. TRANSACTION HISTORY
# =====================================================

elif page == "Transaction History":

    show_title(
        "Transaction History",
        "View all your deposits and withdrawals."
    )

    account_no = st.session_state.account_no

    pin = verify_pin()

    if st.button(
        "View Transactions",
        use_container_width=True
    ):

        history = bank.get_transaction_history(
            account_no,
            pin
        )

        if history is None:

            st.error("Invalid PIN or account.")

        elif not history:

            st.info("No transactions found.")

        else:

            st.success(
                f"{len(history)} transaction(s) found."
            )

            df = pd.DataFrame(history)

            df = df.rename(
                columns={
                    "transaction_id": "Transaction ID",
                    "type": "Transaction Type",
                    "amount": "Amount (₹)",
                    "balance_after": "Balance After (₹)",
                    "timestamp": "Date & Time"
                }
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            deposits = sum(
                float(t["amount"])
                for t in history
                if t["type"] == "DEPOSIT"
            )

            withdrawals = sum(
                float(t["amount"])
                for t in history
                if t["type"] == "WITHDRAWAL"
            )

            st.divider()

            col1, col2 = st.columns(2)

            col1.metric(
                "Total Deposits",
                f"₹ {deposits:.2f}"
            )

            col2.metric(
                "Total Withdrawals",
                f"₹ {withdrawals:.2f}"
            )


# =====================================================
# 13. UPDATE PROFILE
# =====================================================

elif page == "Update Profile":

    show_title(
        "Update Account Details",
        "Change your personal information or PIN."
    )

    account_no = st.session_state.account_no

    st.info(
        "Leave any field blank if you do not want to change it."
    )

    with st.form("update_profile_form"):

        pin = st.text_input(
            "Current PIN",
            type="password",
            max_chars=4
        )

        name = st.text_input(
            "New Name",
            placeholder="Leave blank to keep unchanged"
        )

        email = st.text_input(
            "New Email",
            placeholder="Leave blank to keep unchanged"
        )

        age = st.text_input(
            "New Age",
            placeholder="Leave blank to keep unchanged"
        )

        new_pin = st.text_input(
            "New 4-digit PIN",
            type="password",
            max_chars=4,
            placeholder="Leave blank to keep unchanged"
        )

        submitted = st.form_submit_button(
            "Update Details",
            use_container_width=True
        )

        if submitted:

            try:

                age_value = None

                if age.strip():
                    age_value = int(age)

                success, result = bank.update_profile(
                    account_no,
                    pin,
                    name=name.strip() or None,
                    email=email.strip() or None,
                    age=age_value,
                    new_pin=new_pin or None
                )

                if success:

                    st.success(result)

                else:

                    st.error(result)

            except ValueError:

                st.error("Please enter a valid numeric age.")

            except RuntimeError as error:

                st.error(str(error))


# =====================================================
# 14. DELETE ACCOUNT
# =====================================================

elif page == "Delete Account":

    show_title(
        "Delete Bank Account",
        "Permanently delete your bank account."
    )

    st.warning(
        """
        This action is permanent.

        You can delete your account only when your
        account balance is zero.
        """
    )

    account_no = st.session_state.account_no

    with st.form("delete_account_form"):

        pin = st.text_input(
            "Enter your PIN",
            type="password",
            max_chars=4
        )

        confirmation = st.checkbox(
            "I understand that my account will be permanently deleted."
        )

        submitted = st.form_submit_button(
            "Delete My Account",
            use_container_width=True
        )

        if submitted:

            if not confirmation:

                st.error(
                    "Please confirm before deleting your account."
                )

            else:

                try:
                    success, result = bank.delete_account(
                        account_no,
                        pin
                    )

                    if success:

                        st.success(result)

                        st.session_state.logged_in = False
                        st.session_state.account_no = None

                        st.rerun()

                    else:

                        st.error(result)

                except RuntimeError as error:

                    st.error(str(error))


# =====================================================
# 15. LOGOUT
# =====================================================

elif page == "Logout":

    st.title("Logout")

    st.write(
        "Are you sure you want to logout?"
    )

    if st.button(
        "Yes, Logout",
        use_container_width=True
    ):

        logout()

