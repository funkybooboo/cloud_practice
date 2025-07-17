#!/usr/bin/env python3

import sys
import boto3
from mypy_boto3_ec2.client import EC2Client


def attach_volume(instance_id: str, volume_id: str, device: str = "/dev/sdf") -> None:
    ec2: EC2Client = boto3.client("ec2")
    ec2.attach_volume(
        VolumeId=volume_id,
        InstanceId=instance_id,
        Device=device
    )
    print(f"🔗 Attached volume {volume_id} to instance {instance_id} at {device}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: attach_volume_to_ec2_instance.py <instance-id> <volume-id> [device]")
        sys.exit(1)

    attach_volume(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "/dev/sdf")
