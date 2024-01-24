import streamlit as st
import yaml
from pathlib import Path
import Login_signup as Login_signup
import My_battles, My_Tournaments_page, Home_page, Create_tournament, Create_badge, Create_battle, My_Profile_page, My_Battles_page
from Authenticator_role.streamlit_authenticator import Authenticate

# Set up the main configuration of the app
st.set_page_config(page_title="CodeKata Battles", page_icon="CBK")

if 'login_status' not in st.session_state:
    st.session_state['login_status'] = False

# Define the page navigation
pages = {
    #"Login/Sign up": Login_signup,
    "Tournaments": My_Tournaments_page,
    "Battle page": My_battles,
    "User profile": Home_page,
    "My profile": My_Profile_page,
    "My battles": My_Battles_page
}
student_pages = {
}
educator_pages = {"Create Battle": Create_battle,
                  "Create Tournament": Create_tournament, 
                  "Create Badge": Create_badge,
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
# Function to show appropriate pages based on role
def show_pages_based_on_role():
    if st.session_state['role'] == "Educator":
        #combined_pages = {**pages, **educator_pages}
        page = st.sidebar.radio("Select your page", list(pages))
        pages[page].show()
    elif st.session_state['role'] == "Student":
        combined_pages = {**pages, **student_pages}
        page = st.sidebar.radio("Select your page", list(combined_pages))
        combined_pages[page].show()

# Display the front page by default or when not logged in
if not st.session_state['login_status'] or st.session_state['logout']:
    st.session_state['logout'] = False
    authenticator, username, name = Login_signup.show(authenticator)
    # Fetch and store the user's role upon successful login
    user_info = config['credentials']['usernames'].get(username, {})

    st.session_state['role'] = user_info.get('role', None)  # Default to None if role is not defined
    st.session_state['name'] = name
# Show other pages if logged in
elif st.session_state['login_status']:

    st.sidebar.title(f"Welcome {st.session_state['name']}, {st.session_state['role']}")
    show_pages_based_on_role()

    authenticator.logout("Logout","sidebar")

else:
    st.error("Please log in to access this page")


# import streamlit as st
# import Login_signup
# import Front_page
# from st_pages import Page, show_pages, add_page_title, hide_pages


# # Set up the main configuration of the app
# st.set_page_config(page_title="CodeKata Battles", page_icon="⛩️")

# if 'login_status' not in st.session_state:
#     st.session_state['login_status'] = False
    
# pages = {
#     "Login/Sign up": Front_page,
# }



# # Display the front page by default or when not logged in
# if not st.session_state['login_status']:
#     pages["Login/Sign up"].show()

 
# elif st.session_state['login_status']:
#     if st.session_state['role'] == "Educator":
        
#         show_pages(
#             [
#                 Page("Home_page.py", "Home", "⛩️"),
#                 Page("My_Tournaments_page.py", "My Tournaments", "🏆"),
#                 Page("My_Battles_page.py", "My Battles", "⚔️"),
#                 Page("Create_battle.py", "Create Battle", "⚔️"),
#                 Page("My_Profile_page.py", "My Profile", "𖠌"),
#                 Page("Tournament_page.py", ""),
#                 Page("Battle_page.py", ""),
#             ]
#         )
#     #    hide_pages(
#     #        "My Battles"
#     #    )
        
        
        
#     elif st.session_state['role'] == "Student":
#         hide_pages(
#             [
#                 "Create Battle"
#             ]
#         )
        
#         # Show other pages if logged in
# else:
#     st.error("Please log in to access this page")