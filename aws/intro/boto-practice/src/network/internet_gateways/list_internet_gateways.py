#!/usr/bin/env python3

import boto3
from mypy_boto3_ec2.client import EC2Client


def list_igws() -> None:
    ec2: EC2Client = boto3.client("ec2")
    igws = ec2.describe_internet_gateways()["InternetGateways"]

    if not igws:
        print("⚠️ No internet gateways found.")
        return

    for igw in igws:
        igw_id = igw["InternetGatewayId"]
        attachments = [a["VpcId"] for a in igw.get("Attachments", []) if a.get("VpcId")]
        vpcs = ", ".join(attachments) if attachments else "unattached"
        print(f"🌐 {igw_id} | attached to: {vpcs}")


if __name__ == "__main__":
    list_igws()
