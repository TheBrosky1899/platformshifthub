import logging
from typing import Optional, List, Dict, Any
import boto3
from botocore.exceptions import ClientError

# /Users/alexbreault/Documents/GitHub/platformshifthub/src/aws/s3.py

logger = logging.getLogger(__name__)


class S3Helper:
    """
    Small S3 helper that operates on a single bucket defined by the environment variable S3_BUCKET_NAME.
    """

    def __init__(
        self,
        *,
        bucket_name: str,
        s3_client: Optional[Any] = None,
        session: Optional[Any] = None,
    ) -> None:
        """
        Initialize the helper. Reads the bucket name from the given environment variable and
        stores it as self.bucket_name for use across methods.

        :param s3_client: optional boto3 S3 client to use (for testing or custom session)
        :param session: optional boto3 Session; if provided and s3_client is None, a client will be created
        :param env_var: environment variable name that contains the bucket name
        :raises ValueError: if the environment variable is not set
        """
        self.bucket_name = bucket_name

        # Priority of S3 client resolution:
        # 1. explicit s3_client parameter
        # 2. session parameter -> session.client("s3")
        # 3. default boto3.client("s3") which uses standard credential resolution
        if s3_client is not None:
            self.s3 = s3_client
        elif session is not None:
            # session may be a boto3.Session or a compatible object with client()
            self.s3 = session.client("s3")
        else:
            self.s3 = boto3.client("s3")

    def upload_file(
        self, local_path: str, key: str, extra_args: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Upload a file from disk to the bucket at the specified key.
        """
        try:
            self.s3.upload_file(
                local_path, self.bucket_name, key, ExtraArgs=extra_args or {}
            )
        except ClientError:
            logger.exception(
                "Failed to upload file %s to s3://%s/%s",
                local_path,
                self.bucket_name,
                key,
            )
            raise

    def upload_bytes(
        self, data: bytes, key: str, content_type: Optional[str] = None
    ) -> None:
        """
        Upload raw bytes to the bucket at the specified key.
        """
        extra_args = {"ContentType": content_type} if content_type else None
        try:
            self.s3.put_object(
                Bucket=self.bucket_name, Key=key, Body=data, **(extra_args or {})
            )
        except ClientError:
            logger.exception(
                "Failed to put object to s3://%s/%s", self.bucket_name, key
            )
            raise

    def download_file(self, key: str, local_path: str) -> None:
        """
        Download an object from the bucket to a local file path.
        """
        try:
            self.s3.download_file(self.bucket_name, key, local_path)
        except ClientError:
            logger.exception(
                "Failed to download s3://%s/%s to %s", self.bucket_name, key, local_path
            )
            raise

    def get_object_bytes(self, key: str) -> bytes:
        """
        Retrieve object content as bytes.
        """
        try:
            resp = self.s3.get_object(Bucket=self.bucket_name, Key=key)
            return resp["Body"].read()
        except ClientError:
            logger.exception("Failed to get object s3://%s/%s", self.bucket_name, key)
            raise

    def list_keys(
        self, prefix: Optional[str] = None, max_keys: int = 1000
    ) -> List[str]:
        """
        List object keys in the bucket optionally filtered by prefix.
        """
        kwargs: Dict[str, Any] = {"Bucket": self.bucket_name, "MaxKeys": max_keys}
        if prefix:
            kwargs["Prefix"] = prefix

        keys: List[str] = []
        try:
            resp = self.s3.list_objects_v2(**kwargs)
            for obj in resp.get("Contents", []):
                keys.append(obj["Key"])
            return keys
        except ClientError:
            logger.exception(
                "Failed to list objects in s3://%s with prefix=%s",
                self.bucket_name,
                prefix,
            )
            raise

    def delete_key(self, key: str) -> None:
        """
        Delete a single object key from the bucket.
        """
        try:
            self.s3.delete_object(Bucket=self.bucket_name, Key=key)
        except ClientError:
            logger.exception("Failed to delete s3://%s/%s", self.bucket_name, key)
            raise

    def head_object(self, key: str) -> Dict[str, Any]:
        """
        Retrieve metadata (HEAD) for an object.
        """
        try:
            return self.s3.head_object(Bucket=self.bucket_name, Key=key)
        except ClientError:
            logger.exception("Failed to head object s3://%s/%s", self.bucket_name, key)
            raise

    def generate_presigned_url(
        self, key: str, expires_in: int = 3600, method: str = "get_object"
    ) -> str:
        """
        Generate a presigned URL for the given object key. The method parameter should be an S3 client method
        name supported for presigning (commonly 'get_object' or 'put_object').
        """
        try:
            return self.s3.generate_presigned_url(
                ClientMethod=method,
                Params={"Bucket": self.bucket_name, "Key": key},
                ExpiresIn=expires_in,
            )
        except ClientError:
            logger.exception(
                "Failed to generate presigned url for s3://%s/%s", self.bucket_name, key
            )
            raise
