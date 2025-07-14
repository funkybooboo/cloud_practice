#!/usr/bin/env bash
set -euo pipefail

# Check if AWS credentials are configured
if ! aws sts get-caller-identity &>/dev/null; then
  echo "No valid AWS credentials found. Running 'aws configure'..."
  aws configure
else
  echo "AWS credentials already configured."
fi

# Continue with your command
aws iam list-users
