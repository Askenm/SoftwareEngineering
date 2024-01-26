import datetime
import streamlit as st



def show():
    with st.form(key='battle_form'):
        st.markdown("# Create New Battle")

        # Text input for battle name
        battle_name = st.text_input("Battle Name")

        # Selectbox for parent tournament
        parent_tournament = st.selectbox("Parent Tournament", ["Tournament 1", "Tournament 2", "Tournament 3"])

        # Date input for deadlines
        registration_deadline = st.date_input("Registration Deadline", min_value=datetime.date.today())
        final_submission_deadline = st.date_input("Final Submission Deadline", min_value=datetime.date.today())

        # Radio buttons for status
        status = st.radio("Status", ['Active', 'Inactive'])

        # Text input for creator's name
        creator_name = st.text_input("Creator Name")

        # Number input for min/max number of students per team
        min_students = st.number_input("Min Number of Students per Team", min_value=1, max_value=100, step=1)
        max_students = st.number_input("Max Number of Students per Team", min_value=1, max_value=100, step=1)

        # Multiselect for participant list
        participant_list = st.multiselect("Participant List", ["Student 1", "Student 2", "Student 3"])

        # Form submit button
        submit_button = st.form_submit_button(label='Create Battle')

        if submit_button:
            # Handle the form submission here
            st.write("Battle Name:", battle_name)
            st.write("Parent Tournament:", parent_tournament)
            st.write("Registration Deadline:", registration_deadline)
            st.write("Final Submission Deadline:", final_submission_deadline)
            st.write("Status:", status)
            st.write("Creator Name:", creator_name)
            st.write("Min Students per Team:", min_students)
            st.write("Max Students per Team:", max_students)
            st.write("Participant List:", participant_list)


