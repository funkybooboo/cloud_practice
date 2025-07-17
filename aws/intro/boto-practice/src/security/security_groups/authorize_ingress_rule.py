#!/usr/bin/env python3

import sys
import boto3
from mypy_boto3_ec2.client import EC2Client
from botocore.exceptions import ClientError


def authorize_ingress(group_id: str, port: int, cidr: str = "0.0.0.0/0") -> None:
    ec2: EC2Client = boto3.client("ec2")
    try:
        ec2.authorize_security_group_ingress(
            GroupId=group_id,
            IpPermissions=[
                {
                    "IpProtocol": "tcp",
                    "FromPort": port,
                    "ToPort": port,
                    "IpRanges": [{"CidrIp": cidr}]
                }
            ]
        )
        print(f"✅ Added rule to {group_id}: {port}/tcp from {cidr}")
    except ClientError as e:
        print(f"❌ Error: {e.response['Error']['Message']}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: authorize_ingress_rule.py <group-id> <port>")
        sys.exit(1)
    authorize_ingress(sys.argv[1], int(sys.argv[2]))
