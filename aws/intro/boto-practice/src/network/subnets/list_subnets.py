#!/usr/bin/env python3

import boto3
from mypy_boto3_ec2.client import EC2Client


def list_subnets() -> None:
    ec2: EC2Client = boto3.client("ec2")
    response = ec2.describe_subnets()

    if not response["Subnets"]:
        print("⚠️ No subnets found.")
        return

    for subnet in response["Subnets"]:
        subnet_id = subnet["SubnetId"]
        vpc_id = subnet["VpcId"]
        cidr = subnet["CidrBlock"]
        az = subnet["AvailabilityZone"]
        state = subnet["State"]
        print(f"📦 {subnet_id} | {vpc_id} | {cidr} | {az} | {state}")


if __name__ == "__main__":
    list_subnets()
