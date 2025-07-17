#!/usr/bin/env python3

import boto3
from mypy_boto3_ec2.client import EC2Client


def list_vpc_endpoints() -> None:
    ec2: EC2Client = boto3.client("ec2")
    response = ec2.describe_vpc_endpoints()

    if not response["VpcEndpoints"]:
        print("⚠️ No VPC Endpoints found.")
        return

    for ep in response["VpcEndpoints"]:
        ep_id = ep["VpcEndpointId"]
        service = ep["ServiceName"]
        vpc_id = ep["VpcId"]
        state = ep["State"]
        rt_ids = ", ".join(ep.get("RouteTableIds", []))
        print(f"🌐 {ep_id} | Service: {service} | VPC: {vpc_id} | State: {state} | Route Tables: {rt_ids}")


if __name__ == "__main__":
    list_vpc_endpoints()
