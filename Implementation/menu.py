import streamlit as st

def authenticated_menu():
    # Show a navigation menu for authenticated users
    try:
        if st.session_state.role in ["Student", "Educator"]:
            st.sidebar.page_link("pages/Home_page.py", label="Home")
            st.sidebar.page_link("pages/My_Battles_page.py", label="My Battles")
            st.sidebar.page_link("pages/My_Tournaments_page.py", label = "My Tournament")
            st.sidebar.page_link("pages/My_Profile_page.py", label = "My Tournament")
        if st.session_state.role == "Educator":
            st.sidebar.page_link("pages/Submissions.py", label="Grade Submissions")
            st.sidebar.page_link("pages/Create_badge.py", label="Create Badge")
            st.sidebar.page_link("pages/Create_battle.py", label="Create Battle")
            st.sidebar.page_link("pages/Create_tournament.py", label="Create Tournament")
    except KeyError:
        pass

    if 'authenticator' in st.session_state:
        st.session_state['authenticator'].logout('Logout','sidebar')

def unauthenticated_menu(app_page=False):
    # Show a navigation menu for unauthenticated users
    if not app_page:
        st.switch_page("app.py")
    st.sidebar.page_link("app.py", label="Log in & Sign up")


def menu(app_page=False):
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    if st.session_state['login_status'] != True:
        unauthenticated_menu(app_page)
        return
    authenticated_menu()


def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        st.switch_page("app.py")
    menu()