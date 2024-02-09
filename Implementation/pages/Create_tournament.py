import streamlit as st
import datetime
from menu import menu

menu()


with st.form(key='tournament_form'):
    st.markdown("# Create New Tournament")

    # Text input for tournament name
    tournament_name = st.text_input("Tournament Name")

    # Date input for subscription deadline
    subscription_deadline = st.date_input("Subscription Deadline", min_value=datetime.date.today())

    # Text area for brief description
    brief_description = st.text_area("Brief Description")


    # Form submit button
    submit_button = st.form_submit_button(label='Create Tournament')

    if submit_button:
        # Handle the form submission here

        tournament_data = {'_TOURNAMENT_NAME_': tournament_name,
                        '_SUBSCRIPTION_DEADLINE_':subscription_deadline,
                        '_DESCRIPTION_':brief_description}

        st.session_state['user_object'].create_tournament(tournament_data)
        st.balloons()



