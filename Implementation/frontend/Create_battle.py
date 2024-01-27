import datetime
import streamlit as st



def show():
    with st.form(key='battle_form'):
        st.markdown("# Create New Battle")

        # Text input for battle name
        battle_name = st.text_input("Battle Name")


        # Date input for deadlines
        registration_deadline = st.date_input("Registration Deadline", min_value=datetime.date.today())
        final_submission_deadline = st.date_input("Final Submission Deadline", min_value=datetime.date.today())

        brief_description = st.text_area("Brief Description")

        # Number input for min/max number of students per team
        min_students = st.number_input("Min Number of Students per Team", min_value=1, max_value=100, step=1)
        max_students = st.number_input("Max Number of Students per Team", min_value=1, max_value=100, step=1)

        # Form submit button
        submit_button = st.form_submit_button(label='Create Battle')

        if submit_button:

            battle_data = {'_BATTLE_NAME_': battle_name,
                            '_REGISTRATION_DEADLINE_':registration_deadline,
                            "_END_DATE_":final_submission_deadline,
                            '_BATTLE_DESC_':brief_description,
                            '_TOURNAMENT_ID_':st.session_state['current_tournament_id'],
                            '_MIN_GROUP_SIZE_':min_students,
                            '_MAX_GROUP_SIZE_':max_students}

            returned = st.session_state['user_object'].create_battle(battle_data)


            # TODO : FIX ENTIRE GITHUB IMPLEMENTATION IN BACKEND MODULE
            if returned == 0:
                st.balloons()
            else:
                st.error(returned)


            

            """
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
            """


