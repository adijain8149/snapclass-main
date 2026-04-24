import streamlit as st
from src.database.db import create_subject, enroll_student_to_subject, create_attendance
from src.database.config import supabase
import time

@st.dialog("Quick Enrollment")
def auto_enroll_dialog(subject_code):
    st.markdown("""
    <style>
    div[data-testid="stDialog"] .stButton button, 
    div[data-testid="stDialog"] .stButton button p, 
    div[data-testid="stDialog"] .stButton button div[data-testid="stMarkdownContainer"], 
    div[data-testid="stDialog"] .stButton button span {
        color: white !important;
    }
    div[data-testid="stDialog"] button[aria-label="Close"] * {
        color: black !important;
        fill: black !important;
    }
    </style>
    """, unsafe_allow_html=True)
    student_id = st.session_state.student_data['student_id']
    
    res = supabase.table('subjects').select('subject_id , name').eq('subject_code', subject_code).execute()
    if not res.data:
        st.error('Subject code not found')
        if st.button('close'):
            if 'join_code' in st.session_state:
                del st.session_state['join_code']
            st.query_params.clear()
            st.rerun()
        return

    subject = res.data[0]

    check = supabase.table('subject_students').select('*').eq('subject_id', subject['subject_id']).eq('student_id', student_id).execute()
    if check.data:
        st.success(f"You are already enrolled in **{subject['name']}**")
        st.markdown("Would you like to **Verify Attendance** for today's session?")
        if st.button('Mark me Present ✅', type='primary', use_container_width=True):
            from datetime import datetime
            current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            create_attendance([{
                'student_id': student_id,
                'subject_id': subject['subject_id'],
                'timestamp': current_timestamp,
                'is_present': True
            }])
            st.toast("Attendance Verified!", icon="✅")
            if 'join_code' in st.session_state:
                del st.session_state['join_code']
            st.query_params.clear()
            time.sleep(2)
            st.rerun()
        
        if st.button('Not now', type='tertiary'):
            if 'join_code' in st.session_state:
                del st.session_state['join_code']
            st.query_params.clear()
            st.rerun()
        return

    st.markdown(f"Would you like to enroll in **{subject['name']}**?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button('No thanks'):
            if 'join_code' in st.session_state:
                del st.session_state['join_code']
            st.query_params.clear()
            st.rerun()
            

    with col2:
        if st.button('Yes enroll now!', type='primary', use_container_width=True):
            enroll_student_to_subject(student_id, subject_code)
            
            # Also mark attendance immediately upon enrollment
            from datetime import datetime
            current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            create_attendance([{
                'student_id': student_id,
                'subject_id': subject['subject_id'],
                'timestamp': current_timestamp,
                'is_present': True
            }])
            
            st.success('Joined & Attendance Verified!')
            if 'join_code' in st.session_state:
                del st.session_state['join_code']
            st.query_params.clear()
            time.sleep(2)
            st.rerun()