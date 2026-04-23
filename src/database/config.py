import streamlit as st
import os

try:
    from supabase import create_client, Client
except ImportError:
    pass

@st.cache_resource
def init_supabase():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"Failed to initialize Supabase. Make sure SUPABASE_URL and SUPABASE_KEY are added to .streamlit/secrets.toml. Error: {e}")
        return None

supabase = init_supabase()