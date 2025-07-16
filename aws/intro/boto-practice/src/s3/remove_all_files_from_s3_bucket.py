#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_s3.client import S3Client


def clear_bucket(bucket_name: str) -> None:
    s3: S3Client = boto3.client("s3")
    s3_resource = boto3.resource("s3")
    bucket = s3_resource.Bucket(bucket_name)

    try:
        print(f"🧹 Deleting all files from bucket '{bucket_name}'...")

        # Delete all objects
        deleted = bucket.objects.all().delete()

        # Delete all object versions (if versioning is enabled)
        try:
            deleted_versions = bucket.object_versions.all().delete()
        except ClientError as e:
            if e.response["Error"]["Code"] != "NoSuchBucket":
                print(f"⚠️ Could not delete object versions: {e.response['Error']['Message']}")

        print(f"✅ Cleared all files from '{bucket_name}'")
    except ClientError as e:
        print(f"❌ Error clearing bucket: {e.response['Error']['Message']}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: remove_all_files_from_s3_bucket.py <bucket-name>")
        sys.exit(1)

    clear_bucket(sys.argv[1])
