from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from aws_cdk.aws_s3 import Bucket

from constructs import Construct


class PlatformshifthubStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        platformshiftbucket = Bucket(self, self.build_name("bucket"))

    def build_name(self, resource_name: str) -> str:
        return f"{self.stack_name}-{resource_name}"
