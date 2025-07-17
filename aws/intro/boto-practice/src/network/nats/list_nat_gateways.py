#!/usr/bin/env python3

import boto3
from mypy_boto3_ec2.client import EC2Client


def list_nat_gateways() -> None:
    ec2: EC2Client = boto3.client("ec2")
    response = ec2.describe_nat_gateways()

    if not response["NatGateways"]:
        print("⚠️ No NAT Gateways found.")
        return

    for nat in response["NatGateways"]:
        nat_id = nat["NatGatewayId"]
        subnet = nat["SubnetId"]
        state = nat["State"]
        public_ip = next((addr.get("PublicIp") for addr in nat.get("NatGatewayAddresses", [])), "N/A")
        print(f"🌐 {nat_id} | Subnet: {subnet} | State: {state} | Public IP: {public_ip}")


if __name__ == "__main__":
    list_nat_gateways()
