#!/usr/bin/env python3

import sys
import boto3
from mypy_boto3_ec2.client import EC2Client


def delete_vpc_endpoint(endpoint_id: str) -> None:
    ec2: EC2Client = boto3.client("ec2")
    ec2.delete_vpc_endpoints(VpcEndpointIds=[endpoint_id])
    print(f"🗑️ Deleted VPC Endpoint: {endpoint_id}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: delete_vpc_endpoint.py <vpc-endpoint-id>")
        sys.exit(1)

    delete_vpc_endpoint(sys.argv[1])
