import os
import boto3
from aws.s3 import S3Helper
import streamlit as st


def setup_aws():
    # If AWS credentials are provided via environment variables, create a boto3 Session
    # and pass a client created from that session into the S3Helper. This allows the
    # app to use explicit credentials instead of the default credential resolution.
    aws_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_session_token = os.getenv("AWS_SESSION_TOKEN")

    if aws_key and aws_secret:
        # Create a session with provided credentials. If a session token is present include it.
        if aws_session_token:
            session = boto3.Session(
                aws_access_key_id=aws_key,
                aws_secret_access_key=aws_secret,
                aws_session_token=aws_session_token,
            )
        else:
            session = boto3.Session(
                aws_access_key_id=aws_key, aws_secret_access_key=aws_secret
            )

        s3_client = session.client("s3")
        st.session_state.s3_helper = S3Helper(
            s3_client=s3_client, env_var="SPLASH_BUCKET"
        )
    else:
        # Fall back to default boto3 client resolution (env, shared config, iam role, etc.)
        st.session_state.s3_helper = S3Helper(env_var="SPLASH_BUCKET")
