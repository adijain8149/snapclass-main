import streamlit as st
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def header_home():
    img_path = "filled_logo.png"
    bin_str = get_base64_image(img_path)
    
    st.markdown(
        f"""
        <div style='display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom: 30px;margin-top:30px;'>
            <img src="data:image/png;base64,{bin_str}" width="200" style="object-fit: contain;" />
            <h1 style='text-align: center; color: #E0E3FF;'>SNAP<br/>CLASS</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
def header_dashboard():
    
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    
    st.markdown(f"""
        <div style="display:flex; align-items:center; justify-content:flex-start; gap:15px; margin-top:10px;">
            <img src='{logo_url}' style='height:80px;' />
            <h2 style='text-align:left; color:#5865F2 !important; font-family: "Climate Crisis", sans-serif; line-height: 0.9; margin: 0; font-size: 2.5rem !important;'>SNAP<br/>CLASS</h2>
        </div>
        """, unsafe_allow_html=True)
