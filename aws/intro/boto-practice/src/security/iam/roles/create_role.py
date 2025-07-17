#!/usr/bin/env python3

import sys
import json
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_iam.client import IAMClient


def create_role(role_name: str, service: str) -> None:
    """
    service: e.g. 'ec2.amazonaws.com' or 'lambda.amazonaws.com'
    """
    iam: IAMClient = boto3.client("iam")
    assume_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": service},
            "Action": "sts:AssumeRole"
        }]
    }

    try:
        resp = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(assume_policy)
        )
        print(f"✅ Created role: {role_name} (ARN: {resp['Role']['Arn']})")
    except ClientError as e:
        print(f"❌ Error creating role {role_name}: {e.response['Error']['Message']}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: create_role.py <role-name> <service-principal>")
        sys.exit(1)
    create_role(sys.argv[1], sys.argv[2])
