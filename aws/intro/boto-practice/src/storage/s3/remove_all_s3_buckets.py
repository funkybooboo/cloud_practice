#!/usr/bin/env python3

import boto3
from botocore.exceptions import ClientError
from mypy_boto3_s3.client import S3Client


def delete_all_buckets() -> None:
    s3: S3Client = boto3.client("s3")
    s3_resource = boto3.resource("s3")

    response = s3.list_buckets()
    buckets = response.get("Buckets", [])

    if not buckets:
        print("📭 No buckets to delete.")
        return

    for bucket in buckets:
        name = bucket["Name"]
        try:
            print(f"\n🧹 Emptying bucket '{name}'...")
            b = s3_resource.Bucket(name)
            b.objects.all().delete()
            b.object_versions.all().delete()

            print(f"🗑️ Deleting bucket '{name}'...")
            s3.delete_bucket(Bucket=name)
            print(f"✅ Deleted: {name}")
        except ClientError as e:
            print(f"❌ Failed to delete '{name}': {e.response['Error']['Message']}")


if __name__ == "__main__":
    confirm = input("⚠️ This will delete ALL accessible S3 buckets. Proceed? (y/N): ").strip().lower()
    if confirm == "y":
        delete_all_buckets()
    else:
        print("❎ Cancelled.")
