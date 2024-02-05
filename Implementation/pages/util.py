import streamlit as st
import numpy as np
from datetime import datetime

def dataframe_with_selections(df, key_= None):
    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)
    if key_ == None:
        edited_df = st.data_editor(
            df_with_selections,
            hide_index=True,
            column_config={"Select": st.column_config.CheckboxColumn(required=True)},
            disabled=df.columns,
        )
    else: 
        edited_df = st.data_editor(
            df_with_selections,
            hide_index=True,
            column_config={"Select": st.column_config.CheckboxColumn(required=True)},
            disabled=df.columns,
            key=key_
        )
    selected_indices = list(np.where(edited_df.Select)[0])
    selected_rows = df[edited_df.Select]
    return {"selected_rows_indices": selected_indices, "selected_rows": selected_rows}

def check_date_exceeds(comparison_date):
    """
    Check if the current date exceeds a given date in "yyyy-mm-dd" format.

    :param current_date: A date in "yyyy-mm-dd" format representing the current date.
    :param comparison_date: A date in "yyyy-mm-dd" format to compare against.
    :return: True if current_date exceeds comparison_date, False otherwise.
    """
    current_date = datetime.now()#.strftime("%Y-%m-%d")
    # Convert both dates from string to datetime objects
    #current_date_obj = datetime.strptime(current_date, "%Y-%m-%d")
    #comparison_date_obj = datetime.strptime(comparison_date, "%Y-%m-%d")

    # Compare the dates
    return #current_date_obj > comparison_date_obj


