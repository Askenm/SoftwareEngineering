import streamlit as st
from menu import authenticated_menu
authenticated_menu()

with st.form(key='badge_form'):
    
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
    selected_index = st.selectbox("Your Tournaments", 
                                YourTournaments)

    TournamentID = st.session_state['your_tournaments'][st.session_state['your_tournaments']['tournament_name'] == selected_index]['tid'].iloc[0]


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
        
    



