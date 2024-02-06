import pandas as pd
from .util import button_call, dataframe_with_selections
import streamlit as st

def show():
    # TODO : MISSING PROPER SUBMISSION ID FORWARDING WHEN PRESSING A SUBMISSION ON BATTLE PAGE AS AN EDUCATOR
    # submission_id = 13
    # Read submission from DB
    # Highest score automatic 
    """
    Submissions in sidebar
    For each educator in drop down menu 
    show tope scoring submission for each group participating in battles 
    where you are the CREATOR and submission_deadline is passed
    """
    st.markdown("## Select submission to grade")
    submissions_list, submissions_dict = st.session_state['user_object'].get_submission_manuel_scoring(st.session_state['user_id'])
    selected_index = st.selectbox("Groups highest scoring submissions", submissions_list, index=0)

    if selected_index != submissions_list[0]:
        submission_id = submissions_dict[selected_index][0]
        st.write(f'{submission_id=}')
        st.session_state['current_submission'] = st.session_state['user_object'].get_submission(submission_id)

        st.markdown("### Repository Link")
        st.markdown(f"*{submissions_dict[selected_index][1]}*")


        st.markdown("### Manual Score")
        score = st.slider("Submission Score",0,100,0)

        # Submit button
        if st.button('Submit'):
            
            st.session_state['user_object'].score_submission(score,st.session_state['current_submission']["smid"].values[0])
            
            st.toast('Submission Scored')
            st.balloons()
            
            st.experimental_rerun()

    # Upload information upon button press
    # Send notification