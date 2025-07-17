#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_iam.client import IAMClient


def attach_policy_to_role(role_name: str, policy_arn: str) -> None:
    iam: IAMClient = boto3.client("iam")
    try:
        iam.attach_role_policy(RoleName=role_name, PolicyArn=policy_arn)
        print(f"✅ Attached policy {policy_arn} to role {role_name}")
    except ClientError as e:
        print(f"❌ Error: {e.response['Error']['Message']}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: attach_policy_to_role.py <role-name> <policy-arn>")
        sys.exit(1)
    attach_policy_to_role(sys.argv[1], sys.argv[2])
