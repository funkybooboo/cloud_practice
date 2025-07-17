#!/usr/bin/env python3

import boto3
from mypy_boto3_ec2.client import EC2Client


def create_igw() -> None:
    ec2: EC2Client = boto3.client("ec2")
    response = ec2.create_internet_gateway(
        TagSpecifications=[{
            "ResourceType": "internet-gateway",
            "Tags": [{"Key": "Name", "Value": "CustomIGW"}]
        }]
    )
    igw_id = response["InternetGateway"]["InternetGatewayId"]
    print(f"✅ Created Internet Gateway: {igw_id}")


if __name__ == "__main__":
    create_igw()
