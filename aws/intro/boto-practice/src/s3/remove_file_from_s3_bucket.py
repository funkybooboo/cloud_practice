#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_s3.client import S3Client


def remove_file(bucket: str, key: str) -> None:
    s3: S3Client = boto3.client("s3")
    try:
        s3.delete_object(Bucket=bucket, Key=key)
        print(f"✅ Removed '{key}' from bucket '{bucket}'")
    except ClientError as e:
        print(f"❌ Deletion failed: {e.response['Error']['Message']}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: remove_file_from_s3_bucket.py <bucket-name> <s3-key>")
        sys.exit(1)

    remove_file(sys.argv[1], sys.argv[2])
