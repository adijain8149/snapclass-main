import streamlit as st
import os

from supabase import create_client, Client

@st.cache_resource
def init_supabase():
    try:
        if "SUPABASE_URL" not in st.secrets or "SUPABASE_KEY" not in st.secrets:
            st.error("Missing Supabase credentials in Streamlit secrets.")
            return None
            
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"Failed to initialize Supabase: {e}")
        return None

supabase = init_supabase()