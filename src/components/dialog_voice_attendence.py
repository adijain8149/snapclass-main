import streamlit as st
import pandas as pd
from datetime import datetime
from src.database.config import supabase
from src.pipeline.voice_pipeline import process_bulk_audio

@st.dialog("Voice Attendance", width="large")
def voice_attendance_dialog(subject_id):
    st.write("Record audio of students saying I am present. Then AI will recognize the students")
    
    audio_file = st.audio_input("Record classroom audio")
    
    if "voice_results" not in st.session_state:
        st.session_state.voice_results = None

    if st.button("Analyze Audio", type="secondary", use_container_width=True):
        if audio_file:
            with st.spinner("Analyzing voice signatures..."):
                # 1. Get enrolled students and their voice embeddings
                response = supabase.table('subject_students').select("*, students(*)").eq('subject_id', subject_id).execute()
                enrolled_students = response.data
                
                if not enrolled_students:
                    st.warning("No students enrolled in this subject.")
                    return
                
                # Filter students with voice embeddings
                candidates = {
                    node['students']['student_id']: node['students']['voice_embedding']
                    for node in enrolled_students if node['students'].get('voice_embedding')
                }
                
                if not candidates:
                    st.error("None of the enrolled students have voice profiles registered.")
                    return
                
                # 2. Process audio
                audio_bytes = audio_file.getvalue()
                identified_results = process_bulk_audio(audio_bytes, candidates)
                
                # 3. Prepare results
                results = []
                attendance_to_log = []
                current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                
                for node in enrolled_students:
                    student = node['students']
                    sid = student['student_id']
                    score = identified_results.get(sid)
                    is_present = score is not None
                    
                    results.append({
                        "Name": student['name'],
                        "ID": sid,
                        "Source": f"{score:.4f}" if is_present else "-",
                        "Status": "✅ Present" if is_present else "❌ Absent"
                    })
                    
                    attendance_to_log.append({
                        'student_id': sid,
                        'subject_id': subject_id,
                        'timestamp': current_timestamp,
                        'is_present': bool(is_present)
                    })
                
                st.session_state.voice_results = {
                    "df": pd.DataFrame(results),
                    "log": attendance_to_log
                }
        else:
            st.warning("Please record audio first.")

    if st.session_state.voice_results:
        st.divider()
        st.write("Please review attendance before confirming.")
        st.dataframe(st.session_state.voice_results["df"], use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Discard", type="primary", use_container_width=True):
                st.session_state.voice_results = None
                st.rerun()
        with col2:
            if st.button("Confirm & Save", type="secondary", use_container_width=True):
                try:
                    if st.session_state.voice_results["log"]:
                        supabase.table('attendance_logs').insert(st.session_state.voice_results["log"]).execute()
                    st.toast("Voice attendance logged successfully!")
                    st.session_state.voice_results = None
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to log attendance: {str(e)}")
