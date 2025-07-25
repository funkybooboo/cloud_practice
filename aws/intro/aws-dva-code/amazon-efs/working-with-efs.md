
# Working with EFS

## Launch instances in multiple AZs
1. Create a security group
aws ec2 create-security-group --group-name StorageLabs --description "Temporary SG for the Storage Service Labs"
2. Add a rule for SSH inbound to the security group
aws ec2 authorize-security-group-ingress --group-name StorageLabs --protocol tcp --port 22 --cidr 0.0.0.0/0
3. Launch instance in US-EAST-1A
aws ec2 run-instances --image-id ami-0cbbe2c6a1bb2ad63 --instance-type t2.micro --placement AvailabilityZone=us-east-1a --security-group-ids sg-0ef9aeefca9ea9d24
4. Launch instance in US-EAST-1B
aws ec2 run-instances --image-id ami-0cbbe2c6a1bb2ad63 --instance-type t2.micro --placement AvailabilityZone=us-east-1b --security-group-ids sg-0ef9aeefca9ea9d24

## Create an EFS File System
1. Add a rule to the security group to allow the NFS protocol from group members

aws ec2 authorize-security-group-ingress --group-id sg-0ef9aeefca9ea9d24 --protocol tcp --port 2049 --source-group sg-0ef9aeefca9ea9d24

2. Create an EFS file system through the console, and add the StorageLabs security group to the mount targets for each AZ

## Mount using the NFS Client (perform steps on both instances)
1. Create an EFS mount point
mkdir ~/efs-mount-point
2. Install NFS client
sudo yum -y install nfs-utils
3. Mount using the EFS client
sudo mount -t nfs4 -o nfsvers=4.1,rsize=1048576,wsize=1048576,hardn,timeo=600,retrans=2,oresvport fs-042cce83a06ba5a7c.efs.us-east-1.amazonaws.com:/ ~/efs-mount-point
4. Create a file on the file system
5. Add a file system policy to enforce encryption in-transit
6. Unmount (make sure to change directory out of efs-mount-point first)
sudo umount ~/efs-mount-point
4. Mount again using the EFS client (what happens?)

## Mount using the EFS utils (perform steps on both instances)
1. Install EFS utils
sudo yum install -y amazon-efs-utils
2. Mount using the EFS mount helper
sudo mount -t efs -o tls fs-042cce83a06ba5a7c.efs.us-east-1.amazonaws.com:/ ~/efs-mount-point
