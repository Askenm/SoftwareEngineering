import pandas as pd
from .util import button_call, dataframe_with_selections,check_date_exceeds
import streamlit as st
from datetime import datetime


# SCAFFOLDING
if "current_battle_id" not in st.session_state.keys():
    st.session_state['current_battle_id'] = 29


def show():
    #hardcoded for testing
    #title should be fetched from DB of specific battle
    #need to figure out how to get st.switch_pages to pass on a battle ID to Battle_page.py

    if 'show_form' not in st.session_state:
        st.session_state.show_form = False


    if not st.session_state.show_form:
        st.session_state['user_object'].get_battle_page_info(st.session_state['current_battle_id'])
        st.session_state['free_group_members'] = st.session_state['user_object'].battle.unassigned_subs

        st.session_state['current_battle'] = st.session_state['user_object'].battle


        battle_user_data = st.session_state['current_battle'].battle_data
        battle_simple_data = st.session_state['current_battle'].battle_data_df

        st.markdown(f"# {battle_simple_data['battle_name'].values[0]}")
        st.write('#')

        

        c1, c2, = st.columns(2)
        c3, c4, = st.columns(2)
        c5 = st.columns(1)

        with c1:

            st.markdown("### Battle Description")
        
            st.write(f"{battle_simple_data['battle_description'].values[0]}")

            st.markdown("#### Battle Repository")
            st.write(f"{battle_simple_data['github_repo'].values[0]}")
            

        with c2:
            if battle_simple_data['registration_deadline'].values[0] > datetime.now().date() and \
            st.session_state['user_object'].uid not in st.session_state['current_battle'].participants \
            and st.session_state['role'] == 'Student':
                if st.button("💥 REGISTER"):

                    st.session_state.show_form = True

                    st.experimental_rerun()



        


        with c3:

            st.caption("Registration deadline")
            container = st.container(border=True)
            container.write(battle_simple_data['registration_deadline'].values[0])
            

        with c4:
            st.caption("Final Submission Deadline")
            container = st.container(border=True)
            container.write(battle_simple_data['end_date'].values[0])


        """
        with c3: 
            st.write('##')
            col1, col2 = st.columns(2)
            with col1:
                st.caption("Min number of Students per Team")
                container = st.container(border=True)
                container.write("2")
            with col2:
                st.caption("Max number of Students per Team")
                container = st.container(border=True)
                container.write("4")

        


        with c4:
            st.write('##')
            st.text(" ")
            st.text(" ")
            st.text(" ")
            st.text(" ")
            if st.button("💥 REGISTER"):
                st.toast('💥 THE BATTLE IS ON!! 💥')
        """  

        with c5[0]:


            st.markdown("### Battle Rankings")
            st.dataframe(battle_user_data['battle_rankings'])

            st.markdown("### Battle Submissions")
            st.dataframe(battle_user_data['submissions'])


            st.write('##')
            st.subheader ("𖠌 Battling Groups")
            st.dataframe(st.session_state['current_battle'].groups)

    else:

        st.markdown("### Group Registration")
        # Text input field
        group_name = st.text_input("Choose A Group Name")

        unames = st.session_state['free_group_members']['user_name'].values.tolist()
        # Multi-select list
        options = st.multiselect("Choose your group", 
                                 unames
                                 ,max_selections=3)


        selected_indexes = [unames.index(uname) for uname in options]
        userids = st.session_state['free_group_members'].iloc[selected_indexes]['uid'].values.tolist()
        userids.append(st.session_state['user_object'].uid)
        
        
        # Submit button
        if st.button('Submit'):
            
            st.session_state['current_battle'].join(user_ids=userids,
                                                        group_name=group_name)
            
            st.toast('💥 THE BATTLE IS ON!! 💥')
            st.balloons()

            #st.dataframe(st.session_state['free_group_members'].iloc[options])

            st.session_state['show_form']=False
            
            st.experimental_rerun()
