import streamlit as st
import segno
import io

@st.dialog("Share Subject Code")
def share_subject_dialog(subject_name, subject_code):
    # Get domain from secrets or session state (defaults to snapclass-main if not set)
    if "BASE_URL" in st.secrets:
        app_domain = st.secrets["BASE_URL"]
    elif "custom_domain" in st.session_state:
        app_domain = st.session_state["custom_domain"]
    else:
        app_domain = "snap-class-main.streamlit.app"

    join_url = f"https://{app_domain}/?join-code={subject_code}"
    st.header("scan to join")
    qr = segno.make(join_url)
    out = io.BytesIO()
    qr.save(out , kind = 'png', scale = 10 , border = 1)
    col1 , col2 = st.columns(2)
    with col1:
        st.markdown('### copy Link')
        st.code(join_url, language="text")
        st.code(subject_code, language="text")
        st.info('Copy this link to share on WhatsApp or Email')
        
        # Allow user to quickly update the domain if it's wrong
        new_domain = st.text_input("App Domain (change this to yours):", value=app_domain, key="domain_input_field")
        if new_domain != app_domain:
            st.session_state["custom_domain"] = new_domain
            st.rerun()
    with col2:
        st.markdown('### scan to join')
        st.image(out.getvalue(), caption='QRCODE for class joining')











