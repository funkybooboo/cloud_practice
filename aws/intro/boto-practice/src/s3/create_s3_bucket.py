#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_s3.client import S3Client
from list_s3_buckets import list_buckets


def create_bucket(bucket_name: str, region: str = "us-east-1") -> None:
    s3: S3Client = boto3.client("s3", region_name=region)

    try:
        # Check if bucket exists (globally)
        s3.head_bucket(Bucket=bucket_name)
        print(f"⚠️  Bucket '{bucket_name}' already exists and is accessible.")
        return
    except ClientError as e:
        error_code = int(e.response["Error"]["Code"])
        if error_code == 404:
            pass  # Bucket does not exist, safe to create
        elif error_code == 403:
            print(f"❌ Bucket '{bucket_name}' exists but is owned by another account.")
            return
        else:
            print(f"❌ Unexpected error: {e}")
            return

    try:
        if region == "us-east-1":
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": region},
            )
        print(f"✅ Bucket '{bucket_name}' created in region '{region}'")
    except ClientError as e:
        print(f"❌ Error: {e.response['Error']['Message']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: create_bucket.py <bucket-name> [region]")
        sys.exit(1)

    bucket_name = sys.argv[1]
    region = sys.argv[2] if len(sys.argv) > 2 else "us-east-1"

    create_bucket(bucket_name, region)
    list_buckets()
