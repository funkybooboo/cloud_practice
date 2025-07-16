#!/usr/bin/env python3

import sys
import boto3
from mypy_boto3_ec2.client import EC2Client


def stop_instance(instance_id: str) -> None:
    ec2: EC2Client = boto3.client("ec2")
    ec2.stop_instances(InstanceIds=[instance_id])
    print(f"⏹️ Stopped instance: {instance_id}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: stop_ec2_instance.py <instance-id>")
        sys.exit(1)

    stop_instance(sys.argv[1])
