import streamlit as st
import yaml
from pathlib import Path
import Login_signup
from Authenticator_role.streamlit_authenticator.authenticate import Authenticate
from st_pages import Page, show_pages, add_page_title, hide_pages


# Set up the main configuration of the app
st.set_page_config(page_title="CodeKata Battles", page_icon="⛩️")

if 'login_status' not in st.session_state:
    st.session_state['login_status'] = False
    
pages = {
    "Login/Sign up": Login_signup,
}

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

# Display the front page by default or when not logged in
if not st.session_state['login_status'] or st.session_state['logout']:
    st.session_state['logout'] = False
    authenticator, username, name = Login_signup.show(authenticator)
    # Fetch and store the user's role upon successful login
    user_info = config['credentials']['usernames'].get(username, {})

    st.session_state['role'] = user_info.get('role', None)  # Default to None if role is not defined
    st.session_state['name'] = name


elif st.session_state['login_status']:
    if st.session_state['role'] == "Educator":
        
       
        show_pages(
            [
                Page("Home_page.py", "Home", "⛩️"),
                Page("My_Tournaments_page.py", "My Tournaments", "🏆"),
                Page("My_Battles_page.py", "My Battles", "⚔️"),
                Page("Create_battle.py", "Create Battle", "⚔️"),
                Page("My_Profile_page.py", "My Profile", "𖠌"),
                Page("Tournament_page.py", ""),
                Page("Battle_page.py", ""),
                Page("Login_signup_test.py", "test"),
                Page("Logout_page.py", "Logout" )
            ]
            
        )
        
    #    hide_pages(
    #        "My Battles"
    #    )
        
        
        
    elif st.session_state['role'] == "Student":
        hide_pages(
            [
                "Create Battle"
            ]
        )
        
        # Show other pages if logged in
else:
    st.error("Please log in to access this page")