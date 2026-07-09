import streamlit as st
from PIL import Image

@st.dialog("Capture or upload photos")
def add_photos_dialog():
    """
    Dialog for adding classroom photos via camera or file upload.
    """
    st.markdown("### 📸 Add Photos")
    st.markdown('<p style="color: #636E72; font-size: 0.9rem;">Add classroom snapshots to analyze attendance using AI.</p>', unsafe_allow_html=True)

    # Initialize tab state if not present
    if 'photo_tab' not in st.session_state:
        st.session_state.photo_tab = 'camera'

    # Use columns for a custom tab-like interface
    t1, t2 = st.columns(2)

    with t1:
        is_camera = st.session_state.photo_tab == 'camera'
        if st.button('📷 Camera', 
                     type="primary" if is_camera else "secondary", 
                     use_container_width=True,
                     key="dialog_camera_tab"):
            st.session_state.photo_tab = 'camera'
            st.rerun()

    with t2:
        is_upload = st.session_state.photo_tab == 'upload'
        if st.button('📁 Upload', 
                     type="primary" if is_upload else "secondary", 
                     use_container_width=True,
                     key="dialog_upload_tab"):
            st.session_state.photo_tab = 'upload'
            st.rerun()

    st.divider()

    # CAMERA TAB
    if st.session_state.photo_tab == 'camera':
        cam_photo = st.camera_input('Take Snapshot', key='dialog_cam')
        if cam_photo:
            # We append and then rerun to close the dialog and show it in the main gallery
            st.session_state.attendance_images.append(Image.open(cam_photo))
            st.toast('Photo Captured Successfully!', icon="📸")
            st.rerun()

    # UPLOAD TAB
    elif st.session_state.photo_tab == 'upload':
        uploaded_files = st.file_uploader(
            'Choose image files', 
            type=['jpg', 'png', 'jpeg'], 
            accept_multiple_files=True, 
            key='dialog_upload_widget'
        )
        
        if uploaded_files:
            st.info(f"Selected {len(uploaded_files)} photos.")
            if st.button('Add Selected Photos', type='primary', use_container_width=True):
                for f in uploaded_files:
                    st.session_state.attendance_images.append(Image.open(f))
                st.toast(f'Successfully added {len(uploaded_files)} photos!', icon="✅")
                st.rerun()

    # GALLERY PREVIEW (Inside Dialog)
    if st.session_state.attendance_images:
        st.divider()
        st.markdown(f"**Current Gallery ({len(st.session_state.attendance_images)})**")
        preview_cols = st.columns(5)
        for i, img in enumerate(st.session_state.attendance_images[-5:]): # Show last 5
            with preview_cols[i % 5]:
                st.image(img, use_container_width=True)
        if len(st.session_state.attendance_images) > 5:
            st.caption(f"...and {len(st.session_state.attendance_images) - 5} more")

    st.divider()
    if st.button('Done', type='secondary', use_container_width=True):
        st.rerun()


