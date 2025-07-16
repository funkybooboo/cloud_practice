#!/usr/bin/env python3

import boto3
from mypy_boto3_ec2.client import EC2Client


def list_security_groups() -> None:
    ec2: EC2Client = boto3.client("ec2")
    groups = ec2.describe_security_groups()["SecurityGroups"]

    for sg in groups:
        name = sg.get("GroupName", "Unnamed")
        group_id = sg["GroupId"]
        desc = sg["Description"]
        print(f"{group_id} | {name} | {desc}")


if __name__ == "__main__":
    list_security_groups()
