import streamlit as st
import os

from supabase import create_client, Client

class SupabaseMock:
    is_mock = True
    def table(self, *args, **kwargs):
        st.error("🚨 **Database Connection Error**: The Supabase client is not initialized.")
        st.info("💡 **Fix**: Make sure you have added `SUPABASE_URL` and `SUPABASE_KEY` to the **Secrets** section in your Streamlit Cloud dashboard.")
        st.stop()

def init_supabase():
    try:
        if "SUPABASE_URL" not in st.secrets or "SUPABASE_KEY" not in st.secrets:
            return None
            
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        return None

supabase = init_supabase()
if supabase is None:
    supabase = SupabaseMock()