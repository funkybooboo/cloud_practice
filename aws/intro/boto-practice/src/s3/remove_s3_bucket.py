#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_s3.client import S3Client


def delete_bucket(bucket_name: str) -> None:
    s3: S3Client = boto3.client("s3")

    try:
        # Must delete all objects before deleting bucket
        print(f"🧹 Emptying bucket '{bucket_name}'...")
        s3_resource = boto3.resource("s3")
        bucket = s3_resource.Bucket(bucket_name)
        bucket.objects.all().delete()
        bucket.object_versions.all().delete()

        print(f"🗑️ Deleting bucket '{bucket_name}'...")
        s3.delete_bucket(Bucket=bucket_name)
        print(f"✅ Bucket '{bucket_name}' deleted.")
    except ClientError as e:
        print(f"❌ Error: {e.response['Error']['Message']}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: remove_s3_bucket.py <bucket-name>")
        sys.exit(1)

    delete_bucket(sys.argv[1])
