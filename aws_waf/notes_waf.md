<details><summary style="font-size:25px;color:Orange">AWS WAF Hands-on</summary>

Here's a **step-by-step hands-on guide** to setting up AWS WAF to **protect your web application**.

---

# **Step 1: Create a Web ACL (Access Control List)**

A Web ACL is the main configuration where you define security rules for your AWS WAF setup.

## **1.1 Navigate to AWS WAF in the Console**

1. Sign in to the **AWS Management Console**.
2. Go to **AWS WAF & Shield** (Search for "AWS WAF" in the search bar).
3. Click **Web ACLs** on the left panel.
4. Click **Create web ACL**.

## **1.2 Configure Web ACL Settings**

-   **Name:** `MyWebACL`
-   **Region:** Choose the region where your application is hosted.
-   **Resource Type:** Choose what you want to protect:
    -   **CloudFront** (best for global traffic).
    -   **Application Load Balancer (ALB)** (best for AWS-hosted applications).
    -   **API Gateway** (best for REST APIs).
-   Click **Next**.

---

# **Step 2: Add Rules to Your Web ACL**

Now, add security rules to filter malicious traffic.

## **2.1 Add AWS Managed Rules (Recommended)**

AWS provides pre-configured **Managed Rule Groups** for common threats:

1. Click **Add Rules** → Select **Add managed rule groups**.
2. Choose the **AWS Managed Rules**:
    - ✅ `AWSManagedRulesCommonRuleSet` (protects against SQL Injection & XSS).
    - ✅ `AWSManagedRulesAmazonIpReputationList` (blocks bad bots & malicious IPs).
    - ✅ `AWSManagedRulesKnownBadInputsRuleSet` (detects bad query strings).
3. Click **Add Rules**.

---

## **2.2 Add Custom Rules (Optional, Advanced Users)**

To create a custom rule, click **Add My Own Rules and Rule Groups** and select one of the following:

### **Block Requests from a Specific Country**

1. Click **Add rule** → **Rule Builder**.
2. Name the rule: `BlockFromSpecificCountry`.
3. **If a request matches:**
    - `Geographic match condition`.
    - Choose **Country** (e.g., Russia, China, North Korea).
4. **Action:** `Block`.
5. Click **Save rule**.

### **Rate-Limiting (DDoS Protection)**

1. Click **Add rule** → **Rate-based rule**.
2. Name the rule: `DDoSProtection`.
3. Set **Requests per 5 minutes:** `2000`.
4. **Scope-down conditions:** (e.g., apply only to `/login` endpoint).
5. **Action:** `Block`.
6. Click **Save rule**.

---

# **Step 3: Set Default Web ACL Action**

-   If none of the rules match, should AWS WAF **allow or block** requests?
-   Recommended: Set to **Allow all requests that don’t match any rule**.

Click **Next**.

---

# **Step 4: Associate the Web ACL with a Resource**

Now, attach your Web ACL to your application.

-   **Choose a resource** (CloudFront, ALB, or API Gateway).
-   Select your **CloudFront distribution, ALB, or API Gateway API**.
-   Click **Next**.

---

# **Step 5: Review and Create**

-   Review your **Web ACL settings** and **rules**.
-   Click **Create Web ACL**.

✅ **Congratulations!** You have successfully created an AWS WAF Web ACL. 🚀

---

# **Step 6: Test Your AWS WAF Configuration**

### **6.1 Enable Logging for Monitoring**

1. Go to **AWS WAF** → Click on your Web ACL.
2. Click **Logging and metrics** → **Enable logging**.
3. Select **Amazon S3, CloudWatch Logs, or Kinesis Data Firehose**.

### **6.2 Simulate Traffic & View Logs**

1. Use an API client (Postman, curl, or browser) to send requests to your web application.
2. Go to **AWS WAF Metrics** → Check blocked requests.

---

# **Step 7: Fine-Tune Your Rules**

After a few days, review logs and:

-   **Modify rate limits** if legitimate users are blocked.
-   **Add more rules** if specific attack patterns emerge.
-   **Whitelist safe IPs** if necessary.

---

## **Summary of Steps**

| Step                      | Description                                   |
| ------------------------- | --------------------------------------------- |
| **1. Create Web ACL**     | Define Web ACL in AWS WAF Console             |
| **2. Add Rules**          | Use AWS Managed Rules & Custom Rules          |
| **3. Set Default Action** | Allow or Block unknown traffic                |
| **4. Associate Web ACL**  | Attach WAF to CloudFront, ALB, or API Gateway |
| **5. Enable Logging**     | Store logs in S3, CloudWatch, or Kinesis      |
| **6. Test & Monitor**     | Simulate traffic and check blocked requests   |
| **7. Optimize Rules**     | Fine-tune settings for better protection      |

---

🔥 **Next Steps**  
Would you like a **Terraform or AWS CLI** script to automate this setup? 🚀

</details>

```ini
provider "aws" {
  region = "us-east-1"  # Change to your AWS region
}

# Step 1: Create Web ACL
resource "aws_wafv2_web_acl" "my_waf" {
  name        = "MyWebACL"
  scope       = "REGIONAL"  # Use "CLOUDFRONT" for CloudFront
  description = "Web ACL for ALB protection"
  default_action {
    allow {}  # Allow traffic by default
  }

  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name                = "MyWebACL"
    sampled_requests_enabled   = true
  }

  # Step 2: Add AWS Managed Rules
  rule {
    name     = "AWS-CommonRuleSet"
    priority = 1
    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesCommonRuleSet"
        vendor_name = "AWS"
      }
    }
    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "AWS-CommonRuleSet"
      sampled_requests_enabled   = true
    }
    action {
      block {}  # Block requests that match the rule
    }
  }

  rule {
    name     = "AWS-BadIPs"
    priority = 2
    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesAmazonIpReputationList"
        vendor_name = "AWS"
      }
    }
    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "AWS-BadIPs"
      sampled_requests_enabled   = true
    }
    action {
      block {}
    }
  }
}

# Step 3: Attach Web ACL to ALB
resource "aws_wafv2_web_acl_association" "my_waf_alb_association" {
  resource_arn = aws_lb.my_alb.arn  # Replace with your ALB ARN
  web_acl_arn  = aws_wafv2_web_acl.my_waf.arn
}

# (Optional) Step 4: Create an Application Load Balancer (ALB)
resource "aws_lb" "my_alb" {
  name               = "my-app-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.lb_sg.id]
  subnets           = [aws_subnet.public_1.id, aws_subnet.public_2.id]
}

# (Optional) Step 5: ALB Security Group
resource "aws_security_group" "lb_sg" {
  name_prefix = "lb-sg-"
  vpc_id      = aws_vpc.main.id  # Replace with your VPC ID

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

```python
import boto3
import json

# AWS region
REGION = "us-east-1"

# WAF details
WAF_NAME = "MyWebACL"
SCOPE = "REGIONAL"  # Use "CLOUDFRONT" for CloudFront

# Load balancer ARN (Replace with your ALB ARN)
ALB_ARN = "arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/MyALB/abcdef123456"

# Initialize WAF client
waf_client = boto3.client("wafv2", region_name=REGION)

def create_web_acl():
    """Creates an AWS WAF Web ACL with managed rules."""
    response = waf_client.create_web_acl(
        Name=WAF_NAME,
        Scope=SCOPE,
        DefaultAction={"Allow": {}},  # Allow all traffic by default
        Description="Web ACL for ALB protection",
        VisibilityConfig={
            "SampledRequestsEnabled": True,
            "CloudWatchMetricsEnabled": True,
            "MetricName": WAF_NAME,
        },
        Rules=[
            {
                "Name": "AWS-CommonRuleSet",
                "Priority": 1,
                "Statement": {
                    "ManagedRuleGroupStatement": {
                        "Name": "AWSManagedRulesCommonRuleSet",
                        "VendorName": "AWS",
                    }
                },
                "VisibilityConfig": {
                    "SampledRequestsEnabled": True,
                    "CloudWatchMetricsEnabled": True,
                    "MetricName": "AWS-CommonRuleSet",
                },
                "Action": {"Block": {}},  # Block requests that match the rule
            },
            {
                "Name": "AWS-BadIPs",
                "Priority": 2,
                "Statement": {
                    "ManagedRuleGroupStatement": {
                        "Name": "AWSManagedRulesAmazonIpReputationList",
                        "VendorName": "AWS",
                    }
                },
                "VisibilityConfig": {
                    "SampledRequestsEnabled": True,
                    "CloudWatchMetricsEnabled": True,
                    "MetricName": "AWS-BadIPs",
                },
                "Action": {"Block": {}},
            },
        ],
    )

    print(f"Web ACL '{WAF_NAME}' created successfully.")
    return response["Summary"]["ARN"]


def associate_web_acl(web_acl_arn):
    """Associates the Web ACL with an ALB."""
    waf_client.associate_web_acl(
        WebACLArn=web_acl_arn,
        ResourceArn=ALB_ARN
    )
    print(f"Web ACL '{WAF_NAME}' associated with ALB successfully.")


if __name__ == "__main__":
    web_acl_arn = create_web_acl()
    associate_web_acl(web_acl_arn)

```
