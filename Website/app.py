import streamlit as st
import Front_page
import Tournament_page
import Battle_page
import Create_battle

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
student_pages = {
}
educator_pages = { "Create Battle": Create_battle,
}

# Function to show appropriate pages based on role
def show_pages_based_on_role():
    if st.session_state['role'] == "Educator":
        combined_pages = {**pages, **educator_pages}
        page = st.sidebar.radio("Select your page", list(combined_pages))
        print(combined_pages)
        combined_pages[page].show()
    elif st.session_state['role'] == "Student":
        combined_pages = {**pages, **student_pages}
        page = st.sidebar.radio("Select your page", list(combined_pages))
        combined_pages[page].show()

# Display the front page by default or when not logged in
if not st.session_state['login_status']:
    pages["Login/Sign up"].show()


# Show other pages if logged in
elif st.session_state['login_status']:
    show_pages_based_on_role()
else:
    st.error("Please log in to access this page")
