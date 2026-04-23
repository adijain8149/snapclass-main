import streamlit as st
import time
from ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.database.db import check_teacher_exists, create_teacher, teacher_login, get_teacher_subject,get_attendance_for_teacher
from src.components.dialouge_create_subject import create_subject_dialog
from src.components.subject_card import subject_card
from src.components.dialouge_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog
from src.pipeline.face_pipeline import predict_attendance
import numpy as np
from src.database.config import supabase
from datetime import datetime
import pandas as pd
from src.components.dialog_attendence_result import attendence_result_dialog
from src.components.dialog_voice_attendence import voice_attendance_dialog
def teacher_screen():
    style_background_dashboard()
    style_base_layout()
    if "teacher_data" in st.session_state:
        teacher_dashboard()
        return

    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=="login":
     teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()

def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    
    # Local CSS for specific text adjustments in Teacher Dashboard
    st.markdown("""
        <style>
            div[data-testid="stNotification"] p {
                color: #000000 !important;
            }
        </style>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2, vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        st.markdown(f"""<div style="color: #2F3136 !important; font-family: 'Outfit', sans-serif; text-align: left; font-size: 1.8rem; font-weight: 800; line-height: 1.2; margin-bottom: 10px;">Welcome, {teacher_data["name"]}</div>""", unsafe_allow_html=True)
        if st.button("Logout ⌘+Backspace", type="primary", key="loginbackbtn_login", shortcut="control+backspace"):
            st.session_state.clear()
            st.rerun()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'

    tab1, tab2, tab3 = st.columns(3)
    with tab1:
        type1 = "secondary" if st.session_state.current_teacher_tab == 'take_attendance' else "tertiary"
        if st.button('Take Attendance', type=type1, use_container_width=True, icon=':material/qr_code_scanner:'):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()

    with tab2:
        type2 = "secondary" if st.session_state.current_teacher_tab == 'manage_subjects' else "tertiary"
        if st.button('Manage Subjects', type=type2, use_container_width=True, icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab = 'manage_subjects'
            st.rerun()

    with tab3:
        type3 = "secondary" if st.session_state.current_teacher_tab == 'attendance_records' else "tertiary"
        if st.button('Attendance Records', type=type3, use_container_width=True, icon=':material/history:'):
            st.session_state.current_teacher_tab = 'attendance_records'
            st.rerun()
    
    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()

    elif st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()
        
    elif st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()

def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.header('Take AI Attendance')
    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subject(teacher_id)

    if not subjects:
        st.warning('You havent created any subjects yet! Please create one to begin!')
        return

    subject_options = {f"{s['name']} - {s['subject_code']}": s['subject_id'] for s in subjects}

    col1, col2 = st.columns([3, 1], vertical_alignment='bottom')

    with col1:
        selected_subject_label = st.selectbox('Select Subject', options=list(subject_options.keys()))

    with col2:
        if st.button('Add Photos', type='primary', icon=':material/photo_prints:', width='stretch'):
            add_photos_dialog()

        selected_subject_id = subject_options[selected_subject_label]

    st.divider()
    if st.session_state.attendance_images:
        st.header('Added Photos')
    gallery_cols = st.columns(4)

    for idx, img in enumerate(st.session_state.attendance_images):
        with gallery_cols[idx % 4]:
            st.image(img, width='stretch', caption=f'Photo {idx+1}')
    has_photos = bool(st.session_state.attendance_images)
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button('Clear all photos', width='stretch', type='tertiary', icon=':material/delete:', disabled= not has_photos):
            st.session_state.attendance_images = []
            st.rerun()

    with c2:
        
        if st.button('Run Face Analysis', width='stretch', type='secondary', icon=':material/analytics:', disabled= not has_photos ):
            with st.spinner('Deep scanning classroom photos...'):
                all_detected_ids = {}

                for idx, img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert('RGB'))
                    detected, _, _ = predict_attendance(img_np)

                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)

                            all_detected_ids.setdefault(student_id, []).append(f"Photo {idx+1}")

                enrolled_res = supabase.table('subject_students').select("*, students(*)").eq('subject_id', selected_subject_id).execute()
                enrolled_students = enrolled_res.data

                if not enrolled_students:
                    st.warning('No students enrolled in this course')
                else:
                    results, attendance_to_log = [], []

                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                    for node in enrolled_students:
                        student = node['students']
                        sources = all_detected_ids.get(int(student['student_id']), [])
                        is_present = len(sources) > 0

                        results.append({
                            "Name": student['name'],
                            "ID": student['student_id'],
                            "Source": ", ".join(sources) if is_present else "-",
                            "Status": "✅ Present" if is_present else "❌ Absent"
                        })

                        attendance_to_log.append({
                            'student_id': student['student_id'],
                            'subject_id': selected_subject_id,
                            'timestamp': current_timestamp,
                            'is_present': bool(is_present)
                        })
                    
                    attendence_result_dialog(pd.DataFrame(results),attendance_to_log)
    with c3:
        if st.button('Use Voice Attendance', type='primary', width='stretch', icon=':material/mic:'):
            voice_attendance_dialog(selected_subject_id)









def teacher_tab_manage_subjects():
    # Safely get teacher ID, checking for both 'teacher_id' and 'id' keys
    teacher_data = st.session_state.get('teacher_data', {})
    teacher_id = teacher_data.get('teacher_id') or teacher_data.get('id')
    
    if not teacher_id:
        st.error("Teacher ID not found in session state.")
        return
    col1 , col2 = st.columns([2, 1], vertical_alignment="center")
    with col1:
        st.markdown("<h1 style='color: #2F3136; margin: 0; padding-bottom: 20px;'>Manage<br>Subjects</h1>", unsafe_allow_html=True)
    with col2:
        if st.button('Create New Subject', use_container_width=True, type="primary"):
            create_subject_dialog(teacher_id)
            
    # Fetch and display subjects
    subjects = get_teacher_subject(teacher_id)
    if subjects:
        for sub in subjects:
            # Stats for the card
            card_stats = [
                ("👥", "Students", sub.get('total_students', 0)),
                ("⌚", "Classes", sub.get('total_classes', 0))
            ]
            
            # Render the card
            subject_card(
                name=sub['name'],
                code=sub.get('subject_code', 'N/A'),
                section=sub.get('section', 'N/A'),
                stats=card_stats
            )

            # Share Button - rendered directly to ensure visibility and primary styling
            button_label = f"Share Code: {sub['name']}"
            button_key = f"share_btn_{sub['subject_code']}"
            
            st.markdown(f'''
                <div class="share-btn-container-{sub['subject_code']}"></div>
                <style>
                    div.element-container:has(.share-btn-container-{sub['subject_code']}) + div.element-container {{
                        margin-top: -45px !important;
                        margin-left: 20px !important;
                        position: relative !important;
                        z-index: 10 !important;
                    }}
                </style>
            ''', unsafe_allow_html=True)
            if st.button(button_label, key=button_key, icon=":material/share:", use_container_width=False, type="primary"):
                st.info(f"Subject Code: {sub['subject_code']}")
                share_subject_dialog(sub['name'], sub['subject_code'])
    else:
        st.info("No Subjects Found. Create one above to get started.")

def teacher_tab_attendance_records():
    st.header('Attendance Records')
    teacher_id = st.session_state.teacher_data['teacher_id']
    records = get_attendance_for_teacher(teacher_id)
    if not records:
        return
    data = []

    for r in records:
        ts = r.get('timestamp')
        data.append({
            "ts_group": ts.split(".")[0] if ts else None,
            "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N/A",
            "Subject": r['subjects']['name'],
            "Subject Code": r['subjects']['subject_code'],
            "is_present": bool(r.get('is_present', False))
        })

    df = pd.DataFrame(data)

    summary = (
        df.groupby(['ts_group', 'Time', 'Subject', 'Subject Code'])
    .agg(
        Present_Count = ('is_present', 'sum'),
        Total_Count = ('is_present', 'count')
    ).reset_index()
)

    summary['Attendance Stats'] = (
    "✅ " + summary['Present_Count'].astype(str) + " /"
    + summary['Total_Count'].astype(str) + ' Students'
)

    display_df = ( summary.sort_values(by='ts_group' ,ascending=False)
    [['Time', 'Subject', 'Subject Code', 'Attendance Stats']]
)

    st.dataframe(display_df, width = 'stretch' , hide_index = True)
    
def login_teacher(username ,password):
    if not username or not password:
        return False
    teacher = teacher_login(username, password)
    if teacher :
        st.session_state.user_role = "teacher"
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True

def teacher_screen_login():
    c1, c2 = st.columns(2, vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        st.markdown('<div style="display: flex; justify-content: flex-end; width:100%;">', unsafe_allow_html=True)
        if st.button("Go back to Home", type="primary", key="loginbackbtn_login"):
            st.session_state['login_type'] = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
            
    st.markdown("<h2 style='text-align: center; color: #2F3136; margin-top:2rem;'>Login using password</h2>", unsafe_allow_html=True)
    st.write("")
    
    teacher_username = st.text_input("Enter username")
    teacher_pass = st.text_input("Enter password", type="password")
    
    st.divider()
    
    btn1, btn2 = st.columns(2)
    with btn1:
        if st.button('Login', type='primary', icon=':material/login:', use_container_width=True):
            if login_teacher(teacher_username , teacher_pass):
                st.toast("Welcome back!", icon="👋")
                time.sleep(1)
                st.rerun()
            else :
                st.error("Invalid username and password combo")
    with btn2:
        if st.button('Register Instead', type="secondary", icon=':material/person_add:', use_container_width=True):
            st.session_state.teacher_login_type = 'register'
            st.rerun()

def register_teacher(teacher_username,teacher_name,teacher_pass,teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass:
        return False , "all fields are required!"
    if check_teacher_exists(teacher_username):
        return False , "username already taken "
    if teacher_pass != teacher_pass_confirm:
        return False , "password dosen't match"
    try:
        create_teacher(teacher_username,teacher_pass,teacher_name)
        return True , "sucessfully created ! login now "
    except Exception as e :
        return False , "unexpected Error!"

def teacher_screen_register():
    c1, c2 = st.columns(2, vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        st.markdown('<div style="display: flex; justify-content: flex-end; width:100%;">', unsafe_allow_html=True)
        if st.button("Go back to Home", type="primary", key="loginbackbtn_register"):
            st.session_state['login_type'] = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
            
    st.markdown("<h2 style='text-align: center; color: #2F3136; margin-top:2rem;'>Register your teacher profile</h2>", unsafe_allow_html=True)
    st.write("")
    
    teacher_username = st.text_input("Enter username")
    teacher_name = st.text_input("Enter name")
    teacher_pass = st.text_input("Enter password", type="password")
    teacher_pass_confirm = st.text_input("confirm password", type="password")
    
    st.divider()
    
    btn1, btn2 = st.columns(2)
    with btn1:
        if st.button('Register', type='primary', icon=':material/login:', use_container_width=True):
            success, massage = register_teacher(teacher_username,teacher_name,teacher_pass,teacher_pass_confirm)
            if success:
                st.success(massage)
                time.sleep(2)
                st.session_state.teacher_login_type = "login"
                st.rerun()
            else :
                st.error(massage)
    with btn2:
       if st.button('login Register Instead', type="secondary", icon=':material/person_add:', use_container_width=True):
            st.session_state.teacher_login_type="login"
            st.rerun()