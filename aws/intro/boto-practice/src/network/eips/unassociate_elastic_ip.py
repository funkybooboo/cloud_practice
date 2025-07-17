#!/usr/bin/env python3

import sys
import boto3
from mypy_boto3_ec2.client import EC2Client
from botocore.exceptions import ClientError


def unassociate_elastic_ip(public_ip: str) -> None:
    ec2: EC2Client = boto3.client("ec2")

    try:
        # Lookup the association ID using the public IP
        response = ec2.describe_addresses(PublicIps=[public_ip])
        addresses = response.get("Addresses", [])
        if not addresses or "AssociationId" not in addresses[0]:
            print(f"❌ No associated Elastic IP found for {public_ip}")
            return

        association_id = addresses[0]["AssociationId"]

        # Disassociate the Elastic IP
        ec2.disassociate_address(AssociationId=association_id)
        print(f"🔌 Disassociated Elastic IP {public_ip} (AssociationId: {association_id})")

    except ClientError as e:
        print(f"❌ Error: {e.response['Error']['Message']}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: unassociate_elastic_ip.py <public-ip>")
        sys.exit(1)

    unassociate_elastic_ip(sys.argv[1])
