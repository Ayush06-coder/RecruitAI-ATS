import streamlit as st

# Recruiter credentials
VALID_USERNAME = "Recruiter"
VALID_PASSWORD = "resumeparser123"

def login_page():
    st.title("🔐 Resume Parser — Login")
    st.markdown("Please login to access the recruiter dashboard.")
    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        username = st.text_input("👤 Username")
        password = st.text_input("🔑 Password", type="password")

        if st.button("Login", use_container_width=True):
            if username == VALID_USERNAME and password == VALID_PASSWORD:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.rerun()
            else:
                st.error("Invalid username or password.")

def logout():
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    st.rerun()

def is_logged_in():
    return st.session_state.get("logged_in", False)