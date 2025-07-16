#!/usr/bin/env python3

import boto3
from mypy_boto3_ec2.client import EC2Client


def list_amis(owner: str = "amazon") -> None:
    ec2: EC2Client = boto3.client("ec2")

    response = ec2.describe_images(
        Owners=[owner],
        Filters=[
            {"Name": "name", "Values": ["al2023-ami-*-x86_64"]},
            {"Name": "state", "Values": ["available"]}
        ]
    )

    images = sorted(response["Images"], key=lambda x: x["CreationDate"], reverse=True)

    for img in images[:10]:
        print(f"{img['ImageId']} | {img['Name']} | {img['CreationDate']}")


if __name__ == "__main__":
    list_amis()
