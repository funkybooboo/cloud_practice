#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_s3.client import S3Client


def download_file(bucket: str, key: str, destination: str) -> None:
    s3: S3Client = boto3.client("s3")
    try:
        s3.download_file(bucket, key, destination)
        print(f"✅ Downloaded '{bucket}/{key}' to '{destination}'")
    except ClientError as e:
        print(f"❌ Download failed: {e.response['Error']['Message']}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: download_file_from_s3_bucket.py <bucket-name> <s3-key> <destination-path>")
        sys.exit(1)

    download_file(sys.argv[1], sys.argv[2], sys.argv[3])
