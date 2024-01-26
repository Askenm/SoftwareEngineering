import streamlit as st
import datetime

def show():
    with st.form(key='tournament_form'):
        st.markdown("# Create New Tournament")

        # Text input for tournament name
        tournament_name = st.text_input("Tournament Name")

        # Date input for subscription deadline
        subscription_deadline = st.date_input("Subscription Deadline", min_value=datetime.date.today())

        # Radio buttons for status
        status = st.radio("Status", ['Active', 'Inactive'])

        # Text input for creator's name
        creator_name = st.text_input("Creator Name")

        # Text area for brief description
        brief_description = st.text_area("Brief Description")

        # Display active battles if the tournament is active
        if status == 'Active':
            active_battles = st.multiselect("Active Battles", ["Battle 1", "Battle 2", "Battle 3"])

        # Multiselect for upcoming battles
        upcoming_battles = st.multiselect("Upcoming Battles", ["Battle 4", "Battle 5", "Battle 6"])

        # Display ongoing rankings if the tournament is active
        if status == 'Active':
            ongoing_rankings = st.text("Ongoing Rankings")  # Modify as needed for your data structure

        # Number input for subscriber count
        subscriber_count = st.number_input("Subscriber Count", min_value=0, max_value=10000, step=1)

        # Multiselect for list of subscribers
        list_of_subscribers = st.multiselect("List of Subscribers", ["Subscriber 1", "Subscriber 2", "Subscriber 3"])

        # Form submit button
        submit_button = st.form_submit_button(label='Create Tournament')

        if submit_button:
            # Handle the form submission here
            st.write("Tournament Name:", tournament_name)
            st.write("Subscription Deadline:", subscription_deadline)
            st.write("Status:", status)
            st.write("Creator Name:", creator_name)
            st.write("Brief Description:", brief_description)
            if status == 'Active':
                st.write("Active Battles:", active_battles)
            st.write("Upcoming Battles:", upcoming_battles)
            if status == 'Active':
                st.write("Ongoing Rankings:", ongoing_rankings)
            st.write("Subscriber Count:", subscriber_count)
            st.write("List of Subscribers:", list_of_subscribers)