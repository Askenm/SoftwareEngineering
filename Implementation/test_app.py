import frontend.Create_tournament as Create_tournament
import frontend.Create_battle as Create_battle
import frontend.Create_badge as Create_badge
import frontend.Battle_details as Battle_details
import streamlit as st
from backend.backend import Student,Educator



if __name__ == '__main__':
    user_id = 5
    user_role = 'Educator'

    st.session_state['current_tournament_id'] = 16

    roles = {'Educator':Educator,
             'Student':Student}


    
    st.session_state['user_object'] = roles[user_role](user_id)

    #Create_tournament.show()
    Battle_details.show()