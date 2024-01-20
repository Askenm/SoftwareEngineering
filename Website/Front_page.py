# Front_page.py
import streamlit as st
from database_module import authenticate_user, create_user

def show():
    st.title("Login/Sign up")
    st.sidebar.success("Select a page above.")

    # Initialize login status in session state
    if 'login_status' not in st.session_state:
        st.session_state['login_status'] = False

    # Display logged-in message
    if st.session_state['login_status']:
        st.write("You are logged in.")
        # Here you can add logout functionality
    else:
        # Show login/signup form when not logged in
        choice = st.radio("Login/Signup", ("Login", "Signup"))

        if choice == "Login":
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                if authenticate_user(username, password):
                    st.session_state['login_status'] = True
                    st.success("Logged in successfully!")
                else:
                    st.error("Incorrect Username/Password")

        elif choice == "Signup":
            new_username = st.text_input("New Username")
            new_password = st.text_input("New Password", type="password")
            if st.button("Create Account"):
                create_user(new_username, new_password)
                st.success("Account created successfully! You can now login.")
