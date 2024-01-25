import streamlit as st



st.markdown("# ⚔️ My Battles")
st.write('#')

col1, col2 = st.columns(2)

with col1:
    st.subheader ("My ongoing Battles")
    #can st.button label be replaced with id dependant DB content of specific tournaments?
    #can switch page be provided with DB id of the corresponding tournament, for Tournament_page to be populated with the corresponding tournament data?
    if st.button("While loop battle  \nin Python Iteration tournament  \nfinal submission deadline: date", key = 1):
        st.switch_page("Battle_page.py")
    
    if st.button("While loop battle  \nin Python Iteration tournament  \nfinal submission deadline: date", key=2):
        st.switch_page("Battle_page.py")
        

with col2:
    st.subheader ("My upcoming Battles")
    #hardcoded, to be replaced by fetched tournament info from DB
    
    if st.button("While loop battle  \nin Python Iteration tournament  \nfinal submission deadline: date", key=3):
        st.switch_page("Battle_page.py")