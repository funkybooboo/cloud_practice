#!/usr/bin/env python3

import boto3
from mypy_boto3_ec2.client import EC2Client


def list_instances() -> None:
    ec2: EC2Client = boto3.client("ec2")
    reservations = ec2.describe_instances()["Reservations"]

    if not reservations:
        print("📭 No instances found.")
        return

    for res in reservations:
        for inst in res["Instances"]:
            instance_id = inst["InstanceId"]
            state = inst["State"]["Name"]
            instance_type = inst["InstanceType"]
            print(f"🖥️ {instance_id} | {state} | {instance_type}")


if __name__ == "__main__":
    list_instances()
