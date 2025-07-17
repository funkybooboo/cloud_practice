#!/usr/bin/env python3

import sys
import boto3
from mypy_boto3_ec2.client import EC2Client


def release_elastic_ip(allocation_id: str) -> None:
    ec2: EC2Client = boto3.client("ec2")
    ec2.release_address(AllocationId=allocation_id)
    print(f"🗑️ Released Elastic IP with Allocation ID: {allocation_id}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: release_elastic_ip.py <allocation-id>")
        sys.exit(1)

    release_elastic_ip(sys.argv[1])
