


st.write(st.session_state.page)

def page1():
    st.title("Page 1")
    st.write("This is the content of page 1.")
    if st.button("Go to Page 2"):
        st.session_state.page = 'page2'
        st.experimental_rerun()

def page2():
    st.title("Page 2")
    st.write("This is the content of page 2.")
    if st.button("Go to Page 1"):
        st.session_state.page = 'page1'
        st.experimental_rerun()

# Display the appropriate page based on the session state
if st.session_state.page == 'page1':
    page1()
elif st.session_state.page == 'page2':
    page2()


st.write(st.session_state.page)