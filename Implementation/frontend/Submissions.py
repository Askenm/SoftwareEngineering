import pandas as pd
from .util import button_call, dataframe_with_selections
import streamlit as st

def show():
    # TODO : MISSING PROPER SUBMISSION ID FORWARDING WHEN PRESSING A SUBMISSION ON BATTLE PAGE AS AN EDUCATOR
    submission_id = 13
    # Read submission from DB

    st.session_state['current_submission'] = st.session_state['user_object'].get_submission(submission_id)

    
    st.markdown(f"# Submission by {st.session_state['current_submission']['group_name'].values[0]}")
    st.write('#')

    st.markdown("## Repository Link")
    st.markdown(f"*{st.session_state['current_submission']['group_repository'].values[0]}*")


    st.markdown("## Manual Score")
    score = st.slider("Submission Score",0,100,0)

    # Submit button
    if st.button('Submit'):
        
        st.session_state['user_object'].score_submission(score,st.session_state['current_submission']["smid"].values[0])
        
        st.toast('Submission Scored')
        st.balloons()
        
        st.experimental_rerun()

    # Upload information upon button press
    # Send notification