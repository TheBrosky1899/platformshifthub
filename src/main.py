import streamlit as st
from auth.setup import setup_aws, setup_helpers
from auth.login import login_user_with_google
import json
import logging

logger = logging.getLogger(__name__)

st.set_page_config(page_title="Platform Shift Hub", page_icon="🚀", layout="wide")

st.title("Welcome to Platform Shift Hub")


def main():
    if user := login_user_with_google():
        
        allowed_users = json.load(open("src/admin/allowed_users.json"))
        if user.email not in allowed_users:
            st.error("You do not have permission to access this application.")
            st.stop()
        logger.info(f"User {user.email} logged in successfully.")
        # later todo: async
        setup_aws()
        setup_helpers()


if __name__ == "__main__":
    main()
