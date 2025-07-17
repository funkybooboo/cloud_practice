#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_s3.client import S3Client


def upload_file(bucket: str, key: str, file_path: str) -> None:
    s3: S3Client = boto3.client("s3")
    try:
        s3.upload_file(file_path, bucket, key)
        print(f"✅ Uploaded '{file_path}' to '{bucket}/{key}'")
    except ClientError as e:
        print(f"❌ Upload failed: {e.response['Error']['Message']}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: upload_file_to_s3_bucket.py <bucket-name> <s3-key> <local-file-path>")
        sys.exit(1)

    upload_file(sys.argv[1], sys.argv[2], sys.argv[3])
