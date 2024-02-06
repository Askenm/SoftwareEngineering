from pages.util import dataframe_with_selections
import streamlit as st
from menu import authenticated_menu

authenticated_menu()
st.markdown("# ⚔️ My Battles")
st.write('#')

st.session_state['user_object'].get_home_page()

col1 = st.columns(1) 
col2 = st.columns(1)

with col1[0]:

    st.subheader ("⚔️ My ongoing Battles")
    selection = dataframe_with_selections(st.session_state['user_object'].user_information['user_ongoing_battles'])
    if selection['selected_rows_indices'] != []:
        st.session_state['current_battle_id'] = selection['selected_rows']['bid'].iloc[0]
        st.switch_page("pages/Battle_details.py")

with col2[0]:
    st.subheader ("⚔️ My upcoming Battles")
    print(st.session_state['user_object'].user_information['user_upcoming_battles'])
    selection = dataframe_with_selections(st.session_state['user_object'].user_information['user_upcoming_battles'],key_="UUT")

    if selection['selected_rows_indices'] != []:
        st.session_state['current_battle_id'] = selection['selected_rows']['bid'].iloc[0]
        st.switch_page("pages/Battle_details.py")

    