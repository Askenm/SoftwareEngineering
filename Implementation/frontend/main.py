import streamlit as st
from page1 import page1
from page2 import page2


st.session_state['some_val'] = 0

# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = 'page1'


# Display the appropriate page based on the session state
if st.session_state.page == 'page1':
    page1()
elif st.session_state.page == 'page2':
    page2()