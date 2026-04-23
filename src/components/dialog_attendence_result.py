import streamlit as st
from src.database.config import supabase

@st.dialog("Attendance Reports", width="large")
def attendence_result_dialog(results_df, attendance_to_log):
    st.write("Please review attendance before confirming.")
    st.dataframe(results_df, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Discard", type="primary", use_container_width=True):
            st.session_state.attendance_images = []
            st.rerun()
            
    with col2:
        if st.button("Confirm & Save", type="secondary", use_container_width=True):
            try:
                if attendance_to_log:
                    supabase.table('attendance_logs').insert(attendance_to_log).execute()
                st.toast("Attendance logged successfully!")
                st.session_state.attendance_images = [] # Clear images on success
                st.rerun()
            except Exception as e:
                st.error(f"Failed to log attendance: {str(e)}")
