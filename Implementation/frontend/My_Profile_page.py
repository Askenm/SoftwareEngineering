import pandas as pd
from .util import button_call, dataframe_with_selections
import streamlit as st
from backend.backend import Student


def show():
        st.session_state['display_other_profile'] = st.session_state.to_dict().get('display_other_profile', False)
        if st.session_state['display_other_profile']:
            object = Student(st.session_state['selected_userID'])
            st.session_state['display_other_profile'] = False
        else:
            object = st.session_state['user_object']
        object.get_home_page()
        
        st.markdown(f"# 𖠌 {object.user_information['user_name']}")
        st.write('#')
        
        # TO DO: log in with a user account to check if this condition works
       
        if  st.session_state['role'] == 'Student':
            st.subheader ("🏅 Awarded Badges")
            st.dataframe(object.user_badges, hide_index=True)
        
            st.write('###')
            st.subheader ("🏆 Subscribed Tournaments")
        
            selection = dataframe_with_selections(object.user_information['user_tournaments'])

            if selection['selected_rows_indices'] != []:
                st.session_state['current_tournament_id'] = selection['selected_rows']['tid'].iloc[0]
                button_call("Tournament details")
        else:
            st.subheader ("🏆 Subscribed Tournaments")
        
            selection = dataframe_with_selections(object.user_information['user_tournaments'])

            if selection['selected_rows_indices'] != []:
                st.session_state['current_tournament_id'] = selection['selected_rows']['tid'].iloc[0]
                button_call("Tournament details")
            
