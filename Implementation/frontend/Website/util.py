import streamlit as st

def button_call(page_str):
    st.session_state['current_page'] = page_str
    st.session_state['switch_pages_button'] = True
    st.experimental_rerun()