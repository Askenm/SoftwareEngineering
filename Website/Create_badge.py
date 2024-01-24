import streamlit as st

#hardcoded for testing
#title should be fetched from DB of specific tournament
#need to figure out how to get st.switch_pages to pass on a tournament ID to Tournament_page.py
st.markdown("# 🏆 Python Iteration Tournament")
st.write('#')

c1, c2, = st.columns([3, 1])
c3, c4, = st.columns(2)
c5, c6, = st.columns(2)

with c1:
    st.caption("Description")
    container = st.container(border=True)
    container.write("This is a tournament description")

with c2:
    st.caption("Subscription deadline")
    container = st.container(border=True)
    container.write("date")

with c3: 
    st.write('##')
    st.subheader ("⚔️ Ongoing Battles")
    #can st.button label be replaced with id dependant DB content of specific tournaments?
    #can switch page be provided with DB id of the corresponding tournament, for Tournament_page to be populated with the corresponding tournament data?
    if st.button("While loop battle  \nfinal submission deadline: date"):
        st.switch_page("Battle_page.py")
    if st.button("While loop battle  \nfinal submission deadline: date", key=1):
        st.switch_page("Battle_page.py")
    if st.button("While loop battle  \nfinal submission deadline: date", key=2):
        st.switch_page("Battle_page.py")

with c4:
    st.write('##')
    st.subheader ("🚀 Ranking")
    col1, col2, col3 = st.columns([1,3,2])
    with col1:
        container = st.container(border=True, height=40)
        container.write("1")
        
        container = st.container(border=True, height=40)
        container.write("2")
        
        container = st.container(border=True, height=40)
        container.write("3")
        
    with col2:
        if st.button("user_name1", key=4):
            st.switch_page("My_Profile_page.py")
        
        if st.button("user_name2", key=5):
            st.switch_page("My_Profile_page.py")
        
        if st.button("user_name3", key=6):
            st.switch_page("My_Profile_page.py")
    
    with col3:
        container = st.container(border=True, height=40)
        container.write("500")
        
        container = st.container(border=True, height=40)
        container.write("450")
        
        container = st.container(border=True, height=40)
        container.write("300")
        
        

with c5:
    st.write('##')
    st.subheader ("⚔️ Upcoming Battles")
    #hardcoded, to be replaced by fetched tournament info from DB
    if st.button("While loop battle  \nfinal submission deadline: date", key=3):
        st.switch_page("Battle_page.py")
    

with c6:
    st.write('##')
    st.subheader ("𖠌 Subscribers")
    col4, col5 = st.columns(2)
    with col4:
        if st.button("user_name1", key=7):
            st.switch_page("My_Profile_page.py")
        if st.button("user_name2", key=8):
            st.switch_page("My_Profile_page.py")
        if st.button("user_name3", key=9):
            st.switch_page("My_Profile_page.py")
    with col5: 
        if st.button("user_name4", key=10):
            st.switch_page("My_Profile_page.py")
        if st.button("user_name5", key=11):
            st.switch_page("My_Profile_page.py")
        if st.button("user_name6", key=12):
            st.switch_page("My_Profile_page.py")

