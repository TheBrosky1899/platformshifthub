import streamlit as st
from auth.setup import setup_aws
from auth.login import login_user_with_google

st.set_page_config(page_title="Platform Shift Hub", page_icon="🚀", layout="wide")

st.title("Welcome to Platform Shift Hub")


def main():
    if user := login_user_with_google():
        st.write(user)
        setup_aws()


if __name__ == "__main__":
    main()
