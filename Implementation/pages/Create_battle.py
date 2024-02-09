import datetime 
import streamlit as st
from menu import authenticated_menu

authenticated_menu()

with st.form(key='battle_form'):
    st.markdown("# Create New Battle")
    with st.expander("First time creating a battle? Check the repository template here!"):
        st.write("To create a battle, follow the instruction in the README in the Battle Template Repository.")
        st.link_button("Battle Template Link", "https://github.com/Askenm/battle_template") 


    st.session_state['user_object'].get_home_page()
    st.session_state['your_tournaments'] = st.session_state['user_object'].user_information['user_tournaments']

    YourTournaments = st.session_state['your_tournaments']['tournament_name'].values.tolist()

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


