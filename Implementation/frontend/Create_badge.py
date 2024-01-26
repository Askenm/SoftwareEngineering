import streamlit as st

def show():
    with st.form(key='badge_form'):
        st.markdown("# Create New Badge")

        # Text input for badge name
        badge_name = st.text_input("Badge Name")

        # Text area for description
        description = st.text_area("Description")

        # Text area for criteria
        criteria = st.text_area("Criteria")

        # Form submit button
        submit_button = st.form_submit_button(label='Create Badge')

        if submit_button:
            # Handle the form submission here
            st.write("Badge Name:", badge_name)
            st.write("Description:", description)
            st.write("Criteria:", criteria)



