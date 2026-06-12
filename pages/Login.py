import streamlit as st
from auth import login_page, is_logged_in
from styles import inject_css

st.set_page_config(page_title="Company Login", page_icon="🔐", layout="wide")
inject_css()

if is_logged_in():
    st.rerun()

login_page()