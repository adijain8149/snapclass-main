import streamlit as st
from PIL import Image

@st.dialog("Add Photos for Attendance")
def add_photos_dialog():
    st.write("Upload photos of your classroom or take a picture.")
    
    tab1, tab2 = st.tabs(["Upload Files", "Use Camera"])
    
    with tab1:
        uploaded_files = st.file_uploader("Choose images", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)
        if st.button("Add Uploaded Photos", type="primary", use_container_width=True):
            if uploaded_files:
                for file in uploaded_files:
                    img = Image.open(file)
                    st.session_state.attendance_images.append(img)
                st.toast(f"Added {len(uploaded_files)} photos!")
                st.rerun()
            else:
                st.warning("Please upload at least one photo.")

    with tab2:
        camera_photo = st.camera_input("Take a picture")
        if st.button("Add Camera Photo", type="primary", use_container_width=True):
            if camera_photo:
                img = Image.open(camera_photo)
                st.session_state.attendance_images.append(img)
                st.toast("Camera photo added!")
                st.rerun()
            else:
                st.warning("Please take a picture first.")
