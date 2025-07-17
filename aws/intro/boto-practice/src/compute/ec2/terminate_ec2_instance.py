#!/usr/bin/env python3

import sys
import boto3
from mypy_boto3_ec2.client import EC2Client


def terminate_instance(instance_id: str) -> None:
    ec2: EC2Client = boto3.client("ec2")
    ec2.terminate_instances(InstanceIds=[instance_id])
    print(f"💀 Terminated instance: {instance_id}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: terminate_ec2_instance.py <instance-id>")
        sys.exit(1)

    terminate_instance(sys.argv[1])
