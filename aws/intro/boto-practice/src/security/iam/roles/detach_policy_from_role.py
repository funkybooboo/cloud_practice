#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_iam.client import IAMClient


def detach_policy_from_role(role_name: str, policy_arn: str) -> None:
    iam: IAMClient = boto3.client("iam")
    try:
        iam.detach_role_policy(RoleName=role_name, PolicyArn=policy_arn)
        print(f"❌ Detached policy {policy_arn} from role {role_name}")
    except ClientError as e:
        print(f"❌ Error: {e.response['Error']['Message']}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: detach_policy_from_role.py <role-name> <policy-arn>")
        sys.exit(1)
    detach_policy_from_role(sys.argv[1], sys.argv[2])
