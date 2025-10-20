import streamlit as st
from aws.s3 import S3Helper

st.title("Welcome to Platform Shift Hub") 

s3_helper = S3Helper(env_var="SPLASH_BUCKET")
