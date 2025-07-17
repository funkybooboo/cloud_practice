#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_iam.client import IAMClient

def remove_role_from_instance_profile(profile_name: str, role_name: str) -> None:
    iam: IAMClient = boto3.client("iam")
    try:
        iam.remove_role_from_instance_profile(
            InstanceProfileName=profile_name,
            RoleName=role_name
        )
        print(f"❌ Removed role '{role_name}' from instance profile '{profile_name}'")
    except ClientError as e:
        print(f"❌ Error removing role from instance profile: {e.response['Error']['Message']}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: remove_role_from_instance_profile.py <profile-name> <role-name>")
        sys.exit(1)
    remove_role_from_instance_profile(sys.argv[1], sys.argv[2])
