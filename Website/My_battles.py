import streamlit as st

def show():
    #hardcoded for testing
    #title should be fetched from DB of specific battle
    #need to figure out how to get st.switch_pages to pass on a battle ID to Battle_page.py

    st.markdown("# ⚔️ While loop Battle")
    st.write('#')

    c1, c2, = st.columns(2)
    c3, c4, = st.columns(2)
    #c5, c6, = st.columns(2)

    with c1:
        st.caption("Final Submission Deadline")
        container = st.container(border=True)
        container.write("Date")

    with c2:
        st.caption("Registration deadline")
        container = st.container(border=True)
        container.write("date")

    with c3: 
        st.write('##')
        col1, col2 = st.columns(2)
        with col1:
            st.caption("Min number of Students per Team")
            container = st.container(border=True)
            container.write("2")
        with col2:
            st.caption("Max number of Students per Team")
            container = st.container(border=True)
            container.write("4")



    with c4:
        st.write('##')
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        if st.button("💥 REGISTER"):
            st.toast('💥 THE BATTLE IS ON!! 💥')
        
    st.write('##')
    st.subheader ("𖠌 Subscribers")
    col3, col4, col5 = st.columns(3)
    with col3:
            if st.button("user_name1", key=7):
                st.switch_page("My_Profile_page.py")
            if st.button("user_name2", key=8):
                st.switch_page("My_Profile_page.py")
            if st.button("user_name3", key=9):
                st.switch_page("My_Profile_page.py")
    with col4: 
            if st.button("user_name4", key=10):
                st.switch_page("My_Profile_page.py")
            if st.button("user_name5", key=11):
                st.switch_page("My_Profile_page.py")
            if st.button("user_name6", key=12):
                st.switch_page("My_Profile_page.py")    
    with col5: 
            if st.button("user_name7", key=13):
                st.switch_page("My_Profile_page.py")
            if st.button("user_name8", key=14):
                st.switch_page("My_Profile_page.py")
            if st.button("user_name9", key=15):
                st.switch_page("My_Profile_page.py")  
        