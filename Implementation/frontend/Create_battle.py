import datetime
import streamlit as st



def show():
    with st.form(key='battle_form'):
        # TODO : EVERYTHING GOOD
        st.markdown("# Create New Battle")

        st.session_state['user_object'].get_home_page()
        st.session_state['your_tournaments'] = st.session_state['user_object'].user_information['user_tournaments']
        print(st.session_state['your_tournaments'])
        YourTournaments = st.session_state['your_tournaments']['tournament_name'].values.tolist()
        # Multi-select list
        options = st.multiselect("Your Tournaments", 
                                 YourTournaments
                                 ,max_selections=1)


        selected_indexes = [YourTournaments.index(uname) for uname in options]
        if selected_indexes:
            TournamentID = st.session_state['your_tournaments'].iloc[selected_indexes]['tid'].values.tolist()[0]
        

        # Text input for battle name
        battle_name = st.text_input("Battle Name")

        github_repo = st.text_input("Battle Repository")

        manual_scoring = st.radio("Choose the scoring method:", ('Manual Scoring', 'Automatic Scoring'), index=1)

        manual_scoring = {'Manual Scoring':'TRUE',
                          'Automatic Scoring':'FALSE'}[manual_scoring]


        # Date input for deadlines
        registration_deadline = st.date_input("Registration Deadline", min_value=datetime.date.today())
        final_submission_deadline = st.date_input("Final Submission Deadline", min_value=datetime.date.today())

        brief_description = st.text_area("Brief Description")

        # Number input for min/max number of students per team
        min_students = st.number_input("Min Number of Students per Team", min_value=1, max_value=100, step=1)
        max_students = st.number_input("Max Number of Students per Team", min_value=1, max_value=100, step=1)





        # Form submit button
        submit_button = st.form_submit_button(label='Create Battle')
        st.write(manual_scoring)

        if submit_button:

            battle_data = {'_BATTLE_NAME_': battle_name,
                            '_BATTLE_DESC_':brief_description,
                            '_TOURNAMENT_ID_':TournamentID,
                            '_BATTLE_REPO_':github_repo,
                            "_END_DATE_":final_submission_deadline,
                            '_REGISTRATION_DEADLINE_':registration_deadline,
                            '_MIN_GROUP_SIZE_':min_students,
                            '_MAX_GROUP_SIZE_':max_students,
                            '_MANUAL_SCORING_':manual_scoring}

            returned = st.session_state['user_object'].create_battle(battle_data)


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


