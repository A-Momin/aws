-   In AWS, the access key ID and secret access key are used to authenticate your application or script when interacting with AWS services programmatically using AWS SDKs, including the Boto3 library for Python. Here's how you can integrate your AWS access key and secret access key with Boto3:
-   Configure AWS Credentials: Boto3 uses the AWS credentials stored in a configuration file or environment variables. The recommended approach is touse a configuration file called ~/.aws/credentials on Linux/macOS or C:\Users\<your_username>\.aws\credentials on Windows. You can create this file if it doesn't exist.
-   Open the ~/.aws/credentials file using a text editor and add your AWS access key ID and secret access key under a profile name. Here's an example:

```ini
[default]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY

```

-   Use Boto3 in Your Python Script: Once your credentials are configured, you can start using Boto3 in your Python script. Boto3 will automatically read the credentials from the configuration file and use them for authentication.

---

---

-   [Code any boto3 in AWS Lambda | Step by Step Coding | Stop EC2 Instance](https://www.youtube.com/watch?v=RL-mQWFWJcM&t=958s)
    -   [code](https://github.com/saha-rajdeep/Lambda/blob/master/publishtoEventBridge.py)
