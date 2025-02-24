import boto3

# Initialize Route 53 client
route53 = boto3.client("route53")

# Define the Hosted Zone ID (replace with your actual hosted zone ID)
hosted_zone_id = "Z04555692B7PI94BFJEBI"  # Replace with your Hosted Zone ID

# Define records
record_sets = [
    {
        "Action": "UPSERT",
        "ResourceRecordSet": {
            "Name": "example.com.",
            "Type": "A",
            "AliasTarget": {
                "HostedZoneId": "Z2FDTNDATAQYW2",  # Use correct ALB, S3, or CloudFront Hosted Zone ID
                "DNSName": "secure-LoadB-qNBBuPNmMEVs-303894070.us-east-1.elb.amazonaws.com",
                "EvaluateTargetHealth": True
            }
        }
    },
    # {
    #     "Action": "UPSERT",
    #     "ResourceRecordSet": {
    #         "Name": "www.example.com.",
    #         "Type": "CNAME",
    #         "TTL": 300,
    #         "ResourceRecords": [{"Value": "example.com."}]
    #     }
    # },
    # {
    #     "Action": "UPSERT",
    #     "ResourceRecordSet": {
    #         "Name": "example.com.",
    #         "Type": "MX",
    #         "TTL": 3600,
    #         "ResourceRecords": [
    #             {"Value": "10 mail.example.com."},
    #             {"Value": "20 backupmail.example.com."}
    #         ]
    #     }
    # },
    # {
    #     "Action": "UPSERT",
    #     "ResourceRecordSet": {
    #         "Name": "example.com.",
    #         "Type": "TXT",
    #         "TTL": 300,
    #         "ResourceRecords": [
    #             {"Value": '"v=spf1 include:_spf.example.com ~all"'}
    #         ]
    #     }
    # },
    # {
    #     "Action": "UPSERT",
    #     "ResourceRecordSet": {
    #         "Name": "_sip._tcp.example.com.",
    #         "Type": "SRV",
    #         "TTL": 300,
    #         "ResourceRecords": [
    #             {"Value": "10 5 5060 sipserver.example.com."}
    #         ]
    #     }
    # }
]

# Create Route 53 record set
print("Creating Route 53 records...")
response = route53.change_resource_record_sets(
    HostedZoneId=hosted_zone_id,
    ChangeBatch={
        "Comment": "Adding multiple records to Route 53",
        "Changes": record_sets
    }
)

print("Route 53 records created successfully.")
print("Change Info:", response["ChangeInfo"])

####################################################################################

# NOT WORKING !!


# Define the record to be deleted
record_to_delete = {
    "Name": "harnesstechtx.com",  # Replace with the actual record name
    "Type": "A",  # Replace with the actual record type (A, CNAME, TXT, etc.)
    # "TTL": 300,  # Replace with the correct TTL of the record
    "ResourceRecords": [{"Value": "dualstack.secure-loadb-qnbbupnmmevs-303894070.us-east-1.elb.amazonaws.com."}]  # Replace with the correct value
}

# Delete the Route 53 record
print(f"Deleting Route 53 record: {record_to_delete['Name']} ({record_to_delete['Type']})...")
response = route53.change_resource_record_sets(
    HostedZoneId=hosted_zone_id,
    ChangeBatch={
        "Comment": "Deleting a Route 53 record",
        "Changes": [
            {
                "Action": "DELETE",
                "ResourceRecordSet": record_to_delete
            }
        ]
    }
)

print("Record deleted successfully.")
print("Change Info:", response["ChangeInfo"])
