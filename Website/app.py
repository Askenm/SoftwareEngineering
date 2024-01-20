import streamlit as st
from database_module import authenticate_user, create_user
import Front_page
import Tournament_page
import Battle_page

# Set up the main configuration of the app
st.set_page_config(page_title="CodeKata Battles", page_icon="CBK")

# Initialize session state for login status if it doesn't exist
if 'login_status' not in st.session_state:
    st.session_state['login_status'] = False

# Define the page navigation
pages = {
    "Login/Sign up": Front_page,
    "Tournament": Tournament_page,
    "Battle": Battle_page
}

# Sidebar for navigation
page = st.sidebar.radio("Select your page", list(pages.keys()))

# Show the selected page
if page == "Login/Sign up" or st.session_state['login_status']:
    pages[page].show()  # Each page has a function called 'show' to display its content
else:
    st.error("Please log in to access this page")
