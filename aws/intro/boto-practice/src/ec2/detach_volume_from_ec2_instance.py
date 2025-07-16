#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_ec2.client import EC2Client


def detach_volume(volume_id: str, force: bool = False) -> None:
    ec2: EC2Client = boto3.client("ec2")
    try:
        ec2.detach_volume(
            VolumeId=volume_id,
            Force=force
        )
        print(f"✅ Detached volume '{volume_id}' (force={force})")
    except ClientError as e:
        print(f"❌ Failed to detach volume: {e.response['Error']['Message']}")


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print("Usage: detach_volume_from_ec2_instance.py <volume-id> [--force]")
        sys.exit(1)

    volume_id = sys.argv[1]
    force_flag = "--force" in sys.argv
    detach_volume(volume_id, force=force_flag)
