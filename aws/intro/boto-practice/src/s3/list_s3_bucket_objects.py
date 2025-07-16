#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_s3.client import S3Client
from datetime import datetime


def list_objects(bucket_name: str, prefix: str = "") -> None:
    s3: S3Client = boto3.client("s3")

    try:
        paginator = s3.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

        print(f"📦 Objects in bucket '{bucket_name}' (prefix='{prefix}'):\n")

        found = False
        for page in pages:
            for obj in page.get("Contents", []):
                key = obj["Key"]
                size = obj["Size"]
                last_modified = obj["LastModified"].strftime("%Y-%m-%d %H:%M:%S")
                print(f" - {key}  ({size} bytes, modified {last_modified})")
                found = True

        if not found:
            print("⚠️  No objects found.")
    except ClientError as e:
        print(f"❌ Error: {e.response['Error']['Message']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: list_s3_bucket_objects.py <bucket-name> [prefix]")
        sys.exit(1)

    bucket = sys.argv[1]
    prefix = sys.argv[2] if len(sys.argv) > 2 else ""
    list_objects(bucket, prefix)
