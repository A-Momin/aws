import boto3
import time

# Initialize the ACM client
acm_client = boto3.client("acm", region_name="us-east-1")  # Change region as needed
route53 = boto3.client("route53")
hosted_zone_id = "Z04555692B7PI94BFJEBI"  # Replace with actual hosted zone ID

# Define certificate details
domain_name = "harnesstechtx.com"  # Replace with your domain
alternative_names = ["www.harnesstechtx.com", "sub.harnesstechtx.com"]  # Replace with alternative domain names

# Request a public certificate
print(f"Requesting SSL/TLS certificate for domain: {domain_name}")
response = acm_client.request_certificate(
    DomainName=domain_name,
    SubjectAlternativeNames=alternative_names,
    ValidationMethod="DNS",  # Can be "DNS" or "EMAIL"
    Options={"CertificateTransparencyLoggingPreference": "ENABLED"},
    Tags=[{"Key": "Environment", "Value": "QA"}]
)


# Get the certificate ARN
certificate_arn = response["CertificateArn"]
print(f"Certificate request initiated. ARN: {certificate_arn}")

# Wait for ACM to generate validation records
print("Waiting for ACM to generate DNS validation records...")
time.sleep(10)  # Give AWS some time to generate records

# Fetch DNS validation details
certificate_details = acm_client.describe_certificate(CertificateArn=certificate_arn)
dns_records = []
for domain_validation in certificate_details["Certificate"]["DomainValidationOptions"]:
    if "ResourceRecord" in domain_validation:
        dns_records.append(domain_validation["ResourceRecord"])

# Add DNS validation records to Route 53
changes = []
for record in dns_records:
    changes.append({
        "Action": "UPSERT",
        "ResourceRecordSet": {
            "Name": record["Name"],
            "Type": record["Type"],
            "TTL": 300,
            "ResourceRecords": [{"Value": record["Value"]}]
        }
    })

print("Adding DNS validation records to Route 53...")
route53.change_resource_record_sets(
    HostedZoneId=hosted_zone_id,
    ChangeBatch={
        "Comment": "Adding DNS validation records for ACM",
        "Changes": changes
    }
)

print("DNS records added successfully. Waiting for validation...")

# Wait for ACM validation
while True:
    certificate_status = acm_client.describe_certificate(CertificateArn=certificate_arn)["Certificate"]["Status"]
    print(f"Current certificate status: {certificate_status}")

    if certificate_status == "ISSUED":
        print(f"Certificate successfully validated and issued: {certificate_arn}")
        break
    elif certificate_status == "FAILED":
        print("Certificate validation failed. Check AWS ACM console.")
        break

    time.sleep(30)  # Wait before checking again

print("Script execution complete.")

# response = acm_client.delete_certificate(CertificateArn=certificate_arn)
