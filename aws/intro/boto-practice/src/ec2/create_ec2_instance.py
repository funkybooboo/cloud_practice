#!/usr/bin/env python3

import sys
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_ec2.client import EC2Client


DEFAULT_AMI_ID = "ami-0c02fb55956c7d316"  # Amazon Linux 2023 (us-east-1)
DEFAULT_INSTANCE_TYPE = "t3.micro"


def get_default_security_group_id() -> str:
    ec2: EC2Client = boto3.client("ec2")

    vpcs = ec2.describe_vpcs(Filters=[{"Name": "isDefault", "Values": ["true"]}])["Vpcs"]
    if not vpcs:
        print("❌ No default VPC found in this region.")
        sys.exit(1)
    default_vpc_id = vpcs[0]["VpcId"]

    sgs = ec2.describe_security_groups(
        Filters=[
            {"Name": "vpc-id", "Values": [default_vpc_id]},
            {"Name": "group-name", "Values": ["default"]}
        ]
    )["SecurityGroups"]

    if not sgs:
        print("❌ No 'default' security group found in default VPC.")
        sys.exit(1)

    return sgs[0]["GroupId"]


def create_instance(
    ami_id: str,
    instance_type: str,
    key_name: str,
    security_group_id: str
) -> None:
    ec2: EC2Client = boto3.client("ec2")
    try:
        response = ec2.run_instances(
            ImageId=ami_id,
            InstanceType=instance_type,
            KeyName=key_name,
            SecurityGroupIds=[security_group_id],
            MinCount=1,
            MaxCount=1
        )
        instance_id = response["Instances"][0]["InstanceId"]
        print(f"✅ Created EC2 instance: {instance_id}")
    except ClientError as e:
        print(f"❌ Error: {e.response['Error']['Message']}")
        sys.exit(1)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Launch a basic EC2 instance")
    parser.add_argument("key_name", help="EC2 key pair name (used for SSH)")
    parser.add_argument("--ami-id", default=DEFAULT_AMI_ID, help="AMI ID (default: Amazon Linux 2023)")
    parser.add_argument("--instance-type", default=DEFAULT_INSTANCE_TYPE, help="EC2 instance type (default: t3.micro)")
    parser.add_argument("--security-group", help="Security group ID (optional, default = 'default' group)")

    args = parser.parse_args()

    sg_id = args.security_group or get_default_security_group_id()

    create_instance(
        ami_id=args.ami_id,
        instance_type=args.instance_type,
        key_name=args.key_name,
        security_group_id=sg_id
    )
