import streamlit as st
from src.database.db import create_subject, enroll_student_to_subject

@st.dialog("Enroll in Subject")
def enroll_dialog():
    st.write("Enter the subject code to enroll")
    subject_code = st.text_input("Subject Code", placeholder="e.g. CS101")
    
    if st.button("Enroll Now", type='primary', use_container_width=True):
        if subject_code:
            try:
                student_id = st.session_state.student_data['student_id']
                enroll_student_to_subject(student_id, subject_code)
                st.toast("Enrolled Successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a subject code")

@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    st.write("Enter the details of new subject")
    sub_id = st.text_input("subject code" , placeholder="C5101")
    sub_name = st.text_input("subject Name" , placeholder="Intoduction to computer science")
    sub_section = st.text_input("section", placeholder= "A")
    if st.button("create subject Now", type = 'primary', use_container_width=True):
        if sub_id and sub_name and sub_section:
            try:
                create_subject(sub_id , sub_name,sub_section, teacher_id)
                st.toast("subject created Successfully!")
                st.rerun()
            except Exception as e :
                st.error(f"error :{str(e)}")
            else:
                st.warning("please fil all the fields")
                

