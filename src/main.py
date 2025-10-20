import streamlit as st
from auth.setup import setup_aws
from auth.login import login_user_with_google

from aws.s3 import S3Helper

st.set_page_config(page_title="Platform Shift Hub", page_icon="🚀", layout="wide")

st.title("Welcome to Platform Shift Hub")


def main():
    if user := login_user_with_google():
        st.write(user)
        setup_aws()

        s3_helper: S3Helper = st.session_state.s3_helper
        st.write(s3_helper.list_keys())


if __name__ == "__main__":
    main()
