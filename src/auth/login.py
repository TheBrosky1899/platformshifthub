import streamlit as st

def login_user_with_google() -> st._UserInfoProxy:
    if not st.user.is_logged_in:
        if st.button("Log in"):
            st.login()
    else:
        with st.sidebar:
            if st.button("Log out"):
                st.logout()
        return st.user