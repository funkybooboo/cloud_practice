#!/usr/bin/env python3

import sys
import boto3
from mypy_boto3_ec2.client import EC2Client
from botocore.exceptions import ClientError
from typing import List


def attach_s3_endpoint(vpc_id: str, route_table_ids: List[str], region: str = "us-east-1") -> None:
    ec2: EC2Client = boto3.client("ec2", region_name=region)

    try:
        response = ec2.create_vpc_endpoint(
            VpcEndpointType="Gateway",
            VpcId=vpc_id,
            ServiceName=f"com.amazonaws.{region}.s3",
            RouteTableIds=route_table_ids
        )

        endpoint_id = response["VpcEndpoint"]["VpcEndpointId"]
        print(f"✅ Created S3 VPC Endpoint: {endpoint_id}")

    except ClientError as e:
        print(f"❌ Error creating endpoint: {e.response['Error']['Message']}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: attach_s3_vpc_endpoint.py <vpc-id> <route-table-id-1> [<route-table-id-2> ...]")
        sys.exit(1)

    vpc_id_arg = sys.argv[1]
    route_table_ids_arg = sys.argv[2:]
    attach_s3_endpoint(vpc_id_arg, route_table_ids_arg)
