#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_iam.client import IAMClient


def create_instance_profile(profile_name: str) -> None:
    iam: IAMClient = boto3.client("iam")
    try:
        iam.create_instance_profile(InstanceProfileName=profile_name)
        print(f"✅ Created instance profile: {profile_name}")
    except ClientError as e:
        print(f"❌ Error: {e.response['Error']['Message']}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: create_instance_profile.py <profile-name>")
        sys.exit(1)
    create_instance_profile(sys.argv[1])
