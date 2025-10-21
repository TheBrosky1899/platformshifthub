import github
from github.Auth import Token
import streamlit as st

class BaseHelper:
    def __init__(self):
        self.git = github.Github(auth=Token(st.secrets["github"]["GIT_TOKEN"]))
        self.MODULE_SIR = "src/external_modules"