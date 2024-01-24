import streamlit as st

def show():
    st.title("My profile")

    print(f'{st.session_state.to_dict().items()=}')

    # Query for badges for st.session_state['username']
    # Columns: Name, Date, Description 

    # Query for the users active torunaments
    # Columns: Name, Date, Description 

    # Query for the users active battles 
    # Columns: Name, Date, Description 