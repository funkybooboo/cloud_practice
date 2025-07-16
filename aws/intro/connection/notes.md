# 🚀 Connecting to EC2 Instances

## ✅ AWS Linux Instance (via SSH)

Use the following command to connect:

```bash
ssh -i "us-east-ns.pem" ec2-user@ec2-3-89-126-122.compute-1.amazonaws.com
```

* `us-east-ns.pem`: Your private key file
* `ec2-user`: Default username for Amazon Linux
* Make sure the `.pem` file has correct permissions:

  ```bash
  chmod 400 us-east-ns.pem
  ```

## 🪟 Windows Instance (via RDP)

Use a Remote Desktop Protocol (RDP) client to connect:

* **Host**: `ec2-3-80-155-116.compute-1.amazonaws.com`
* **Username**: `Administrator`
* **Password**: Stored in `passwd.md`

> 💡 Make sure the Windows instance has the RDP port (3389) open in its security group.
