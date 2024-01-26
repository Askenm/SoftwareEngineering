import pandas as pd
from .util import button_call, dataframe_with_selections
import streamlit as st


def show():
        st.markdown(f"# 𖠌 {st.session_state.to_dict()['username']}")
        st.write('#')
        st.subheader ("🏅 Awarded Badges")
        df = pd.DataFrame(
        {
            "Tournament name": ["Basic", "Medium", "Advanced"],
            "Subscriber count": [120, 50, 75],
            "Creator": ["John", "Aske", "Lise"],
            "Battle Count": [100, 56, 75],
            "Tournament id": [150, 50, 75],})

        selection = dataframe_with_selections(df)

        if selection['selected_rows_indices'] != []:
            st.session_state['Tournament_Id'] = selection['selected_rows']['Tournament id'].iloc[0]
            button_call("Tournament details")

        st.write('###')
        st.subheader ("🏆 Subscribed Tournaments")

        df = pd.DataFrame(
        {
            "Tournament name": ["Basic", "Medium", "Advanced"],
            "Subscriber count": [100, 50, 75],
            "Creator": ["John", "Aske", "Lise"],
            "Battle Count": [100, 50, 75],
            "Tournament id": [190, 50, 75],})

        selection = dataframe_with_selections(df)

        if selection['selected_rows_indices'] != []:
            st.session_state['Tournament_Id'] = selection['selected_rows']['Tournament id'].iloc[0]
            button_call("Tournament details")