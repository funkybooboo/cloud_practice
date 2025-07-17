#!/usr/bin/env python3

import boto3
from mypy_boto3_ec2.client import EC2Client


def list_key_pairs() -> None:
    ec2: EC2Client = boto3.client("ec2")
    key_pairs = ec2.describe_key_pairs()["KeyPairs"]

    if not key_pairs:
        print("⚠️ No key pairs found.")
        return

    print("🗝️ Available EC2 key pairs:")
    for kp in key_pairs:
        print(f" - {kp['KeyName']}")


if __name__ == "__main__":
    list_key_pairs()
