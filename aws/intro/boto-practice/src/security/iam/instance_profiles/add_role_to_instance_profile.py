#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_iam.client import IAMClient


def add_role_to_instance_profile(role_name: str, profile_name: str) -> None:
    iam: IAMClient = boto3.client("iam")
    try:
        iam.add_role_to_instance_profile(
            InstanceProfileName=profile_name,
            RoleName=role_name
        )
        print(f"✅ Added role '{role_name}' to instance profile '{profile_name}'")
    except ClientError as e:
        print(f"❌ Error: {e.response['Error']['Message']}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: add_role_to_instance_profile.py <role-name> <profile-name>")
        sys.exit(1)
    add_role_to_instance_profile(sys.argv[1], sys.argv[2])
