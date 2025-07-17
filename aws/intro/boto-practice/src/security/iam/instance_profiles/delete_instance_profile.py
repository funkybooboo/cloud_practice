#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_iam.client import IAMClient

def delete_instance_profile(profile_name: str) -> None:
    iam: IAMClient = boto3.client("iam")
    try:
        iam.delete_instance_profile(InstanceProfileName=profile_name)
        print(f"🗑️ Deleted instance profile: {profile_name}")
    except ClientError as e:
        print(f"❌ Error deleting instance profile {profile_name}: {e.response['Error']['Message']}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: delete_instance_profile.py <profile-name>")
        sys.exit(1)
    delete_instance_profile(sys.argv[1])
