import streamlit as st
import yaml
from pathlib import Path
import Login_signup as Login_signup
import Battle_details, My_Tournaments_page, Home_page, Create_tournament, Tournament_details, Create_battle, My_Profile_page, My_Battles_page, Create_badge
from Authenticator_role.streamlit_authenticator import Authenticate

def setup(__file__):
    # Set up the main configuration of the app
    st.set_page_config(page_title="CodeKata Battles", page_icon="CBK")

    if 'login_status' not in st.session_state:
        st.session_state['login_status'] = False

    if 'switch_pages_button' not in st.session_state:
        st.session_state['switch_pages_button'] = False

    # Define the page navigation
    pages = {
    "Tournaments": My_Tournaments_page,
    "Home": Home_page,
    "My profile": My_Profile_page,
    "My battles": My_Battles_page,
}

    educator_pages = {"Create Battle": Create_battle,
                  "Create Tournament": Create_tournament, 
                  "Create Badge": Create_badge
}
    hidden_pages = {
    "Battle details": Battle_details,
    "Tournament details": Tournament_details,

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
    
    return pages,educator_pages,hidden_pages,config,authenticator

# Initiliazes the authenticator object, session state dict, and pages dict
pages, educator_pages, hidden_pages, config, authenticator = setup(__file__)


def show_pages_based_on_role():
    # Function that returns the pages appropriate pages based on role
    if st.session_state['role'] == "Educator":
        combined_pages = {**pages, **educator_pages}
        st.session_state['sidebar_page'] = st.sidebar.radio("Select your page", list(combined_pages))
        return combined_pages
    elif st.session_state['role'] == "Student":
        st.session_state['sidebar_page'] = st.sidebar.radio("Select your page", list(pages))
        return pages 
# Main app logic
if not st.session_state['login_status'] or st.session_state['logout']:
    st.session_state['logout'] = False
    authenticator, username, name = Login_signup.show(authenticator)

    # Fetch and store the user's role upon successful login
    user_info = config['credentials']['usernames'].get(username, {})
    st.session_state['role'] = user_info.get('role', None)  
    st.session_state['name'] = name

elif st.session_state['login_status']:
    st.sidebar.title(f"Welcome {st.session_state['name']}, {st.session_state['role']}")
    pages = show_pages_based_on_role()
    if not st.session_state['switch_pages_button']:
        pages[st.session_state['sidebar_page']].show()
    else:
        st.session_state['switch_pages_button'] = False
        if st.session_state['current_page'] not in pages:
            hidden_pages[st.session_state['current_page']].show()
        else:
            pages[st.session_state['current_page']].show()
        
    authenticator.logout("Logout", "sidebar")
else:
    st.error("Please log in to access this page")


