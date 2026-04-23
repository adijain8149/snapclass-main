import streamlit as st
def style_background_home():
    st.markdown("""
        <style>
            .stApp, [data-testid="stAppViewContainer"], .stApp > header {
                background-color: #5865F2 !important;
            }
            div[data-testid="column"], div[data-testid="stColumn"] {
                background-color: #E0E3FF !important;
                padding: 1rem !important;
                border-radius: 3.5rem !important;
            }
        </style>
""" , unsafe_allow_html = True)
def style_background_dashboard():
    st.markdown("""
        <style>
            .stApp, [data-testid="stAppViewContainer"] {
                background-color: #E0E3FF !important;
            }
        </style>
""" , unsafe_allow_html = True)
def style_base_layout():
#asdasd
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&family=Outfit:wght@100..900&display=swap');
            
            /* Hide Streamlit default components */
            #MainMenu, footer, header {
                visibility: hidden !important;
            }
            .block-container {
                padding-top: 1.5rem !important;
            }
            /* Adjust headings */
            h1 {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 3.5rem !important;
                line-height: 1.1 !important;
                margin-bottom: 0rem !important;
            }
            h2 {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 2.2rem !important;
                line-height: 0.9 !important;
                margin-bottom: 1rem !important;
                color: #2F3136 !important;
            }
            h3, h4, p, span {
                font-family: 'Outfit', sans-serif;
            }

            /* Customizing Text Inputs to perfectly force White background */
            div[data-testid="stTextInput"] div[data-baseweb="input"],
            div[data-testid="stTextInput"] div[data-baseweb="base-input"],
            div[data-testid="stTextInput"] input {
                border-radius: 1rem !important;
                border: none !important;
                background-color: #F8F9FA !important;
                color: #2F3136 !important;
                -webkit-text-fill-color: #2F3136 !important;
                caret-color: #2F3136 !important;
            }
            div[data-testid="stTextInput"] input {
                padding: 0.8rem 1rem !important;
                font-family: 'Outfit', sans-serif !important;
            }
            div[data-testid="stTextInput"] label {
                font-family: 'Outfit', sans-serif !important;
                font-weight: 600 !important;
                color: #2F3136 !important;
                padding-bottom: 0.5rem !important;
            }
            
            /* Password Toggle Eye Icon styling */
            div[data-testid="stTextInput"] div[data-baseweb="input"] button {
                background-color: #5865F2 !important;
                color: white !important;
                border-radius: 50% !important;
                width: 2.2rem !important;
                height: 2.2rem !important;
                margin-right: 0.3rem !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                transition: transform 0.2s ease;
            }
            div[data-testid="stTextInput"] div[data-baseweb="input"] button:hover {
                transform: scale(1.1);
            }
            div[data-testid="stTextInput"] div[data-baseweb="input"] button svg {
                fill: white !important;
                color: white !important;
            }

            /* Secondary buttons styling (Blue) */
            div.stButton > button[kind="secondary"], div.stButton > button[data-testid="baseButton-secondary"] {
                border-radius: 2rem !important;
                background-color: #5865F2 !important;
                color: white !important;
                padding: 0.6rem 1.5rem !important;
                font-family: 'Outfit', sans-serif !important;
                font-weight: 600 !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
                margin-top: 1rem !important;
            }
            div.stButton > button[kind="secondary"]:hover, div.stButton > button[data-testid="baseButton-secondary"]:hover {
                transform: scale(1.05) !important;
                background-color: #4752C4 !important;
            }

            /* Primary buttons styling (Pink) */
            div.stButton > button[kind="primary"], div.stButton > button[data-testid="baseButton-primary"] {
                border-radius: 2rem !important;
                background-color: #FF4B8B !important;
                color: white !important;
                padding: 0.6rem 1.5rem !important;
                font-family: 'Outfit', sans-serif !important;
                font-weight: 600 !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
                margin-top: 1rem !important;
            }
            div.stButton > button[kind="primary"]:hover, div.stButton > button[data-testid="baseButton-primary"]:hover {
                transform: scale(1.05) !important;
                background-color: #E63D7A !important;
            }

            /* Tertiary buttons styling (Black) */
            div.stButton > button[kind="tertiary"], div.stButton > button[data-testid="baseButton-tertiary"] {
                border-radius: 2rem !important;
                background-color: #000000 !important;
                color: white !important;
                padding: 0.6rem 1.5rem !important;
                font-family: 'Outfit', sans-serif !important;
                font-weight: 600 !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
                margin-top: 1rem !important;
            }
            div.stButton > button[kind="tertiary"]:hover, div.stButton > button[data-testid="baseButton-tertiary"]:hover {
                transform: scale(1.05) !important;
                background-color: #2F3136 !important;
            }

            /* Camera Input Styling */
            div[data-testid="stCameraInput"] button {
                border-radius: 1.5rem !important;
                background-color: #5865F2 !important;
                color: white !important;
                padding: 0.6rem 1.5rem !important;
                font-family: 'Outfit', sans-serif !important;
                font-weight: 600 !important;
                border: none !important;
                transition: transform 0.2s ease-in-out !important;
                margin-top: 0.5rem !important;
                width: 100% !important;
            }
            div[data-testid="stCameraInput"] button:hover {
                transform: scale(1.02) !important;
                background-color: #4752C4 !important;
            }
            div[data-testid="stCameraInput"] video, div[data-testid="stCameraInput"] img {
                border-radius: 1rem !important;
            }
            /* === Dialog / Popup Styling === */
            div[data-testid="stDialog"] > div > div {
                background-color: #FFFFFF !important;
                border-radius: 1.5rem !important;
                padding: 1.5rem !important;
            }
            div[data-testid="stDialog"] p,
            div[data-testid="stDialog"] span,
            div[data-testid="stDialog"] label,
            div[data-testid="stDialog"] h1,
            div[data-testid="stDialog"] h2,
            div[data-testid="stDialog"] h3 {
                color: #2F3136 !important;
            }
            div[data-testid="stDialog"] div[data-testid="stMarkdownContainer"] p {
                color: #2F3136 !important;
                font-family: 'Outfit', sans-serif !important;
                font-size: 1rem !important;
            }
        </style>
""", unsafe_allow_html=True)
