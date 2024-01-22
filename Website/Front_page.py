# Front_page.py
import pickle
from pathlib import Path
import streamlit as st
from Authenticator_role.streamlit_authenticator import Authenticate
import yaml


def show():
    st.title("Login/Sign up")
    
    config_path = Path(__file__).parent / "config.yaml"
    with open(config_path) as file:
        config = yaml.safe_load(file)

    # Initialize authenticator with the configuration
    authenticator = Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )
    
    authenticator.logout("Logout", "sidebar")
    # Toggle buttons for login and register
    if 'show_login' not in st.session_state:
        st.session_state['show_login'] = False

    if 'show_register' not in st.session_state:
        st.session_state['show_register'] = False

    if st.button("Login"):
        st.session_state['show_login'] = True
        st.session_state['show_register'] = False

    if st.button("Register"):
        st.session_state['show_register'] = True
        st.session_state['show_login'] = False

    # Display login widget
    if st.session_state['show_login']:
        name, authentication_status, username = authenticator.login("main")
        st.session_state['login_status'] = authentication_status
        st.sidebar.title(f"Welcome {name}")
        if authentication_status == False:
            st.error("Username/password is incorrect")

        elif authentication_status == None:
            st.warning("Please enter your username and password")

    # Display register widget
    if st.session_state['show_register']:
        try:
            if authenticator.register_user(preauthorization=False):
                st.session_state['show_login'] = True
        except Exception as e:
            st.error(e)