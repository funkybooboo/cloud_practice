#!/usr/bin/env python3

import boto3
from mypy_boto3_ec2.client import EC2Client


def list_vpcs() -> None:
    ec2: EC2Client = boto3.client("ec2")
    vpcs = ec2.describe_vpcs()["Vpcs"]

    if not vpcs:
        print("⚠️ No VPCs found.")
        return

    for vpc in vpcs:
        vpc_id = vpc["VpcId"]
        cidr = vpc["CidrBlock"]
        is_default = vpc.get("IsDefault", False)
        state = vpc["State"]
        print(f"🌐 {vpc_id} | {cidr} | {'default' if is_default else 'custom'} | {state}")


if __name__ == "__main__":
    list_vpcs()
