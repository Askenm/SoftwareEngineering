import pandas as pd
from .util import button_call, dataframe_with_selections
import streamlit as st

def show():
    st.markdown("# ⚔️ My Battles")
    st.write('#')

    col1, col2 = st.columns(2)

    with col1:
        st.subheader ("My ongoing Battles")
        df = pd.DataFrame(
        {
            "Tournament name": ["Basic", "Medium", "Advanced"],
            "Subscriber count": [120, 50, 75],
            "Creator": ["John", "Aske", "Lise"],
            "Battle Count": [100, 56, 75],
            "Battle_Id id": [150, 50, 77],})

        selection = dataframe_with_selections(df)

        if selection['selected_rows_indices'] != []:
            st.session_state['Battle_Id'] = selection['selected_rows']['Battle_Id id'].iloc[0]
            button_call("Battle details")
            

    with col2:
        st.subheader ("My upcoming Battles")
        df = pd.DataFrame(
        {
            "Tournament name": ["Basic", "Medium", "Advanced"],
            "Subscriber count": [120, 50, 75],
            "Creator": ["John", "Aske", "Lise"],
            "Battle Count": [100, 56, 75],
            "Battle_Id id": [150, 57, 75],})

        selection = dataframe_with_selections(df)

        if selection['selected_rows_indices'] != []:
            st.session_state['Battle_Id'] = selection['selected_rows']['Battle_Id id'].iloc[0]
            button_call("Battle details")