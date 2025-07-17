#!/usr/bin/env python3

import sys
import boto3
from mypy_boto3_ec2.client import EC2Client
from botocore.exceptions import ClientError


def create_volume(size_gb: int, availability_zone: str, volume_type: str = "gp3") -> None:
    ec2: EC2Client = boto3.client("ec2")
    try:
        response = ec2.create_volume(
            Size=size_gb,
            AvailabilityZone=availability_zone,
            VolumeType=volume_type,
            TagSpecifications=[{
                "ResourceType": "volume",
                "Tags": [{"Key": "Name", "Value": "CreatedVolume"}]
            }]
        )
        volume_id = response["VolumeId"]
        print(f"✅ Created volume: {volume_id} ({size_gb} GiB, {volume_type}) in {availability_zone}")
    except ClientError as e:
        print(f"❌ Error: {e.response['Error']['Message']}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: create_volume.py <size-gb> <availability-zone> [volume-type]")
        sys.exit(1)

    size = int(sys.argv[1])
    az = sys.argv[2]
    vol_type = sys.argv[3] if len(sys.argv) > 3 else "gp3"

    create_volume(size, az, vol_type)
