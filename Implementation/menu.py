import streamlit as st
from backend.backend import Student, Educator

def authenticated_menu():
    # Show a navigation menu for authenticated users
    # st.sidebar.page_link("app.py", label="Switch accounts")
    print(f'{st.session_state.role=}')
    
    if st.session_state.role in ["Student", "Educator"]:
        st.sidebar.page_link("pages/Home_page.py", label="Home")
        st.sidebar.page_link("pages/My_Battles_page.py", label="My Battles")
        st.sidebar.page_link("pages/My_Tournaments_page.py", label = "My Tournament")
    if st.session_state.role == "Educator":
        st.sidebar.page_link("pages/Submissions.py", label="Grade Submissions")
        st.sidebar.page_link("pages/Create_badge.py", label="Create Badge")
        st.sidebar.page_link("pages/Create_battle.py", label="Create Battle")
        st.sidebar.page_link("pages/Create_tournament.py", label="Create Tournament")


def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("app.py", label="Log in")


def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    if st.session_state['login_status'] != True:
        unauthenticated_menu()
        return
    authenticated_menu()


def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        st.switch_page("app.py")
    menu()