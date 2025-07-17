#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_s3.client import S3Client


def print_s3_file(bucket: str, key: str) -> None:
    s3: S3Client = boto3.client("s3")

    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        body = response["Body"].read().decode("utf-8")
        print(f"📄 Contents of '{bucket}/{key}':\n")
        print(body)
    except ClientError as e:
        print(f"❌ Error reading file: {e.response['Error']['Message']}")
    except UnicodeDecodeError:
        print("❌ File is not UTF-8 encoded or contains binary data.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: print_file_from_s3_bucket.py <bucket-name> <s3-key>")
        sys.exit(1)

    print_s3_file(sys.argv[1], sys.argv[2])
