#!/usr/bin/env python3

import boto3
from mypy_boto3_ec2.client import EC2Client


def create_instance(ami_id: str, instance_type: str, key_name: str, security_group: str) -> None:
    ec2: EC2Client = boto3.client("ec2")
    response = ec2.run_instances(
        ImageId=ami_id,
        InstanceType=instance_type,
        KeyName=key_name,
        SecurityGroupIds=[security_group],
        MinCount=1,
        MaxCount=1
    )
    instance_id = response["Instances"][0]["InstanceId"]
    print(f"✅ Created instance: {instance_id}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 5:
        print("Usage: create_ec2_instance.py <ami-id> <instance-type> <key-name> <security-group-id>")
        sys.exit(1)

    create_instance(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
