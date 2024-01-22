import streamlit as st
import Front_page
import Tournament_page
import Battle_page

# Set up the main configuration of the app
st.set_page_config(page_title="CodeKata Battles", page_icon="CBK")

if 'login_status' not in st.session_state:
    st.session_state['login_status'] = False
# Define the page navigation
pages = {
    "Login/Sign up": Front_page,
    "Tournament": Tournament_page,
    "Battle": Battle_page
}

# Display the front page by default or when not logged in
if not st.session_state['login_status']:
    pages["Login/Sign up"].show()


# Show other pages if logged in
elif 'login_status' in st.session_state and st.session_state['login_status']:
    print('prut')
    page = st.sidebar.radio("Select your page", list(pages.keys()))
    pages[page].show()

else:
    st.error("Please log in to access this page")
