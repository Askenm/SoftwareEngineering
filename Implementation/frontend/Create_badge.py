import streamlit as st

def show():
    with st.form(key='badge_form'):
        # TODO : EVERYTHING GOOD
        
        st.markdown("# Create New Badge")

        # Text input for badge name
        badge_name = st.text_input("Badge Name")

        # Text area for description
        description = st.text_area("Description")

        rank = st.slider('Place top',1,10,1)

        num_battles = st.slider("In how many battles in this tournament?",0,15,0)

        st.session_state['user_object'].get_home_page()
        st.session_state['your_tournaments'] = st.session_state['user_object'].user_information['user_tournaments']

        YourTournaments = st.session_state['your_tournaments']['tournament_name'].values.tolist()
        # Multi-select list
        options = st.multiselect("Your Tournaments", 
                                 YourTournaments
                                 ,max_selections=1)


        selected_indexes = [YourTournaments.index(uname) for uname in options]
        TournamentID = st.session_state['your_tournaments'].iloc[selected_indexes]['tid'].values.tolist()[0]

        # Form submit button
        submit_button = st.form_submit_button(label='Create Badge')

        if submit_button:

            badge_data = {'_BADGE_NAME_': badge_name,
                            '_BADGE_DESC_':description,
                            "_RANK_":rank,
                            '_TOURNAMENT_ID_':TournamentID,
                            '_NUM_BATTLES_':num_battles}

            returned = st.session_state['user_object'].create_badge(st.session_state['current_tournament_id'],
                                                                    badge_data)


            # TODO : FIX ENTIRE GITHUB IMPLEMENTATION IN BACKEND MODULE
            if returned == 0:
                st.balloons()
            else:
                st.error(returned)
            
            
            """
            # Handle the form submission here
            st.write("Badge Name:", badge_name)
            st.write("Description:", description)
            st.write("Criteria:", criteria)
            """



