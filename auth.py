from datetime import datetime, timedelta
import streamlit as st
import bcrypt

from backend.database import (
    init_db,
    get_user_by_username,
    get_all_users,
    create_user,
    set_user_password_and_clear_flag,
    update_login_failure,
    reset_login_failures,
    remove_user_by_id,
    count_admin_users,
)

DEFAULT_PASSWORD = "ChangeMe@123"
MAX_FAILED_ATTEMPTS = 5
LOCKOUT_MINUTES = 15


def _init_session():
    defaults = {
        "logged_in": False,
        "username": "",
        "role": "",
        "must_change_password": False,
        "user_id": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def _verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def _parse_lock_until(lock_until_raw):
    if not lock_until_raw:
        return None
    return datetime.fromisoformat(lock_until_raw)


def _is_user_locked(user):
    lock_until = _parse_lock_until(user["lock_until"])
    if not lock_until:
        return False, None
    now = datetime.utcnow()
    if now < lock_until:
        return True, lock_until
    return False, None


def _set_logged_in_user(user):
    st.session_state["logged_in"] = True
    st.session_state["username"] = user["username"]
    st.session_state["role"] = user["role"]
    st.session_state["must_change_password"] = bool(user["must_change_password"])
    st.session_state["user_id"] = user["id"]


def initialize_auth_system():
    init_db()


def login_page():
    initialize_auth_system()
    _init_session()

    st.title("🔐 Resume Parser — Login")
    st.markdown("Login with your account to access the dashboard.")
    st.caption("New users must change their default password at first login.")
    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("👤 Username")
        password = st.text_input("🔑 Password", type="password")

        if st.button("Login", use_container_width=True):
            user = get_user_by_username(username.strip())
            if not user or not user["is_active"]:
                st.error("Invalid username or password.")
                return

            is_locked, lock_until = _is_user_locked(user)
            if is_locked:
                st.error(f"Account locked. Try again after {lock_until.strftime('%H:%M')} UTC.")
                return

            if not _verify_password(password, user["password_hash"]):
                failed_attempts = int(user["failed_attempts"]) + 1
                lock_until_raw = None
                if failed_attempts >= MAX_FAILED_ATTEMPTS:
                    lock_until_raw = (datetime.utcnow() + timedelta(minutes=LOCKOUT_MINUTES)).isoformat()
                update_login_failure(user["id"], failed_attempts, lock_until_raw)
                st.error("Invalid username or password.")
                return

            reset_login_failures(user["id"])
            user = get_user_by_username(username.strip())
            _set_logged_in_user(user)
            st.rerun()


def logout():
    _init_session()
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    st.session_state["role"] = ""
    st.session_state["must_change_password"] = False
    st.session_state["user_id"] = None
    st.rerun()


def is_logged_in():
    _init_session()
    return st.session_state.get("logged_in", False)


def is_admin():
    return st.session_state.get("role") == "admin"


def must_change_password():
    return bool(st.session_state.get("must_change_password", False))


def enforce_access(admin_only=False, allow_password_change_page=False):
    if not is_logged_in():
        st.warning("Please login first.")
        st.stop()

    if must_change_password() and not allow_password_change_page:
        st.error("You must change your password before using the app.")
        st.info("Open the **Change Password** page from the sidebar.")
        st.stop()

    if admin_only and not is_admin():
        st.error("Access denied. Admin role required.")
        st.stop()


def render_sidebar():
    role = st.session_state.get("role", "user")
    with st.sidebar:
        st.markdown(f"👤 Logged in as **{st.session_state.get('username', '')}**")
        st.caption(f"Role: {role.title()}")
        if st.button("Logout"):
            logout()


def change_current_user_password(new_password: str):
    user_id = st.session_state.get("user_id")
    if not user_id:
        return False, "No active user session."

    if len(new_password) < 8:
        return False, "Password must be at least 8 characters."

    hashed = _hash_password(new_password)
    set_user_password_and_clear_flag(user_id, hashed)
    st.session_state["must_change_password"] = False
    return True, "Password changed successfully."


def get_users_for_admin():
    return get_all_users()


def create_user_by_admin(username: str, role: str):
    username = username.strip()
    if not username:
        return False, "Username is required."
    if role not in {"admin", "user"}:
        return False, "Role must be admin or user."

    password_hash = _hash_password(DEFAULT_PASSWORD)
    ok, err = create_user(username, password_hash, role, must_change_password=1)
    if not ok:
        return False, err
    return True, f"User created. Default password: {DEFAULT_PASSWORD}"


def force_reset_password_by_admin(user_id: int):
    users = get_all_users()
    target = next((u for u in users if u["id"] == user_id), None)
    if not target:
        return False, "User not found."

    password_hash = _hash_password(DEFAULT_PASSWORD)
    updated = set_user_password_and_clear_flag(user_id, password_hash, must_change_password=1)
    if not updated:
        return False, "Could not reset password. User may have been removed."
    return True, f"Password reset to default: {DEFAULT_PASSWORD}"


def remove_user_by_admin(current_user_id: int, target_user_id: int):
    if current_user_id == target_user_id:
        return False, "You cannot remove your own account."

    users = get_all_users()
    target = next((u for u in users if u["id"] == target_user_id), None)
    if not target:
        return False, "User not found."

    if target["role"] == "admin" and count_admin_users() <= 1:
        return False, "Cannot remove the last admin user."

    remove_user_by_id(target_user_id)
    return True, "User removed successfully."