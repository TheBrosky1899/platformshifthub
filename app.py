#!/usr/bin/env python3
import os

import aws_cdk as cdk

from platformshifthub.platformshifthub_stack import PlatformshifthubStack

STAGE = os.getenv("STAGE", "dev")

app = cdk.App()
PlatformshifthubStack(
    app,
    "PlatformshifthubStack",
    env=cdk.Environment(
        account=os.getenv("AWS_ACCOUNT_ID"), region=os.getenv("AWS_REGION")
    ),
    stack_name=f"PlatformshifthubStack-{STAGE}".lower(),
)

cdk.Tags.of(app).add("stage", STAGE)
cdk.Tags.of(app).add("project", "platformshift")


app.synth()
