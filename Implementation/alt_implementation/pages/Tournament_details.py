from pages.util import dataframe_with_selections
import streamlit as st
import time
from menu import menu_with_redirect

menu_with_redirect()


print(f"{st.session_state['current_tournament_id']=}")
st.session_state['user_object'].get_tournament_page_info(st.session_state['current_tournament_id'])

st.session_state['current_tournament'] = st.session_state['user_object'].tournament
#   print(f"{st.session_state['user_object'].tournament.tournament_data_df=}")

st.session_state["affiliation"] = st.session_state['user_object'].get_affiliation()

st.markdown(f"# 🏆 {st.session_state['current_tournament'].tournament_data_df['tournament_name'].iloc[0]}")
st.write('#')

c1, c2, = st.columns([3, 1])
c4, c5 = st.columns(2)
c6, c7 = st.columns(2)


with c1:
    st.caption("Description")
    container = st.container(border=True)
    container.write(f"{st.session_state['current_tournament'].tournament_data_df['description'].iloc[0]}")

with c2:
    st.caption("Subscription deadline")
    container = st.container(border=True)
    container.write(f"{st.session_state['current_tournament'].tournament_data_df['subscription_deadline'].iloc[0]}")


if st.session_state["affiliation"] == "Not Subscribed":
    with c1:
        toggle = st.button("💥 SUBSCRIBE")
        if toggle:
            # Subscribe to tournament
            st.session_state['user_object'].subscribe()
            st.balloons()
            time.sleep(2)

            st.experimental_rerun()
        # SUBSCRIBE FUNCTIONALITY

elif st.session_state["affiliation"] == 'Owner':
    with c1:
        if st.button("💥 END TOURNAMENT"):
            st.session_state['current_tournament'].end_tournament()
            st.balloons()
            time.sleep(2)

            #st.experimental_rerun()
            
        # CANCEL FUNCTIONALITY

with c4: 
    st.write('##')
    st.subheader ("⚔️ Ongoing Battles")

    selection = dataframe_with_selections(st.session_state['current_tournament'].tournament_data['related_ongoing_battles'])
    
    if selection['selected_rows_indices'] != []:
        st.session_state['current_battle_id'] = selection['selected_rows']['bid'].iloc[0]
        #   print(st.session_state['current_battle_id'])
        st.switch_page("pages/Battle_details.py")


with c5: 
    st.write('##')
    st.subheader ("⚔️ Upcoming Battles")

    selection = dataframe_with_selections(st.session_state['current_tournament'].tournament_data['related_upcoming_battles'])
    
    if selection['selected_rows_indices'] != []:
        st.session_state['current_battle_id'] = selection['selected_rows']['bid'].iloc[0]
        st.switch_page("pages/Battle_details.py")


with c6:
    st.write('##')
    st.subheader ("🚀 Ranking")
    
    selection = dataframe_with_selections(st.session_state['current_tournament'].tournament_rankings)

    if selection['selected_rows_indices'] != []:
        st.session_state['user_Id'] = selection['selected_rows']['uid'].iloc[0]
        st.switch_page("pages/My_Profile_page.py")
    

with c7:
    st.write('##')
    st.subheader ("🏅 Badges")
    
    st.dataframe(st.session_state['current_tournament'].badges, hide_index=True)





