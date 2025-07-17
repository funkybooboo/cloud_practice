#!/usr/bin/env python3

import boto3
from mypy_boto3_ec2.client import EC2Client
from mypy_boto3_ec2.type_defs import SecurityGroupTypeDef


def list_security_groups() -> None:
    ec2: EC2Client = boto3.client("ec2")
    response = ec2.describe_security_groups()
    groups: list[SecurityGroupTypeDef] = response["SecurityGroups"]

    for sg in groups:
        print(f"{sg['GroupId']} | {sg['GroupName']} | {sg['Description']}")


if __name__ == "__main__":
    list_security_groups()
