from pages.util import dataframe_with_selections
import streamlit as st
from backend.backend import Tournament
from menu import menu_with_redirect  # Import the custom menu functions

menu_with_redirect()  

st.session_state['user_object'].get_home_page()

st.markdown(f"# ⛩️ Welcome back, {st.session_state['user_object'].user_information['user_name']}")
st.write('#')

c3 = st.columns(1)
c1 = st.columns(1) 
c2 = st.columns(1)

    
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
        st.switch_page("pages/My_Profile_page.py")

with c1[0]:
    st.write('#')
    st.subheader ("🏆 All ongoing Tournaments")
        
    OngoingTournaments = Tournament(1)
    OngoingTournaments.get_tournament_page_info()

    selection = dataframe_with_selections(OngoingTournaments.ongoing_tournaments)

    if selection['selected_rows_indices'] != []:
        st.session_state['current_tournament_id'] = selection['selected_rows']['tid'].iloc[0]    #change 'tournament_name' tid 
        st.switch_page("pages/Tournament_details.py")

if st.session_state['role']=='Student':
    c4 = st.columns(1)
    with c4[0]:
        st.subheader ("🏅 My Badges")


        selection = dataframe_with_selections(st.session_state['user_object'].user_information['user_badges'])

with c2[0]:
    st.subheader ("🏆 All upcoming Tournaments")
        
    UpcomingTournaments = Tournament(1)
    UpcomingTournaments.get_tournament_page_info()

    selection = dataframe_with_selections(UpcomingTournaments.upcoming_tournaments)

    if selection['selected_rows_indices'] != []:
        st.session_state['current_tournament_id'] = selection['selected_rows']['tid'].iloc[0]    #change 'tournament_name' tid 
        st.switch_page("pages/Tournament_details.py")




