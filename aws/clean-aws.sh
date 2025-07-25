#!/usr/bin/env bash
set -euo pipefail

command -v aws >/dev/null || { echo "❌ aws CLI not found"; exit 1; }

AWS_PROFILE="${AWS_PROFILE:-default}"
AWS_REGION="${AWS_REGION:-us-east-1}"

# Flags: delete everything by default (except IAM)
DELETE_EC2=true
DELETE_S3=true
DELETE_LAMBDA=true
DELETE_LOGS=true
DELETE_EIP=true
DELETE_SECURITY_GROUPS=true
DELETE_VOLUMES=true
DELETE_VPCS=true
DELETE_IAM=false
DRY_RUN=false

# Help text
show_help() {
  cat <<EOF
Usage: $0 [OPTIONS]

Deletes all non-default AWS resources in the current account and region,
unless specific exclusions are passed as flags.

Options:
  --no-ec2               Skip deletion of EC2 instances
  --no-volumes           Skip deletion of EBS volumes
  --no-eip               Skip deletion of Elastic IPs
  --no-sg | --no-security-groups
                         Skip deletion of non-default security groups
  --no-s3                Skip deletion of all S3 buckets
  --no-lambda            Skip deletion of Lambda functions
  --no-logs              Skip deletion of CloudWatch log groups
  --no-vpc | --no-vpcs   Skip deletion of non-default VPCs
  --iam                  ALSO delete all IAM users, roles, and groups (DANGEROUS)
  --dry-run              Show what would be deleted, but take no action
  --help                 Show this help message and exit

Environment variables:
  AWS_PROFILE            AWS profile to use (default: "default")
  AWS_REGION             AWS region to use (default: "us-east-1")
EOF
}

# Parse arguments
for arg in "$@"; do
  case "$arg" in
    --no-ec2) DELETE_EC2=false ;;
    --no-s3) DELETE_S3=false ;;
    --no-lambda) DELETE_LAMBDA=false ;;
    --no-logs) DELETE_LOGS=false ;;
    --no-eip) DELETE_EIP=false ;;
    --no-sg|--no-security-groups) DELETE_SECURITY_GROUPS=false ;;
    --no-volumes) DELETE_VOLUMES=false ;;
    --no-vpc|--no-vpcs) DELETE_VPCS=false ;;
    --iam) DELETE_IAM=true ;;
    --dry-run) DRY_RUN=true ;;
    --help) show_help; exit 0 ;;
    *)
      echo "❌ Unknown argument: $arg"
      echo "Run \`$0 --help\` for usage."
      exit 1
      ;;
  esac
done

# Region validation
if ! aws ec2 describe-regions --query "Regions[].RegionName" --output text --profile "$AWS_PROFILE" | grep -qw "$AWS_REGION"; then
  echo "❌ Invalid AWS region: $AWS_REGION"
  exit 1
fi

# Profile & credential validation
if ! aws sts get-caller-identity --profile "$AWS_PROFILE" --region "$AWS_REGION" &>/dev/null; then
  echo "❌ AWS CLI is not configured correctly for profile '$AWS_PROFILE' and region '$AWS_REGION'"
  echo "   Run: aws configure --profile \"$AWS_PROFILE\""
  exit 1
fi

# Dry-run wrapper
run_or_echo() {
  if [ "$DRY_RUN" = true ]; then
    echo "[DRY-RUN] $*"
  else
    eval "$@"
  fi
}

echo "⚠️  WARNING: This script will delete AWS resources in account '$AWS_PROFILE' ($AWS_REGION)"
if [ "$DELETE_IAM" = true ]; then
  echo "⚠️  IAM deletion is ENABLED — users, roles, groups may be removed"
fi
if [ "$DRY_RUN" = true ]; then
  echo "🔎 Dry-run mode enabled — no resources will be deleted"
fi

read -rp "Are you sure you want to proceed? (y/N) " confirm
[[ "$confirm" == "y" || "$confirm" == "Y" ]] || exit 0

# --- EC2 ---
if [ "$DELETE_EC2" = true ]; then
  echo "🧨 Terminating EC2 instances..."
  instance_ids=$(aws ec2 describe-instances --profile "$AWS_PROFILE" --region "$AWS_REGION" \
    --query "Reservations[].Instances[].InstanceId" --output text)
  if [[ -n "$instance_ids" ]]; then
    run_or_echo aws ec2 terminate-instances --instance-ids $instance_ids --profile "$AWS_PROFILE" --region "$AWS_REGION"
    run_or_echo aws ec2 wait instance-terminated --instance-ids $instance_ids --profile "$AWS_PROFILE" --region "$AWS_REGION" || true
  fi
fi

# --- EBS Volumes ---
if [ "$DELETE_VOLUMES" = true ]; then
  echo "🧹 Deleting EBS volumes..."
  volume_ids=$(aws ec2 describe-volumes --profile "$AWS_PROFILE" --region "$AWS_REGION" \
    --query "Volumes[?State=='available'].VolumeId" --output text)
  for vol in $volume_ids; do
    run_or_echo aws ec2 delete-volume --volume-id "$vol" --profile "$AWS_PROFILE" --region "$AWS_REGION"
  done
fi

# --- Elastic IPs ---
if [ "$DELETE_EIP" = true ]; then
  echo "🌐 Releasing Elastic IPs..."
  eip_ids=$(aws ec2 describe-addresses --profile "$AWS_PROFILE" --region "$AWS_REGION" \
    --query "Addresses[].AllocationId" --output text)
  for eip in $eip_ids; do
    run_or_echo aws ec2 release-address --allocation-id "$eip" --profile "$AWS_PROFILE" --region "$AWS_REGION"
  done
fi

# --- Security Groups ---
if [ "$DELETE_SECURITY_GROUPS" = true ]; then
  echo "🚧 Deleting non-default Security Groups..."
  sg_ids=$(aws ec2 describe-security-groups --profile "$AWS_PROFILE" --region "$AWS_REGION" \
    --query "SecurityGroups[?GroupName!='default'].GroupId" --output text)
  for sg in $sg_ids; do
    run_or_echo aws ec2 delete-security-group --group-id "$sg" --profile "$AWS_PROFILE" --region "$AWS_REGION"
  done
fi

# --- S3 Buckets ---
if [ "$DELETE_S3" = true ]; then
  echo "🪣 Deleting S3 buckets..."
  bucket_names=$(aws s3api list-buckets --profile "$AWS_PROFILE" --query "Buckets[].Name" --output text)
  for b in $bucket_names; do
    run_or_echo aws s3 rb "s3://$b" --force --profile "$AWS_PROFILE"
  done
fi

# --- Lambda ---
if [ "$DELETE_LAMBDA" = true ]; then
  echo "🐑 Deleting Lambda functions..."
  lambda_fns=$(aws lambda list-functions --profile "$AWS_PROFILE" --region "$AWS_REGION" \
    --query "Functions[].FunctionName" --output text)
  for fn in $lambda_fns; do
    run_or_echo aws lambda delete-function --function-name "$fn" --profile "$AWS_PROFILE" --region "$AWS_REGION"
  done
fi

# --- CloudWatch Logs ---
if [ "$DELETE_LOGS" = true ]; then
  echo "📉 Deleting CloudWatch log groups..."
  log_groups=$(aws logs describe-log-groups --profile "$AWS_PROFILE" --region "$AWS_REGION" \
    --query "logGroups[].logGroupName" --output text)
  for lg in $log_groups; do
    run_or_echo aws logs delete-log-group --log-group-name "$lg" --profile "$AWS_PROFILE" --region "$AWS_REGION"
  done
fi

# --- VPCs ---
if [ "$DELETE_VPCS" = true ]; then
  echo "🏗  Deleting non-default VPCs and dependencies..."
  vpc_ids=$(aws ec2 describe-vpcs --profile "$AWS_PROFILE" --region "$AWS_REGION" \
    --query "Vpcs[?IsDefault==\`false\`].VpcId" --output text)

  for vpc_id in $vpc_ids; do
    echo " - Cleaning up VPC: $vpc_id"

    igws=$(aws ec2 describe-internet-gateways --filters "Name=attachment.vpc-id,Values=$vpc_id" \
      --query "InternetGateways[].InternetGatewayId" --output text --profile "$AWS_PROFILE" --region "$AWS_REGION")
    for igw in $igws; do
      run_or_echo aws ec2 detach-internet-gateway --internet-gateway-id "$igw" --vpc-id "$vpc_id" --profile "$AWS_PROFILE" --region "$AWS_REGION"
      run_or_echo aws ec2 delete-internet-gateway --internet-gateway-id "$igw" --profile "$AWS_PROFILE" --region "$AWS_REGION"
    done

    subnets=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$vpc_id" \
      --query "Subnets[].SubnetId" --output text --profile "$AWS_PROFILE" --region "$AWS_REGION")
    for sn in $subnets; do
      run_or_echo aws ec2 delete-subnet --subnet-id "$sn" --profile "$AWS_PROFILE" --region "$AWS_REGION"
    done

    rt_ids=$(aws ec2 describe-route-tables --filters "Name=vpc-id,Values=$vpc_id" \
      --query "RouteTables[?Associations[?Main!=\`true\`]].RouteTableId" --output text --profile "$AWS_PROFILE" --region "$AWS_REGION")
    for rt in $rt_ids; do
      run_or_echo aws ec2 delete-route-table --route-table-id "$rt" --profile "$AWS_PROFILE" --region "$AWS_REGION"
    done

    acls=$(aws ec2 describe-network-acls --filters "Name=vpc-id,Values=$vpc_id" \
      --query "NetworkAcls[?IsDefault==\`false\`].NetworkAclId" --output text --profile "$AWS_PROFILE" --region "$AWS_REGION")
    for acl in $acls; do
      run_or_echo aws ec2 delete-network-acl --network-acl-id "$acl" --profile "$AWS_PROFILE" --region "$AWS_REGION"
    done

    run_or_echo aws ec2 delete-vpc --vpc-id "$vpc_id" --profile "$AWS_PROFILE" --region "$AWS_REGION"
  done
fi

# --- IAM ---
if [ "$DELETE_IAM" = true ]; then
  echo "🧨 Deleting IAM Users, Groups, and Roles..."

  for role in $(aws iam list-roles --query "Roles[].RoleName" --output text --profile "$AWS_PROFILE"); do
    attached=$(aws iam list-attached-role-policies --role-name "$role" --query "AttachedPolicies[].PolicyArn" --output text --profile "$AWS_PROFILE")
    for arn in $attached; do
      run_or_echo aws iam detach-role-policy --role-name "$role" --policy-arn "$arn" --profile "$AWS_PROFILE"
    done
    run_or_echo aws iam delete-role --role-name "$role" --profile "$AWS_PROFILE"
  done

  for group in $(aws iam list-groups --query "Groups[].GroupName" --output text --profile "$AWS_PROFILE"); do
    users=$(aws iam get-group --group-name "$group" --query "Users[].UserName" --output text --profile "$AWS_PROFILE")
    for user in $users; do
      run_or_echo aws iam remove-user-from-group --group-name "$group" --user-name "$user" --profile "$AWS_PROFILE"
    done
    run_or_echo aws iam delete-group --group-name "$group" --profile "$AWS_PROFILE"
  done

  for user in $(aws iam list-users --query "Users[].UserName" --output text --profile "$AWS_PROFILE"); do
    keys=$(aws iam list-access-keys --user-name "$user" --query "AccessKeyMetadata[].AccessKeyId" --output text --profile "$AWS_PROFILE")
    for key in $keys; do
      run_or_echo aws iam delete-access-key --access-key-id "$key" --user-name "$user" --profile "$AWS_PROFILE"
    done
    run_or_echo aws iam delete-user --user-name "$user" --profile "$AWS_PROFILE"
  done
fi

echo "✅ Cleanup complete."
