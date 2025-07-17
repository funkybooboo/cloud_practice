#!/usr/bin/env python3

import boto3
from mypy_boto3_iam.client import IAMClient


def list_roles() -> None:
    iam: IAMClient = boto3.client("iam")
    paginator = iam.get_paginator("list_roles")
    print("🏷️ IAM Roles:")
    for page in paginator.paginate():
        for r in page["Roles"]:
            print(f" - {r['RoleName']} (ARN: {r['Arn']})")


if __name__ == "__main__":
    list_roles()
