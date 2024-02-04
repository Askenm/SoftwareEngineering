import pandas as pd
from .util import button_call, dataframe_with_selections
import streamlit as st
from backend.backend import Tournament, Student

def show():
<<<<<<< HEAD
    # TODO : Maybe changes here? (Leonie)

    st.markdown(f"# ⛩️ Welcome back, {st.session_state.to_dict()['username']}")
    st.write('#')

    col1, col2 = st.columns(2)
    c3 = st.columns(1)

=======
    
>>>>>>> 68940ebcb2c07a25099e0111ff7309cbabf7397d
    st.session_state['user_object'].get_home_page()
   
    st.markdown(f"# ⛩️ Welcome back, {st.session_state['user_object'].user_information['user_name']}")
    st.write('#')
    
    

    c3 = st.columns(1)
    c1 = st.columns(1) 
    c2 = st.columns(1)
   
      
    # TO DO: User search function 
    with c3[0]:
        usernames, studentlist = st.session_state['user_object'].get_studentslist()
        option = st.selectbox(
        "𖠌 Visit students profiles",
        usernames,
        index=None,
        placeholder="Select user profile...",
        )

        st.write('You selected:', option)
        print(f"\n{option=}\n")
        if option != None:
            st.session_state['selected_userID'] = studentlist.loc[studentlist['user_name']==option,'uid'].iloc[0]
            print(f'{st.session_state["selected_userID"]=}')
            st.session_state['display_other_profile'] = True
            button_call("My Profile")
    
    with c1[0]:
        st.write('#')
        st.subheader ("🏆 All ongoing Tournaments")
         
        OngoingTournaments = Tournament(1)
        OngoingTournaments.get_tournament_page_info()

        selection = dataframe_with_selections(OngoingTournaments.ongoing_tournaments)

        if selection['selected_rows_indices'] != []:
            st.session_state['current_tournament_id'] = selection['selected_rows']['tid'].iloc[0]    #change 'tournament_name' tid 
            button_call("Tournament details")

    """

    if st.session_state['role']=='Student':
        st.subheader ("🏆 My Badges")
    

        selection = dataframe_with_selections(st.session_state['user_object'].user_information['user_badges'])

    """
    
    with c2[0]:
        st.subheader ("🏆 All upcoming Tournaments")
         
        UpcomingTournaments = Tournament(1)
        UpcomingTournaments.get_tournament_page_info()
 
        selection = dataframe_with_selections(UpcomingTournaments.upcoming_tournaments)

        if selection['selected_rows_indices'] != []:
            st.session_state['current_tournament_id'] = selection['selected_rows']['tid'].iloc[0]    #change 'tournament_name' tid 
            button_call("Tournament details")

    

 
    