# Front_page.py
from menu import menu
from backend.backend import Authentication_info, Student,Educator
import streamlit as st
from pages.Authenticator_role.streamlit_authenticator.authenticate import Authenticate

def login_setup():
    Authentication = Authentication_info()
    credentials = Authentication.get_credentials()
    max_id_ = Authentication.get_max_id()
    
    authenticator = Authenticate(
    credentials,
    cookie_name="CKB_cookie",
    key="CKB_key",
    cookie_expiry_days=30,
    max_id=max_id_
    )
    return Authentication,credentials,authenticator

Authentication,credentials,authenticator = login_setup()

def init_variables():
    # Toggle buttons for login and register
    if 'show_login' not in st.session_state:
        st.session_state['show_login'] = False

    if 'show_register' not in st.session_state:
        st.session_state['show_register'] = False

    if "role" not in st.session_state:
        st.session_state.role = None

    if 'login_status' not in st.session_state:
        st.session_state['login_status'] = False

    if st.button("Login"):
        st.session_state['show_login'] = True
        st.session_state['show_register'] = False

    if st.button("Register"):
        st.session_state['show_register'] = True
        st.session_state['show_login'] = False
    st.session_state['authenticator'] = authenticator
    return None,None


st.title("Login & Sign up")
username, name = init_variables()
roles ={"Student": Student, "Educator": Educator}

# Display login widget
if st.session_state['show_login']:
    name, authentication_status, username = authenticator.login("main")
    st.session_state['login_status'] = authentication_status
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

st.session_state['username'] = username
st.session_state['role']  = credentials['usernames'].get(username, {}).get('role', None)

if isinstance(st.session_state['role'],str):
    st.session_state['user_id'] = Authentication.get_uid(st.session_state['username'])
    st.session_state['user_object'] = roles[st.session_state['role']](st.session_state['user_id'])
    st.session_state['authenticator'] = authenticator

    st.switch_page("pages/Home_page.py")

menu(app_page=True) # Render the dynamic menu!

