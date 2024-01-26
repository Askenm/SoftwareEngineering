import pandas as pd
from util import button_call, dataframe_with_selections
import streamlit as st

def show():
    st.markdown("# 🏆 My Tournaments")
    st.write('#')

    col1, col2 = st.columns(2)

    with col1:

        st.subheader ("My ongoing Tournmanents")
        df = pd.DataFrame(
        {
            "Tournament name": ["Basic", "Medium", "Advanced"],
            "Subscriber count": [100, 50, 75],
            "Creator": ["John", "Aske", "Lise"],
            "Battle Count": [100, 50, 75],
            "Tournament id": [100, 50, 75],

        }
        )

        selection = dataframe_with_selections(df)


        if selection['selected_rows_indices'] != []:
            st.session_state['Tournament_Id'] = selection['selected_rows']['Tournament id'].iloc[0]
            button_call("Tournament details")


    with col2:
        st.subheader ("My upcoming Tournaments")
        df = pd.DataFrame(
        {
            "Tournament name": ["Basic", "Medium", "Advanced"],
            "Subscriber count": [100, 50, 75],
            "Creator": ["John", "Aske", "Lise"],
            "Battle Count": [100, 50, 75],
            "Tournament id": [100, 200, 75],

        }
        )

        selection = dataframe_with_selections(df)

        if selection['selected_rows_indices'] != []:
            st.session_state['Tournament_Id'] = selection['selected_rows']['Tournament id'].iloc[0]
            button_call("Tournament details")

