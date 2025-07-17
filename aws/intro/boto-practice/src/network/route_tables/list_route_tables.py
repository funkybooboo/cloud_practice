#!/usr/bin/env python3

import boto3
from mypy_boto3_ec2.client import EC2Client


def list_route_tables() -> None:
    ec2: EC2Client = boto3.client("ec2")
    response = ec2.describe_route_tables()

    if not response["RouteTables"]:
        print("⚠️ No route tables found.")
        return

    for rt in response["RouteTables"]:
        rt_id = rt["RouteTableId"]
        vpc_id = rt["VpcId"]
        associations = ", ".join(a.get("SubnetId", "main") for a in rt.get("Associations", []))
        print(f"📚 {rt_id} | VPC: {vpc_id} | Subnets: {associations}")


if __name__ == "__main__":
    list_route_tables()
