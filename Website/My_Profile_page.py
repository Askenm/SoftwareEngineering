import streamlit as st


st.markdown("# 𖠌 User_name")
st.write('#')

st.subheader ("🏅 Awarded Badges")
container = st.container(border=True)
container.write("test")

container = st.container(border=True)
container.write("test")

st.write('###')
st.subheader ("🏆 Subscribed Tournaments")

if st.button("Python Iteration tournament"):
        st.switch_page("Tournament_page.py")

if st.button("Python Iteration tournament", key=1):
        st.switch_page("Tournament_page.py")