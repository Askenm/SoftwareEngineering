import streamlit as st


def show():
    st.markdown("# ⚔️ My Battles")
    st.write('#')

    col1, col2 = st.columns(2)

    with col1:
        st.subheader ("My ongoing Battles")
        #can st.button label be replaced with id dependant DB content of specific tournaments?
        #can switch page be provided with DB id of the corresponding tournament, for Tournament_page to be populated with the corresponding tournament data?
        if st.button("While loop battle  \nin Python Iteration tournament  \nfinal submission deadline: date"):
            st.switch_page("Battle_page.py")
        
        # check this for page link open in same tab while keeping session state: https://github.com/streamlit/streamlit/issues/7464
        button = st.link_button(
            "While loop battle  \nin Python Iteration tournament  \nfinal submission deadline: date",
            "/My%20Profile"
            )
            

    with col2:
        st.subheader ("My upcoming Battles")
        #hardcoded, to be replaced by fetched tournament info from DB
        
        button = st.link_button(
            "While loop battle  \nregistration deadline: date",
            "/My%20Profile"
            )