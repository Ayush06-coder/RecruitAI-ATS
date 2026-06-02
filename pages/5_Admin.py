import streamlit as st
import pandas as pd

from auth import (
    enforce_access,
    render_sidebar,
    get_users_for_admin,
    create_user_by_admin,
    force_reset_password_by_admin,
    remove_user_by_admin,
)

st.set_page_config(
    page_title="Admin Panel",
    page_icon="🛠️",
    layout="wide"
)

enforce_access(admin_only=True)
render_sidebar()

st.title("🛠️ Admin Panel")
st.caption("Create users, reset passwords, and remove accounts.")
st.divider()

st.subheader("Add New User")
col1, col2 = st.columns(2)
with col1:
    new_username = st.text_input("Username")
with col2:
    new_role = st.selectbox("Role", ["user", "admin"])

if st.button("Create User"):
    ok, message = create_user_by_admin(new_username, new_role)
    if ok:
        st.success(message)
        st.rerun()
    else:
        st.error(message)

st.divider()
st.subheader("Manage Existing Users")

users = get_users_for_admin()
if not users:
    st.info("No users found.")
    st.stop()

df = pd.DataFrame([
    {
        "ID": u["id"],
        "Username": u["username"],
        "Role": u["role"],
        "Must Change Password": "Yes" if u["must_change_password"] else "No",
        "Failed Attempts": u["failed_attempts"],
        "Active": "Yes" if u["is_active"] else "No",
    }
    for u in users
])
df.index = range(1, len(df) + 1)
df.index.name = "No."
st.dataframe(df, use_container_width=True)

st.divider()

user_options = {f"{u['id']} - {u['username']} ({u['role']})": u["id"] for u in users}
selected_label = st.selectbox("Select user", options=list(user_options.keys()))
selected_user_id = user_options[selected_label]
current_user_id = st.session_state.get("user_id")

col_a, col_b = st.columns(2)
with col_a:
    if st.button("Force Password Reset"):
        ok, message = force_reset_password_by_admin(selected_user_id)
        if ok:
            st.success(message)
            st.rerun()
        else:
            st.error(message)

with col_b:
    if st.button("Remove User"):
        ok, message = remove_user_by_admin(current_user_id, selected_user_id)
        if ok:
            st.success(message)
            st.rerun()
        else:
            st.error(message)
