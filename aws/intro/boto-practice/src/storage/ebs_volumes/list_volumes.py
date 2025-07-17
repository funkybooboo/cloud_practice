#!/usr/bin/env python3

import boto3
from mypy_boto3_ec2.client import EC2Client


def list_volumes() -> None:
    ec2: EC2Client = boto3.client("ec2")
    volumes = ec2.describe_volumes()["Volumes"]

    if not volumes:
        print("⚠️ No volumes found.")
        return

    for v in volumes:
        vid = v["VolumeId"]
        size = v["Size"]
        state = v["State"]
        az = v["AvailabilityZone"]
        attached = v["Attachments"]
        attachment = f"attached to {attached[0]['InstanceId']}" if attached else "unattached"
        print(f"💽 {vid} | {size} GiB | {state} | {az} | {attachment}")


if __name__ == "__main__":
    list_volumes()
