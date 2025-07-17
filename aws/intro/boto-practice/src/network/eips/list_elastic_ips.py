#!/usr/bin/env python3

import boto3
from mypy_boto3_ec2.client import EC2Client


def list_elastic_ips() -> None:
    ec2: EC2Client = boto3.client("ec2")
    response = ec2.describe_addresses()

    if not response["Addresses"]:
        print("⚠️ No Elastic IPs found.")
        return

    for addr in response["Addresses"]:
        public_ip = addr.get("PublicIp", "N/A")
        allocation_id = addr.get("AllocationId", "N/A")
        instance_id = addr.get("InstanceId", "unassociated")
        print(f"📡 {public_ip} | Allocation ID: {allocation_id} | Instance: {instance_id}")


if __name__ == "__main__":
    list_elastic_ips()
