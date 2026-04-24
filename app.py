
import streamlit as st
# --- Deployment Health Check ---
try:
    import supabase
    import bcrypt
    import dlib
    import resemblyzer
    import librosa
except ImportError as e:
    st.error(f"❌ **Missing Dependency**: {e}")
    st.info("This usually happens if Streamlit Cloud is still installing your `requirements.txt`. Please wait a few minutes and **Reboot** the app if this persists.")
    st.stop()

from src.screen.home_screen import home_screen
from src.screen.teacher_screen import teacher_screen
from src.screen.student_screen import student_screen
from src.components.dialog_autoenroll import auto_enroll_dialog


def main():
    st.set_page_config(
        page_title='Snapclass - Making Attendence Faster Using AI',
        page_icon= "filled_logo.png"
    )
    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None

    # --- Handle ?join-code= URL param ---
    join_code = st.query_params.get('join-code')
    if join_code:
        # Always persist the join code in session so it survives reruns
        st.session_state['join_code'] = join_code
        # Force switch to student login mode if a join code is present
        if st.session_state['login_type'] != 'student':
            st.session_state['login_type'] = 'student'
            st.rerun()

    match st.session_state['login_type']:
        case 'teacher':
            teacher_screen()
        case 'student':
            student_screen()
        case None:
            home_screen()

    # After login: trigger auto-enroll dialog if join_code is active
    if (st.session_state.get('is_logged_in')
            and st.session_state.get('user_role') == 'student'
            and 'join_code' in st.session_state):
        auto_enroll_dialog(st.session_state['join_code'])
if __name__ == "__main__":
    main()