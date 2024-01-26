import frontend.Create_tournament as Create_tournament
import streamlit as st


if __name__ == '__main__':
    st.session_state['user_id'] = 5
    
    Create_tournament.show()