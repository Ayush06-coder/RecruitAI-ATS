import streamlit as st
from auth import enforce_access, change_current_user_password, must_change_password
from styles import inject_css
from auth import render_sidebar

st.set_page_config(page_title="Change Password", page_icon="🔑", layout="wide")
inject_css()
render_sidebar()
enforce_access(allow_password_change_page=True)

st.title("🔑 Change Password")
# ... rest stays the same

if must_change_password():
    st.warning("First login detected. You must change your password to continue.")
else:
    st.caption("Use this page to update your account password.")

st.divider()

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Update Password", use_container_width=True):
        if not new_password or not confirm_password:
            st.error("Please fill both password fields.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        else:
            success, message = change_current_user_password(new_password)
            if success:
                st.success(message)
                st.info("You can now access all pages allowed for your role.")
            else:
                st.error(message)