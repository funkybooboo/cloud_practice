#!/usr/bin/env python3

import sys
import boto3
from mypy_boto3_ec2.client import EC2Client


def create_security_group(name: str, description: str, vpc_id: str) -> None:
    ec2: EC2Client = boto3.client("ec2")

    try:
        response = ec2.create_security_group(
            GroupName=name,
            Description=description,
            VpcId=vpc_id
        )
        group_id = response["GroupId"]

        # Optional: Add SSH ingress rule
        ec2.authorize_security_group_ingress(
            GroupId=group_id,
            IpPermissions=[
                {
                    "IpProtocol": "tcp",
                    "FromPort": 22,
                    "ToPort": 22,
                    "IpRanges": [{"CidrIp": "0.0.0.0/0"}]
                }
            ]
        )

        print(f"✅ Created security group '{name}' with ID {group_id}")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: create_security_group.py <group-name> <description> <vpc-id>")
        sys.exit(1)

    create_security_group(sys.argv[1], sys.argv[2], sys.argv[3])
