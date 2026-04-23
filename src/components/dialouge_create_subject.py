import streamlit as st
from src.database.db import create_subject
@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    st.write("Enter the details of new subject")
    sub_id = st.text_input("subject code" , placeholder="C5101")
    sub_name = st.text_input("subject Name" , placeholder="Intoduction to computer science")
    sub_section = st.text_input("section", placeholder= "A")
    if st.button("create subject Now", type = 'primary', width='stretch'):
        if sub_id and sub_name and sub_section:
            try:
                create_subject(sub_id , sub_name,sub_section, teacher_id)
                st.toast("subject created Successfully!")
                st.rerun()
            except Exception as e :
                st.error(f"error :{str(e)}")
            else:
                st.warning("please fil all the fields")
                

