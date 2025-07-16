#!/usr/bin/env python3

import os
import sys
import subprocess
import tempfile
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_s3.client import S3Client


def edit_s3_file(bucket: str, key: str) -> None:
    s3: S3Client = boto3.client("s3")

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        # Download
        s3.download_file(bucket, key, tmp_path)
        subprocess.run([os.environ.get("EDITOR", "vim"), tmp_path], check=True)

        # Re-upload
        s3.upload_file(tmp_path, bucket, key)
        print(f"✅ Edited and updated '{bucket}/{key}'")
    except ClientError as e:
        print(f"❌ S3 error: {e.response['Error']['Message']}")
    except subprocess.CalledProcessError:
        print("❌ Editor exited with an error.")
    finally:
        os.remove(tmp_path)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: edit_file_from_s3_bucket.py <bucket-name> <s3-key>")
        sys.exit(1)

    edit_s3_file(sys.argv[1], sys.argv[2])
