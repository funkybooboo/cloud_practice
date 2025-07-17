#!/usr/bin/env python3

import sys
import boto3
from mypy_boto3_ec2.client import EC2Client


def associate_elastic_ip(instance_id: str, allocation_id: str) -> None:
    ec2: EC2Client = boto3.client("ec2")

    # Find the instance's primary network interface
    reservations = ec2.describe_instances(InstanceIds=[instance_id])["Reservations"]
    network_interface_id = reservations[0]["Instances"][0]["NetworkInterfaces"][0]["NetworkInterfaceId"]

    ec2.associate_address(
        AllocationId=allocation_id,
        NetworkInterfaceId=network_interface_id
    )
    print(f"📡 Elastic IP associated with instance {instance_id} (ENI: {network_interface_id})")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: associate_elastic_ip.py <instance-id> <allocation-id>")
        sys.exit(1)

    associate_elastic_ip(sys.argv[1], sys.argv[2])
