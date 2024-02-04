import pandas as pd
from .util import button_call, dataframe_with_selections
import streamlit as st
from backend.backend import Tournament
import time

def show():
    # TODO : Again, mainly an ID forwarding issue
    """
    print(st.session_state.to_dict()['Tournament_Id'])
    TournamentId = st.session_state.to_dict()['Tournament_Id']
    print(st.session_state.to_dict()['Tournament_Id'])
    ThisTournament = Tournament(TournamentId)
    ThisTournament.get_tournament_page_info()
    """
    
    st.session_state['user_object'].get_tournament_page_info(st.session_state['current_tournament_id'])
    st.session_state['current_tournament'] = st.session_state['user_object'].tournament

    st.session_state["affiliation"] = st.session_state['user_object'].get_affiliation()

    st.markdown(f"# 🏆 {st.session_state['current_tournament'].tournament_data_df['tournament_name'].iloc[0]}")
    st.write('#')

    c1, c2, = st.columns([3, 1])
    c3, = st.columns(1)
    c4, = st.columns(1)
    c5, = st.columns(1)
    c6, = st.columns(1)

    with c1:
        st.caption("Description")
        container = st.container(border=True)
        container.write(f"{st.session_state['current_tournament'].tournament_data_df['description'].iloc[0]}")

    with c2:
        st.caption("Subscription deadline")
        container = st.container(border=True)
        container.write(f"{st.session_state['current_tournament'].tournament_data_df['subscription_deadline'].iloc[0]}")

    
    if st.session_state["affiliation"] == "Not Subscribed":
        with c4:
            if st.button("💥 SUBSCRIBE"):
                    
                    # Subscribe to tournament
                    st.session_state['user_object'].subscribe()
                    
                    st.balloons()

                    time.sleep(2)

                    st.experimental_rerun()
            # SUBSCRIBE FUNCTIONALITY
    
    elif st.session_state["affiliation"] == 'Owner':
        with c4:
            if st.button("💥 END TOURNAMENT"):
                st.session_state['current_tournament'].end_tournament()
                st.balloons()
                time.sleep(2)

                st.experimental_rerun()
                
            # CANCEL FUNCTIONALITY

    with c4: 
        st.write('##')
        st.subheader ("⚔️ Ongoing Battles")
        
        # edit the query catalog and backend: new function to retrieve specifically ongoing battles from the related ones
        ThisTournamentBattlesdf = st.session_state['current_tournament'].related_battles
        
        df = pd.DataFrame(
        {
            "Tournament name": ["Basic", "Medium", "Advanced"],
            "Subscriber count": [100, 50, 75],
            "Creator": ["John", "Aske", "Lise"],
            "Battle Count": [100, 50, 75],
            "Battle_Id": [150, 50, 75],})

        selection = dataframe_with_selections(ThisTournamentBattlesdf)
    
        if selection['selected_rows_indices'] != []:
            st.session_state['current_battle_id'] = selection['selected_rows']['Battle_Id'].iloc[0]
            print(st.session_state['current_battle_id'])
            button_call("Battle details")

    with c5:
        st.write('##')
        st.subheader ("🚀 Ranking")
        
        ThisTournamentRankingdf = st.session_state['current_tournament'].tournament_rankings
        
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
        
    
    with c6:
        st.write('##')
        st.subheader ("🚀 Badges")
        
        ThisTournamentBadgesf = st.session_state['current_tournament'].badges

        selection = dataframe_with_selections(ThisTournamentBadgesf)

        if selection['selected_rows_indices'] != []:
            st.session_state['User_Id'] = selection['selected_rows']['User id'].iloc[0]
            button_call("My Profile")
 

    



