#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_ec2.client import EC2Client


def attach_volume(instance_id: str, volume_id: str, device_name: str) -> None:
    ec2: EC2Client = boto3.client("ec2")

    try:
        ec2.attach_volume(
            InstanceId=instance_id,
            VolumeId=volume_id,
            Device=device_name
        )
        print(f"✅ Attached volume '{volume_id}' to instance '{instance_id}' at '{device_name}'")
    except ClientError as e:
        print(f"❌ Failed to attach volume: {e.response['Error']['Message']}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: attach_volume_to_ec2_instance.py <instance-id> <volume-id> <device-name>")
        print("Example device-name: /dev/sdf")
        sys.exit(1)

    attach_volume(sys.argv[1], sys.argv[2], sys.argv[3])
