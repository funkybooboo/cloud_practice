#!/usr/bin/env python3

import boto3
from mypy_boto3_ec2.client import EC2Client


def allocate_elastic_ip() -> None:
    ec2: EC2Client = boto3.client("ec2")
    response = ec2.allocate_address(Domain="vpc")
    print(f"✅ Allocated Elastic IP: {response['PublicIp']} | Allocation ID: {response['AllocationId']}")


if __name__ == "__main__":
    allocate_elastic_ip()
