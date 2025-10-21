import boto3
from aws.s3 import S3Helper
from helpers.modules import ModuleHelper
from helpers.pages import PageHelper
import streamlit as st


def setup_aws():
    # If AWS credentials are provided via environment variables, create a boto3 Session
    # and pass a client created from that session into the S3Helper. This allows the
    # app to use explicit credentials instead of the default credential resolution.
    aws_key = st.secrets["aws"]["AWS_ACCESS_KEY_ID"]
    aws_secret = st.secrets["aws"]["AWS_SECRET_ACCESS_KEY"]

    if aws_key and aws_secret:
        session = boto3.Session(
            aws_access_key_id=aws_key, aws_secret_access_key=aws_secret
        )

        s3_client = session.client("s3")
        return S3Helper(
            s3_client=s3_client, bucket_name=st.secrets["aws"]["SPLASH_BUCKET"]
        )
    else:
        # Fall back to default boto3 client resolution (env, shared config, iam role, etc.)
        st.session_state.s3_helper = S3Helper(
            bucket_name=st.secrets["aws"]["SPLASH_BUCKET"]
        )


def setup_helpers() -> st.navigation:
    # st.session_state.module_helper = ModuleHelper()
    page_helper = PageHelper()
    
    st.session_state.page_helper = page_helper
    
    return page_helper.page_navigation