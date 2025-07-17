#!/usr/bin/env python3

import boto3
from mypy_boto3_iam.client import IAMClient


def list_users() -> None:
    iam: IAMClient = boto3.client("iam")
    paginator = iam.get_paginator("list_users")
    print("🧑‍💼 IAM Users:")
    for page in paginator.paginate():
        for u in page["Users"]:
            print(f" - {u['UserName']} (Created: {u['CreateDate']})")


if __name__ == "__main__":
    list_users()
