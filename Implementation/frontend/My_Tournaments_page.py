import pandas as pd
from .util import button_call, dataframe_with_selections
import streamlit as st

def show():
    st.markdown("# 🏆 My Tournaments")
    st.write('#')

    st.session_state['user_object'].get_home_page()

    col1 = st.columns(1) 
    col2 = st.columns(1)
    

    with col1[0]:

        st.subheader ("🏆 My ongoing Tournmanents")
        
        selection = dataframe_with_selections(st.session_state['user_object'].user_information['user_ongoing_tournaments'])

        if selection['selected_rows_indices'] != []:
            st.session_state['current_tournament_id'] = selection['selected_rows']['tid'].iloc[0]
            print(f"prut {st.session_state['current_tournament_id']=}")
            button_call("Tournament details")

    with col2[0]:
        st.subheader ("🏆 My upcoming Tournaments")
        
        selection = dataframe_with_selections(st.session_state['user_object'].user_information['user_upcoming_tournaments'])

        if selection['selected_rows_indices'] != []:
            st.session_state['current_tournament_id'] = selection['selected_rows']['tid'].iloc[0]
            print(f"prut {st.session_state['current_tournament_id']=}")
            button_call("Tournament details")