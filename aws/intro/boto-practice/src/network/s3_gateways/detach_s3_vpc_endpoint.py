#!/usr/bin/env python3

import sys
import boto3
from mypy_boto3_ec2.client import EC2Client
from botocore.exceptions import ClientError


def detach_s3_endpoint(endpoint_id: str) -> None:
    ec2: EC2Client = boto3.client("ec2")

    try:
        ec2.delete_vpc_endpoint(VpcEndpointIds=[endpoint_id])
        print(f"🗑️ Deleted S3 VPC Endpoint: {endpoint_id}")
    except ClientError as e:
        print(f"❌ Error deleting endpoint: {e.response['Error']['Message']}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: detach_s3_vpc_endpoint.py <vpc-endpoint-id>")
        sys.exit(1)

    detach_s3_endpoint(sys.argv[1])
