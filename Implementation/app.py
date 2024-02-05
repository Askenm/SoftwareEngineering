import streamlit as st

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
import frontend.Submissions as Submissions

from frontend.Authenticator_role.streamlit_authenticator import Authenticate


from backend.backend import Student,Educator,Authentication_info

def init_pages():
        # Define the page navigation
    pages = {
    "Home": Home_page,
    "My Tournaments": My_Tournaments_page,
    "My Battles": My_Battles_page,
    "My Profile": My_Profile_page,
    }

    educator_pages = {"Create Battle": Create_battle,
                  "Create Tournament": Create_tournament, 
                  "Create Badge": Create_badge,
                  "Submissions": Submissions
    }
    
    hidden_pages = {
    "Battle details": Battle_details,
    "Tournament details": Tournament_details,
    }
    return pages, educator_pages, hidden_pages

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

def setup(__file__):
    # Set up the main configuration of the app
    st.set_page_config(page_title="CodeKata Battles", page_icon="CBK")

    if 'login_status' not in st.session_state:
        st.session_state['login_status'] = False

    if 'switch_pages_button' not in st.session_state:
        st.session_state['switch_pages_button'] = False

    pages, educator_pages, hidden_pages = init_pages()

    Authentication, credentials, authenticator = login_setup()   
    roles = {'Educator':Educator,
             'Student':Student}
    
    return pages, educator_pages, hidden_pages, authenticator, credentials, Authentication, roles


def show_pages_based_on_role():
    """Function that returns the pages appropriate pages based on role"""
    if st.session_state['role'] == "Educator":
        combined_pages = {**pages, **educator_pages}
        st.session_state['sidebar_page'] = st.sidebar.radio("Select your page", list(combined_pages))
        return combined_pages
    elif st.session_state['role'] == "Student":
        st.session_state['sidebar_page'] = st.sidebar.radio("Select your page", list(pages))
        return pages 
    

if __name__ == '__main__':
    # Initiliazes the authenticator object, session state dict, and pages dict
    pages, educator_pages, hidden_pages, authenticator, credentials, Authentication, roles = setup(__file__)

    # Main app logic
    if not st.session_state['login_status'] or st.session_state['logout']:
        print(f"{st.session_state['login_status'], st.session_state['logout']=}")
        st.session_state['logout'] = False
        authenticator, username, name = Login_signup.show(authenticator)
        # Fetch and store the user's role upon successful login
        st.session_state['role']  = credentials['usernames'].get(username, {}).get('role', None)

    elif st.session_state['login_status']:
        print(f"{st.session_state['login_status']=}")
        st.session_state['user_id'] = Authentication.get_uid(st.session_state['username'])
        if isinstance(st.session_state['role'],str):
            st.session_state['user_object'] = roles[st.session_state['role']](st.session_state['user_id'])
        st.sidebar.title(f"Welcome {st.session_state['name']}, {st.session_state['role']}")
        pages = show_pages_based_on_role()
        authenticator.logout("Logout", "sidebar")
        if not st.session_state['switch_pages_button']:
            print('sidebar_page')
            pages[st.session_state['sidebar_page']].show()
        else:
            print('current_page')
            st.session_state['switch_pages_button'] = False
            if st.session_state['current_page'] not in pages:
                hidden_pages[st.session_state['current_page']].show()
            else:
                pages[st.session_state['current_page']].show()
    else:
        st.error("Please log in to access this page")


