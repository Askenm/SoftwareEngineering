import streamlit as st

def page1():
    st.title("Page 1")
    st.write("This is the content of page 1.")
    
    st.session_state['some_val'] = st.slider('SCORE',0,10,st.session_state['some_val'])
    st.write(st.session_state['some_val'])

    if st.button("Go to Page 2"):
        st.session_state.page = 'page2'
        st.experimental_rerun()


    