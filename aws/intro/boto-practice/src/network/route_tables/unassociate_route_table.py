#!/usr/bin/env python3

import sys
import boto3
from mypy_boto3_ec2.client import EC2Client
from botocore.exceptions import ClientError


def unassociate_route_table(association_id: str) -> None:
    ec2: EC2Client = boto3.client("ec2")

    try:
        # Disassociate the route table
        ec2.disassociate_route_table(AssociationId=association_id)
        print(f"🔄 Disassociated route table from subnet (AssociationId: {association_id})")

    except ClientError as e:
        print(f"❌ Error: {e.response['Error']['Message']}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: unassociate_route_table.py <association-id>")
        sys.exit(1)

    unassociate_route_table(sys.argv[1])
