import streamlit as st
from ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.database.db import check_teacher_exists, create_teacher, teacher_login
from PIL import Image
import numpy as np
from src.pipeline.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipeline.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students, create_student,get_student_subject,get_student_attendance, unenroll_student_to_subject

import time
import hashlib
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card
from src.components.dialog_autoenroll import auto_enroll_dialog


def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']

    # Trigger Quick Enrollment popup if arriving via join link
    if 'join_code' in st.session_state:
        auto_enroll_dialog(st.session_state.join_code)
    c1, c2 = st.columns(2, vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        st.markdown(f"""<div style="color: #2F3136 !important; font-family: 'Outfit', sans-serif; text-align: left; font-size: 1.8rem; font-weight: 800; line-height: 1.2; margin-bottom: 10px;">Welcome, {student_data["name"]}</div>""", unsafe_allow_html=True)
        if st.button("Logout ⌘+Backspace", type='primary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state.clear()
            st.rerun()
    col1, col2 = st.columns([2, 1], vertical_alignment="center")
    with col1:
        st.markdown("<h1 style='color: #2F3136; margin: 0; padding-bottom: 20px;'>Your Enrolled<br>Subjects</h1>", unsafe_allow_html=True)
    with col2:
        if st.button('Enroll in Subject', type='secondary', use_container_width=True):
            enroll_dialog()
    st.divider()
    with st.spinner('loading your enrolled subjects ..'):
        subjects = get_student_subject(student_id)

        logs = get_student_attendance(student_id)
        stats_map = {}

        for log in logs:
            sid  = log['subject_id']
            if sid not   in stats_map :
                stats_map[sid]={"total":0 , "attended":0}
            stats_map[sid]['total']+=1
            if log.get('is_present'):
                stats_map[sid]['attended']+=1
        cols = st.columns(2)
        for i , sub_node in enumerate(subjects):
            sub = sub_node['subjects']
            sid = sub['subject_id']
            stats = stats_map.get(sid ,{"total":0 , "attended":0})
            def unenroll_button():
                st.markdown(f'''
                    <div class="unenroll-btn-container-{sid}"></div>
                    <style>
                        div.element-container:has(.unenroll-btn-container-{sid}) + div.element-container {{
                            margin-top: -35px !important;
                            margin-left: 15px !important;
                            position: relative !important;
                            z-index: 10 !important;
                        }}
                    </style>
                ''', unsafe_allow_html=True)
                if st.button("Unenroll from tihs course", key=f"unenroll_{sid}", type='tertiary', use_container_width=True, icon=':material/cancel_presentation:'):
                        unenroll_student_to_subject(student_id,sid)
                        st.toast(f"Unenrolled successfully from this course : {sub['name']}!")
                        st.rerun()
            
            with cols[i%2]:
                subject_card(
                    name = sub['name'],
                    code = sub['subject_code'],
                    section = sub ['section'],
                    stats = [
                        ('📅','Total', stats['total']),
                        ('✅','Attended', stats['attended'] )

                    ],footer_callback=unenroll_button

                )





def student_screen():
    # IF LOGGED IN: ONLY show the dashboard
    if "student_data" in st.session_state:
        style_background_dashboard()
        style_base_layout()
        student_dashboard()
        return

    # IF NOT LOGGED IN: Show Login UI
    style_background_dashboard()
    style_base_layout()

    # IF NOT LOGGED IN: Show Login UI
    style_background_dashboard()
    style_base_layout()

    if 'show_registration' not in st.session_state:
        st.session_state.show_registration = False
    if 'verification_msg' not in st.session_state:
        st.session_state.verification_msg = None

    # Top header row
    c1, c2 = st.columns([1, 1], vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        st.markdown('<div style="display: flex; justify-content: flex-end; width:100%;">', unsafe_allow_html=True)
        if st.button("Go back to Home Ctrl+Backspace", type="primary", key="loginbackbtn_login", shortcut="control+backspace"):
            st.session_state.clear()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Dynamic Header based on purpose
    if 'join_code' in st.session_state:
        # Try to fetch subject name for the header
        from src.database.config import supabase
        res = supabase.table('subjects').select('name').eq('subject_code', st.session_state.join_code).execute()
        subj_name = res.data[0]['name'] if res.data else "Subject"
        header_text = f"Attendance Verification: {subj_name}"
    else:
        header_text = "Login using FaceID"

    st.markdown(f"<h2 style='text-align:center; margin-top:20px; margin-bottom: 20px; font-family: \"Climate Crisis\", sans-serif; color: #2F3136;'>{header_text}</h2>", unsafe_allow_html=True)

    # Show join code banner if redirected from a share link
    if 'join_code' in st.session_state:
        st.info(f"📚 You're joining subject with code: **{st.session_state.join_code}** — Scan your face to enroll!")

    if st.session_state.verification_msg:
        st.info(st.session_state.verification_msg)

    # Camera Section
    photo_source = st.camera_input("Biometric Scan", label_visibility="collapsed")

    if 'last_photo_hash' not in st.session_state:
        st.session_state.last_photo_hash = None

    if photo_source:
        photo_bytes = photo_source.getvalue()
        current_hash = hashlib.md5(photo_bytes).hexdigest()
        
        if st.session_state.last_photo_hash != current_hash:
            st.session_state.last_photo_hash = current_hash
            img = np.array(Image.open(photo_source))

            try:
                st.markdown("""<style>[data-testid="stSpinner"] p { color: black !important; font-weight: bold; }</style>""", unsafe_allow_html=True)
                with st.spinner("Analyzing Face..."):
                    detected, all_ids, num_faces = predict_attendance(img)

                    if num_faces == 0:
                        st.error('Face not detected! Please ensure your face is clearly visible.')
                        st.session_state.show_registration = False
                        st.session_state.verification_msg = None
                    
                    elif num_faces > 1:
                        st.warning('Multiple faces detected!')
                        st.session_state.show_registration = False
                        st.session_state.verification_msg = None
                    
                    else:
                        if detected:
                            # Match Found
                            student_id = list(detected.keys())[0]
                            all_students = get_all_students()
                            student = next((s for s in all_students if s['student_id'] == student_id), None)
                            
                            if student:
                                st.session_state.student_data = student
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.show_registration = False
                                st.session_state.verification_msg = None

                                # Use a prominent success toast as the "pop up"
                                st.toast(f"🎉 Welcome Back, {student['name']}!", icon="👋")
                                st.success(f"Login Successful! Redirecting to dashboard...")

                                time.sleep(1.5)
                                st.rerun()
                        else:
                            # NO MATCH FOUND -> NEW STUDENT DETECTION
                            st.session_state.verification_msg = "Face not recognized! You appear to be a new student. Please register below."
                            st.session_state.show_registration = True
                            st.rerun()

            except Exception as e:
                st.error(f"Detection Error: {e}")
                st.session_state.show_registration = True

    # Manual Registration Toggle
    if not st.session_state.show_registration:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("New Student? Register Profile Manually", use_container_width=True):
                st.session_state.show_registration = True
                st.rerun()

    # Registration Section
    if st.session_state.show_registration:
        with st.container(border=True):
            st.markdown('<h2 style="color: #2F3136;">New Student Registration</h2>', unsafe_allow_html=True)
            new_name = st.text_input("Your Full Name", placeholder="Enter name to register", key="reg_name_input")

            st.markdown('<p style="font-weight: 600; font-size: 1.1rem; margin-top: 15px; color: black;">Optional: Voice Setup</p>', unsafe_allow_html=True)
            st.markdown('<p style="color: black; margin-bottom: 5px;">Follow phrase: "I am ready for attendance."</p>', unsafe_allow_html=True)
            audio_data = st.audio_input('Follow phrase: "I am ready for attendance."', label_visibility="collapsed", key="voice_reg_v2")

            if st.button('Register My Profile', type='primary', use_container_width=True):
                if not photo_source:
                    st.error("Please take a photo first using the camera above.")
                elif not new_name.strip():
                    st.warning("Please enter your full name.")
                else:
                    with st.spinner('Saving Profile...'):
                        photo_source.seek(0)
                        img_to_register = np.array(Image.open(photo_source))
                        encodings = get_face_embeddings(img_to_register)

                        if encodings:
                            face_emb = encodings[0].tolist()
                            voice_emb = None
                            if audio_data:
                                vb = audio_data.getvalue()
                                if vb: voice_emb = get_voice_embedding(vb)

                            resp = create_student(new_name.strip(), face_embedding=face_emb, voice_embedding=voice_emb)

                            if resp:
                                train_classifier()
                                st.session_state.student_data = resp[0]
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.show_registration = False
                                st.session_state.verification_msg = None

                                # Auto-enroll via join_code if present
                                if 'join_code' in st.session_state:
                                    try:
                                        from src.database.db import enroll_student_to_subject
                                        enroll_student_to_subject(resp[0]['student_id'], st.session_state.join_code)
                                        st.toast(f"✅ Enrolled in subject {st.session_state.join_code}!", icon="📚")
                                    except Exception as enroll_err:
                                        st.warning(f"Could not auto-enroll: {enroll_err}")
                                    del st.session_state['join_code']

                                st.success("Registered & Enrolled Successfully!")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("Database connection failed.")
                        else:
                            st.error("Face too blurry for registration. Try again.")
