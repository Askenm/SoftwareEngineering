import pandas as pd
from .util import button_call, dataframe_with_selections
import streamlit as st
from backend.backend import Tournament

def show():
    print(st.session_state.to_dict()['Tournament_Id'])
    TournamentId = st.session_state.to_dict()['Tournament_Id']
    print(st.session_state.to_dict()['Tournament_Id'])
    ThisTournament = Tournament(TournamentId)
    ThisTournament.get_tournament_page_info()
    
    st.markdown(f"# 🏆 {ThisTournament.tournament_data_df['tournament_name'].iloc[0]}")
    st.write('#')

    c1, c2, = st.columns([3, 1])
    c3, c4, = st.columns(2)
    c5, c6, = st.columns(2)

    with c1:
        st.caption("Description")
        container = st.container(border=True)
        container.write(f"{ThisTournament.tournament_data_df['description'].iloc[0]}")

    with c2:
        st.caption("Subscription deadline")
        container = st.container(border=True)
        container.write(f"{ThisTournament.tournament_data_df['subscription_deadline'].iloc[0]}")

    with c3: 
        st.write('##')
        st.subheader ("⚔️ Ongoing Battles")
        
        # edit the query catalog and backend: new function to retrieve specifically ongoing battles from the related ones
        ThisTournamentBattlesdf = ThisTournament.related_battles
        
        df = pd.DataFrame(
        {
            "Tournament name": ["Basic", "Medium", "Advanced"],
            "Subscriber count": [100, 50, 75],
            "Creator": ["John", "Aske", "Lise"],
            "Battle Count": [100, 50, 75],
            "Battle_Id": [150, 50, 75],})

        selection = dataframe_with_selections(ThisTournamentBattlesdf)

    
        if selection['selected_rows_indices'] != []:
            st.session_state['Battle_Id'] = selection['selected_rows']['Battle_Id'].iloc[0]
            button_call("Battle details")

    with c4:
        st.write('##')
        st.subheader ("🚀 Ranking")
        
        ThisTournamentRankingdf = ThisTournament.tournament_rankings
        
        df = pd.DataFrame(
        {
            "Tournament name": ["Basic", "Medium", "Advanced"],
            "Subscriber count": [190, 50, 75],
            "Creator": ["John", "Aske", "Lise"],
            "Battle Count": [100, 50, 75],
            "User id": [150, 50, 75],})

        selection = dataframe_with_selections(ThisTournamentRankingdf)

        if selection['selected_rows_indices'] != []:
            st.session_state['User_Id'] = selection['selected_rows']['User id'].iloc[0]
            button_call("My Profile")
        
          
 
    with c5:
        st.write('##')
        st.subheader ("⚔️ Upcoming Battles")
        df = pd.DataFrame(
        {
            "Tournament name": ["Basic", "Medium", "Advanced"],
            "Subscriber count": [100, 50, 75],
            "Creator": ["John", "Aske", "Lise"],
            "Battle Count": [100, 56, 75],
            "Tournament id": [150, 50, 75],})

        selection = dataframe_with_selections(df)

        if selection['selected_rows_indices'] != []:
            st.session_state['Tournament_Id'] = selection['selected_rows']['Tournament id'].iloc[0]
            button_call("Battle details")
    



