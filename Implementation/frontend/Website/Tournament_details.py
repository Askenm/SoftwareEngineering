import pandas as pd
from util import button_call, dataframe_with_selections
import streamlit as st

def show():
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
        df = pd.DataFrame(
        {
            "Tournament name": ["Basic", "Medium", "Advanced"],
            "Subscriber count": [100, 50, 75],
            "Creator": ["John", "Aske", "Lise"],
            "Battle Count": [100, 50, 75],
            "Tournament id": [150, 50, 75],})

        selection = dataframe_with_selections(df)

        if selection['selected_rows_indices'] != []:
            st.session_state['Tournament_Id'] = selection['selected_rows']['Tournament id'].iloc[0]
            button_call("Tournament details")

    with c4:
        st.write('##')
        st.subheader ("🚀 Ranking")
        df = pd.DataFrame(
        {
            "Tournament name": ["Basic", "Medium", "Advanced"],
            "Subscriber count": [190, 50, 75],
            "Creator": ["John", "Aske", "Lise"],
            "Battle Count": [100, 50, 75],
            "Tournament id": [150, 50, 75],})

        selection = dataframe_with_selections(df)

        if selection['selected_rows_indices'] != []:
            st.session_state['Tournament_Id'] = selection['selected_rows']['Tournament id'].iloc[0]
            button_call("Tournament details")
        
        

    with c5:
        st.write('##')
        st.subheader ("⚔️ Upcoming Battles")
        df = pd.DataFrame(
        {
            "Tournament name": ["Basic", "Medium", "Advanced"],
            "Subscriber count": [100, 50, 75],
            "Creator": ["John", "Aske", "Lise"],
            "Battle Count": [100, 56, 75],
            "Tournament id": [150, 50, 75],})

        selection = dataframe_with_selections(df)

        if selection['selected_rows_indices'] != []:
            st.session_state['Tournament_Id'] = selection['selected_rows']['Tournament id'].iloc[0]
            button_call("Tournament details")
    



