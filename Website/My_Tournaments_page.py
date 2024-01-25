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
    
    
    if st.button("Python Iteration tournament", key=1):
        st.switch_page("Tournament_page.py")
        

with col2:
    
    st.subheader ("My upcoming Tournmanents")
    #can st.button label be replaced with id dependant DB content of specific tournaments?
    #can switch page be provided with DB id of the corresponding tournament, for Tournament_page to be populated with the corresponding tournament data?
    if st.button("Python Iteration tournament", key=2):
        st.switch_page("Tournament_page.py")