import pandas as pd
from .util import button_call, dataframe_with_selections
import streamlit as st
from backend.backend import Tournament


def show():
    st.markdown(f"# ⛩️ Welcome back, {st.session_state.to_dict()['username']}")
    st.write('#')

    col1, col2 = st.columns(2)
    c3 = st.columns(1)

    st.session_state['user_object'].get_home_page()
    st.subheader ("🏆 My Tournmanents")
    

    selection = dataframe_with_selections(st.session_state['user_object'].user_information['user_tournaments'])

    if selection['selected_rows_indices'] != []:
        button_call("Tournament details")



    st.subheader ("🏆 My Battles")
    

    selection = dataframe_with_selections(st.session_state['user_object'].user_information['user_battles'])

    if selection['selected_rows_indices'] != []:
        button_call("Battle details")


    if st.session_state['role']=='Student':
        st.subheader ("🏆 My Badges")
    

        selection = dataframe_with_selections(st.session_state['user_object'].user_information['user_badges'])



    """
    with col1:

        st.subheader ("🏆 Ongoing Tournmanents")
        
        OngoingTournaments = Tournament(1)
        OngoingTournaments.get_tournament_page_info()
        OngoingTournamentsdf = OngoingTournaments.ongoing_tournaments
        
     #   df = pd.DataFrame(
     #   {
     #       "Tournament name": ["Basic", "Medium", "Advanced"],
     #       "Subscriber count": [100, 50, 75],
     #       "Creator": ["John", "Aske", "Lise"],
     #       "Battle Count": [100, 50, 75],
     #       "Tournament id": [100, 50, 75],

     #   }
     #   )

        selection = dataframe_with_selections(OngoingTournamentsdf)

        if selection['selected_rows_indices'] != []:
            st.session_state['Tournament_Id'] = selection['selected_rows']['tid'].iloc[0]
            button_call("Tournament details")

    
    with col2:
        st.subheader ("🏆 Upcoming Tournaments")
         
        UpcomingTournaments = Tournament(1)
        UpcomingTournaments.get_tournament_page_info()
        UpcomingTournamentsdf = UpcomingTournaments.upcoming_tournaments
         
      #  df = pd.DataFrame(
      #  {
      #      "Tournament name": ["Basic", "Medium", "Advanced"],
      #      "Subscriber count": [100, 50, 75],
      #      "Creator": ["John", "Aske", "Lise"],
      #      "Battle Count": [100, 50, 75],
      #      "Tournament id": [100, 200, 75],

      #  }
      #  )

        selection = dataframe_with_selections(UpcomingTournamentsdf,)

        if selection['selected_rows_indices'] != []:
            st.session_state['Tournament_Id'] = selection['selected_rows']['tid'].iloc[0]    #change 'tournament_name' tid 
            button_call("Tournament details")
            st.write(st.session_state['Tournament_Id'])

    
    with c3[0]:
        option = st.selectbox(
        "Search other users",
        ("Email", "Home phone", "Mobile phone"),
        index=None,
        placeholder="Select user profile...",
        )

        st.write('You selected:', option)
    """