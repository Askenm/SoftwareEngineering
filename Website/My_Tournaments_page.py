import streamlit as st


st.markdown("# 🏆 My Tournaments")
st.write('#')

col1, col2 = st.columns(2)

with col1:
    st.subheader ("My ongoing Tournmanents")
    #can st.button label be replaced with id dependant DB content of specific tournaments?
    #can switch page be provided with DB id of the corresponding tournament, for Tournament_page to be populated with the corresponding tournament data?
    if st.button("Python Iteration tournament"):
        st.switch_page("Tournament_page.py")
    
    # check this for page link open in same tab while keeping session state: https://github.com/streamlit/streamlit/issues/7464
    button = st.link_button(
        "Python Iterations tournament",
        "/My%20Profile"
        )
        

with col2:
    st.subheader ("My upcoming Tournaments")
    #hardcoded, to be replaced by fetched tournament info from DB
    
    button = st.link_button(
        "Python Iterations tournament  \nsubscription deadline: date",
        "/My%20Profile"
        )

