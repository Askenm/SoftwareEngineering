from pages.util import dataframe_with_selections
import streamlit as st
from menu import menu_with_redirect  # Import the custom menu functions
import pandas as pd

menu_with_redirect() 


st.markdown("# 🏆 My Tournaments")
st.write('#')

st.session_state['user_object'].get_home_page()

col1 = st.columns(1) 
col2 = st.columns(1)


if st.session_state['role'] == 'Educator':
    with col1[0]:
        st.subheader ("🏆 My Tournmanents")
        educator_tournaments = st.session_state['user_object'].get_tournaments(st.session_state['user_object'].uid)

        if isinstance(educator_tournaments,type(pd.DataFrame())):
            selection = dataframe_with_selections(educator_tournaments)
            # Conditional on role: educators all tournament it has created, whose subscription deadline is in the past

            if selection['selected_rows_indices'] != []:
                st.session_state['current_tournament_id'] = selection['selected_rows']['tid'].iloc[0]
                st.page_link("pages/Tournament_details.py", label = "Tournament details")


else:
    with col1[0]:

        st.subheader ("🏆 My ongoing Tournmanents")
        selection = dataframe_with_selections(st.session_state['user_object'].user_information['user_ongoing_tournaments'])
        # Conditional on role: educators all tournament it has created, whose subscription deadline is in the past

        if selection['selected_rows_indices'] != []:
            st.session_state['current_tournament_id'] = selection['selected_rows']['tid'].iloc[0]
            st.page_link("pages/Tournament_details.py", label = "Tournament details")

    with col2[0]:
        st.subheader ("🏆 My upcoming Tournaments")
        
        selection = dataframe_with_selections(st.session_state['user_object'].user_information['user_upcoming_tournaments'])
        # Conditional on role: educators all tournament it has created, whose subscription deadline is in the future 

        if selection['selected_rows_indices'] != []:
            st.session_state['current_tournament_id'] = selection['selected_rows']['tid'].iloc[0]
            st.switch_page("pages/Tournament_details.py")