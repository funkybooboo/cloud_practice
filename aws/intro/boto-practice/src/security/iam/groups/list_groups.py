#!/usr/bin/env python3

import boto3
from mypy_boto3_iam.client import IAMClient


def list_groups() -> None:
    iam: IAMClient = boto3.client("iam")
    paginator = iam.get_paginator("list_groups")
    print("👥 IAM Groups:")
    for page in paginator.paginate():
        for g in page["Groups"]:
            print(f" - {g['GroupName']} (Created: {g['CreateDate']})")


if __name__ == "__main__":
    list_groups()
