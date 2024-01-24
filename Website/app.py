import streamlit as st
import Front_page
from st_pages import Page, show_pages, add_page_title, hide_pages


# Set up the main configuration of the app
st.set_page_config(page_title="CodeKata Battles", page_icon="⛩️")

if 'login_status' not in st.session_state:
    st.session_state['login_status'] = False
    
pages = {
    "Login/Sign up": Front_page,
}



# Display the front page by default or when not logged in
if not st.session_state['login_status']:
    pages["Login/Sign up"].show()

 
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
