#!/usr/bin/env python3

import sys
import boto3
from mypy_boto3_ec2.client import EC2Client


def create_s3_vpc_endpoint(vpc_id: str, route_table_ids: list[str]) -> None:
    ec2: EC2Client = boto3.client("ec2")

    response = ec2.create_vpc_endpoint(
        VpcId=vpc_id,
        ServiceName=f"com.amazonaws.{ec2.meta.region_name}.s3",
        RouteTableIds=route_table_ids,
        VpcEndpointType="Gateway",
        TagSpecifications=[{
            "ResourceType": "vpc-endpoint",
            "Tags": [{"Key": "Name", "Value": "S3GatewayEndpoint"}]
        }]
    )

    endpoint_id = response["VpcEndpoint"]["VpcEndpointId"]
    print(f"✅ Created S3 VPC Endpoint: {endpoint_id}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: create_s3_vpc_endpoint.py <vpc-id> <route-table-id1> [<route-table-id2> ...]")
        sys.exit(1)

    vpc_id = sys.argv[1]
    route_table_ids = sys.argv[2:]
    create_s3_vpc_endpoint(vpc_id, route_table_ids)
