import streamlit as st
from database import get_products, get_db, User
import hashlib
import bcrypt  # For password hashing

# Authentication and Registration
def register(html_form):
    name = html_form['name']
    phone = html_form['phone']
    email = html_form['email']
    password = html_form['password']

    # Hash password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    try:
        with get_db() as db:  # Use 'with' to correctly handle the session
            # Check if user already exists
            existing_user = db.query(User).filter(User.email == email).one_or_none()
            if existing_user:
                st.error("User already exists")
                return

            # Create new user
            new_user = User(name=name, phone=phone, email=email, hashed_password=hashed_password)
            db.add(new_user)
            db.commit()
            st.success("Registration successful! Please log in.")
    except Exception as e:
        st.error(f"Error registering user: {e}")


def login(html_form):
    email = html_form['email']
    password = html_form['password']

    try:
        with get_db() as db:  # Use 'with' to correctly handle the session
            user = db.query(User).filter(User.email == email).one_or_none()

            if user:
                if bcrypt.checkpw(password.encode(), user.hashed_password.encode()):
                    st.session_state["authenticated"] = True
                    st.session_state["user_email"] = email
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Incorrect password.")
            else:
                st.error("User not found.")
    except Exception as e:
        st.error(f"Error logging in: {e}")



def login_or_register_page():
    # If user is already authenticated, skip login/register page
    if st.session_state.get("authenticated", False):
        st.success(f"Welcome back, {st.session_state['user_email']}!")
        return  # You can redirect or load a specific page/dashboard here

    st.header("Login or Register")
    option = st.radio("Select an option", ["Login", "Register"])

    if option == "Login":
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                login({"email": email, "password": password})
    elif option == "Register":
        with st.form("register_form"):
            name = st.text_input("Full Name")
            phone = st.text_input("Phone")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Register")
            if submitted:
                if name and phone and email and password:
                    register({"name": name, "phone": phone, "email": email, "password": password})
                else:
                    st.error("Please fill in all fields.")

def app():
    login_or_register_page()
