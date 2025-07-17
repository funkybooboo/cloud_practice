#!/usr/bin/env python3

import boto3
from mypy_boto3_iam.client import IAMClient

def list_instance_profiles() -> None:
    iam: IAMClient = boto3.client("iam")
    paginator = iam.get_paginator("list_instance_profiles")
    print("📦 IAM Instance Profiles:")
    for page in paginator.paginate():
        for ip in page["InstanceProfiles"]:
            print(f" - {ip['InstanceProfileName']} (ARN: {ip['Arn']})")

if __name__ == "__main__":
    list_instance_profiles()
