#!/usr/bin/env python3

import boto3
from botocore.exceptions import ClientError
from mypy_boto3_ec2.client import EC2Client


def list_instance_types() -> None:
    ec2: EC2Client = boto3.client("ec2")

    try:
        paginator = ec2.get_paginator("describe_instance_types")
        pages = paginator.paginate()

        print(f"{'Instance Type':<20} {'vCPUs':<6} {'Memory (GiB)':<12} {'Arch':<10}")
        print("-" * 50)

        for page in pages:
            for inst_type in page["InstanceTypes"]:
                itype = inst_type["InstanceType"]
                vcpus = inst_type["VCpuInfo"]["DefaultVCpus"]
                mem = inst_type["MemoryInfo"]["SizeInMiB"] / 1024
                archs = ", ".join(inst_type["ProcessorInfo"]["SupportedArchitectures"])
                print(f"{itype:<20} {vcpus:<6} {mem:<12.1f} {archs:<10}")
    except ClientError as e:
        print(f"❌ Error: {e.response['Error']['Message']}")


if __name__ == "__main__":
    list_instance_types()
