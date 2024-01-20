import streamlit as st
from database_module import authenticate_user, create_user

def show():
    st.title("Tournament Page")