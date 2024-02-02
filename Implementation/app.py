import streamlit as st
import yaml
from pathlib import Path

import frontend.Login_signup as Login_signup
import frontend.Battle_details as Battle_details
import frontend.My_Tournaments_page as My_Tournaments_page
import frontend.Home_page as Home_page
import frontend.Create_tournament as Create_tournament
import frontend.Tournament_details as Tournament_details
import frontend.Create_battle as Create_battle
import frontend.My_Profile_page as My_Profile_page
import frontend.My_Battles_page as My_Battles_page
import frontend.Create_badge as Create_badge

from frontend.Authenticator_role.streamlit_authenticator import Authenticate


from backend.backend import Student,Educator




def setup(__file__):
    # Set up the main configuration of the app
    st.set_page_config(page_title="CodeKata Battles", page_icon="CBK")

    if 'login_status' not in st.session_state:
        st.session_state['login_status'] = False

    if 'switch_pages_button' not in st.session_state:
        st.session_state['switch_pages_button'] = False

    # Define the page navigation
    pages = {
    "Home": Home_page,
    "My Tournaments": My_Tournaments_page,
    "My Battles": My_Battles_page,
    "My Profile": My_Profile_page,
    
    }

    educator_pages = {"Create Battle": Create_battle,
                  "Create Tournament": Create_tournament, 
                  "Create Badge": Create_badge
    }
    hidden_pages = {
    "Battle details": Battle_details,
    "Tournament details": Tournament_details,

    }

    # TODO: Replace the use of the yaml file with 
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
    
    return pages, educator_pages, hidden_pages, config, authenticator




def show_pages_based_on_role():
    # Function that returns the pages appropriate pages based on role
    if st.session_state['role'] == "Educator":
        combined_pages = {**pages, **educator_pages}
        st.session_state['sidebar_page'] = st.sidebar.radio("Select your page", list(combined_pages))
        return combined_pages
    elif st.session_state['role'] == "Student":
        st.session_state['sidebar_page'] = st.sidebar.radio("Select your page", list(pages))
        return pages 
    

if __name__ == '__main__':
    # Initiliazes the authenticator object, session state dict, and pages dict
    pages, educator_pages, hidden_pages, config, authenticator = setup(__file__)

    # SCAFFOLDING
    # TODO
    ###############
    # This should be retrieved from the DB upon login
    st.session_state['user_id'] = 5

    # This should be tracked when navigating to the a given tournament/battle page
    # Only hardcoded here in order to test other functionality
    #st.session_state['current_tournament_id'] = 16
    st.session_state['current_battle_id'] = 29
    ################




    # A global Student or Educator object is assigned upon login
    # these objects can be used to view stuff, create stuff, delete stuff etc
    roles = {'Educator':Educator,
             'Student':Student}
    
    # The object is saved in the session_state here
    
    

    # Main app logic
    if not st.session_state['login_status'] or st.session_state['logout']:
        st.session_state['logout'] = False
        authenticator, username, name = Login_signup.show(authenticator)

        # Fetch and store the user's role upon successful login
        user_info = config['credentials']['usernames'].get(username, {})
        st.session_state['role'] = user_info.get('role', None)  
        st.session_state['name'] = name
        if isinstance(st.session_state['role'],str):
            #print(st.session_state.to_dict())
            st.session_state['user_object'] = roles[st.session_state['role']](st.session_state['user_id'])

    elif st.session_state['login_status']:
        st.session_state['user_object'] = roles[st.session_state['role']](st.session_state['user_id'])
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


