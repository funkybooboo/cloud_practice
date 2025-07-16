#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_ec2.client import EC2Client


def reboot_instance(instance_id: str) -> None:
    ec2: EC2Client = boto3.client("ec2")
    try:
        ec2.reboot_instances(InstanceIds=[instance_id])
        print(f"🔁 Rebooted instance '{instance_id}'")
    except ClientError as e:
        print(f"❌ Failed to reboot instance: {e.response['Error']['Message']}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: reboot_ec2_instance.py <instance-id>")
        sys.exit(1)

    reboot_instance(sys.argv[1])
