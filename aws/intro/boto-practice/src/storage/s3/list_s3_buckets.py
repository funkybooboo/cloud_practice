#!/usr/bin/env python3

import boto3
from mypy_boto3_s3.client import S3Client


def list_buckets() -> None:
    s3: S3Client = boto3.client("s3")
    response = s3.list_buckets()
    print("📦 Existing Buckets:")
    for bucket in response["Buckets"]:
        print(f" - {bucket['Name']}")


if __name__ == "__main__":
    list_buckets()
