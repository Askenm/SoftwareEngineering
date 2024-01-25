import pandas as pd
from util import button_call, dataframe_with_selections
import streamlit as st

def show():
    #hardcoded for testing
    #title should be fetched from DB of specific battle
    #need to figure out how to get st.switch_pages to pass on a battle ID to Battle_page.py

    st.markdown("# ⚔️ While loop Battle")
    st.write('#')

    c1, c2, = st.columns(2)
    c3, c4, = st.columns(2)
    c5 = st.columns(1)

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
        
    with c5[0]:
        st.write('##')
        st.subheader ("𖠌 Subscribers")
        df = pd.DataFrame(
            {
                "Team names": ["Basic", "Medium", "Advanced"],
                "Number of submissions": [120, 50, 75],
                "Group participants": ["John & Tokia", "Aske", "Lise"],})

        selection = dataframe_with_selections(df)

        if selection['selected_rows_indices'] != []:
            st.session_state['Tournament_Id'] = selection['selected_rows']['Tournament id'].iloc[0]
            button_call("Tournament details")
            