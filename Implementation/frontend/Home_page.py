import pandas as pd
from .util import button_call, dataframe_with_selections
import streamlit as st


def show():
    st.markdown(f"# ⛩️ Welcome back, {st.session_state.to_dict()['username']}")
    st.write('#')

    col1, col2 = st.columns(2)
    c3 = st.columns(1)

    with col1:

        st.subheader ("Ongoing Tournmanents")
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
        st.subheader ("Upcoming Tournaments")
        df = pd.DataFrame(
        {
            "Tournament name": ["Basic", "Medium", "Advanced"],
            "Subscriber count": [100, 50, 75],
            "Creator": ["John", "Aske", "Lise"],
            "Battle Count": [100, 50, 75],
            "Tournament id": [100, 200, 75],

        }
        )

        selection = dataframe_with_selections(df,)
        # st.write("Your selection:")
        # st.write(selection)

        if selection['selected_rows_indices'] != []:
            st.session_state['Tournament_Id'] = selection['selected_rows']['Tournament id'].iloc[0]
            button_call("Tournament details")

    with c3[0]:
        option = st.selectbox(
        "Search other users",
        ("Email", "Home phone", "Mobile phone"),
        index=None,
        placeholder="Select user profile...",
        )

        st.write('You selected:', option)