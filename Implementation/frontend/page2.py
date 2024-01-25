import streamlit as st

def page2():
    st.title("Page 2")
    st.write("This is the content of page 2.")
    st.write(st.session_state['some_val'])
    if st.button("Go to Page 1"):
        st.session_state.page = 'page1'
        st.experimental_rerun()