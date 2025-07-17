#!/usr/bin/env python3

import sys
import boto3
from mypy_boto3_ec2.client import EC2Client
from botocore.exceptions import ClientError


def create_key_pair(name: str, output_path: str) -> None:
    ec2: EC2Client = boto3.client("ec2")
    try:
        response = ec2.create_key_pair(KeyName=name)
        key_material = response["KeyMaterial"]

        with open(output_path, "w") as f:
            f.write(key_material)

        print(f"✅ Created key pair '{name}'")
        print(f"🔐 Private key saved to: {output_path}")
        print("🔒 Remember to run: chmod 400", output_path)
    except ClientError as e:
        print(f"❌ Error: {e.response['Error']['Message']}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: create_key_pair.py <key-name> <output-path.pem>")
        sys.exit(1)
    create_key_pair(sys.argv[1], sys.argv[2])
