# Front_page.py
import streamlit as st



def show(authenticator):
    st.title("Login/Sign up")
    username, name = None,None
    
    # Toggle buttons for login and register
    if 'show_login' not in st.session_state:
        st.session_state['show_login'] = False

    if 'show_register' not in st.session_state:
        st.session_state['show_register'] = False

    if st.button("Login"):
        st.session_state['show_login'] = True
        st.session_state['show_register'] = False

    if st.button("Register"):
        st.session_state['show_register'] = True
        st.session_state['show_login'] = False

    # Display login widget
    if st.session_state['show_login']:
        name, authentication_status, username = authenticator.login("main")
        st.session_state['login_status'] = authentication_status
        if authentication_status == False:
            st.error("Username/password is incorrect")

        elif authentication_status == None:
            st.warning("Please enter your username and password")
        elif authentication_status == True:
            #st.experimental_rerun()
            print(f"{name, authentication_status, username=}")
            pass
    # Display register widget
    if st.session_state['show_register']:
        try:
            if authenticator.register_user(preauthorization=False):
                st.session_state['show_login'] = True
        except Exception as e:
            st.error(e)

    return authenticator, username, name