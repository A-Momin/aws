-   [Digital Cloud - AWS VPC Tutorial](https://www.youtube.com/watch?v=g2JOHLHh4rI)
-   [AWS VPC Beginner to Pro - Virtual Private Cloud Tutorial](https://www.youtube.com/watch?v=g2JOHLHh4rI&t=5818s)
-   [BeBetterDev: Introduction to Amazon VPC (with Console Tutorial)](https://www.youtube.com/watch?v=ApGz8tpNLgo)
-   [BeBetterDev: AWS VPC Guides](https://www.youtube.com/playlist?list=PL9nWRykSBSFhzwFa9Z5PqBM0XON8hpXE7)

<details><summary style="font-size:25px;color:Orange">IPv4 Addressing Primer</summary>

</details>

<details><summary style="font-size:25px;color:Orange">VPC Basics</summary>

-   **Region Scope**: VPCs are always within a region and cannot span across multiple regions.
-   **Logical Isolation**: A VPC is essentially a logical section of the AWS cloud that you can use to deploy your resources inside it. It's different from the public space outside of the VPC, where services like Amazon S3 reside. This is a private space, and you have full control over how you configure your VPC.

#### Components of VPC

-   **Subnets**:

    -   You create subnets within your VPC and assign them to an availability zone (AZ). A subnet is always assigned to one AZ and cannot span across multiple AZs. However, you can have multiple subnets within the same AZ.
    -   Resources like EC2 instances are deployed into these subnets.

-   **VPC Router**: While you don't directly see the VPC router, it exists and is interacted with by configuring route tables. The VPC router handles all routing for connections going outside a subnet.

-   **Route Tables**: These are used to configure routing within the VPC. You specify destinations and targets for certain networks, helping the VPC router know where to send connection attempts.

-   **Internet Gateway**: Attached to your VPC, this allows egress (outbound) and ingress (inbound) traffic between your VPC and the internet. Each VPC can have only one Internet Gateway.

-   **CIDR Blocks**: Each VPC has a CIDR block, which is the overall block of addresses from which you then create the subnets. It's essential to plan your CIDR blocks properly to ensure enough networks and hosts.

#### Advanced VPC Concepts

-   **Egress-Only Internet Gateway**: For IPv6 traffic, it allows outbound traffic only.

-   **VPC Peering**: Allows you to connect multiple VPCs, enabling routing between them.

-   **Endpoints**: Allow private IP addresses to access public AWS services without traversing the internet.

-   **Virtual Private Gateway and Customer Gateway**: Used for creating VPN connections to your on-premises networks.

-   **Direct Connect**: Provides a private, dedicated connection from your data center to AWS.

-   **Security Groups and Network ACLs**: Security groups are instance-level firewalls, while Network ACLs are subnet-level firewalls.

#### Planning and Configuring VPC

-   **CIDR Block Planning**:

    -   AWS recommends using the private IP ranges defined by RFC 1918.
    -   Ensure the CIDR block size is between /16 and /28, and it should not overlap with any existing CIDR blocks.
    -   Plan for enough networks and hosts per network.

-   **Example**:

    -   For a VPC with CIDR block 10.0.0.0/16, you can create subnets like 10.0.1.0/24, 10.0.2.0/24, etc.
    -   This ensures each subnet has 254 usable IP addresses (after accounting for AWS reserved addresses).

-   **High Availability and Resilience**:

    -   Consider deploying application tiers across multiple AZs for high availability.
    -   Use separate subnets for different application tiers (e.g., web, application, database tiers).

#### Best Practices

-   **Avoid Overlapping CIDR Blocks**: Ensure no overlapping CIDR blocks across all VPCs, regions, and accounts to prevent routing issues.

-   **Subnet Design**:

    -   Smaller subnets are usually sufficient and offer better IP address management.
    -   Plan for future growth and possible VPC peering scenarios.

#### Summary

-   A VPC is a virtual network dedicated to your AWS account, giving you full control over your network settings.

-   You can create multiple VPCs within a region, with each VPC having its own CIDR block and associated subnets.

-   Proper planning of CIDR blocks and subnets is crucial for efficient network management and future scalability.

</details>

<details><summary style="font-size:25px;color:Orange">VPC Wizard</summary>

Hey guys! In this lesson, I'm going to show you how to use the VPC wizard. The wizard helps you easily create a VPC without much manual work. We'll go through the VPC wizard options in the AWS Management Console.

#### Step-by-Step Guide to Using the VPC Wizard

-   **Accessing the VPC Wizard**:

    -   Go to the AWS Management Console.
    -   Navigate to Networking & Content Delivery and select VPC.
    -   On the VPC dashboard, choose Launch VPC Wizard.

-   **VPC Wizard Options**: The wizard offers four different pre-configured options for creating a VPC. Let's go through each of them.

    -   **Option 1**: VPC with a Single Public Subnet

        -   `Configuration`:
            -   You get a /16 CIDR block and a /24 subnet, which is a public subnet.
            -   You can specify the CIDR block or use the default provided.
            -   Optionally, specify a name for your VPC and subnet, and choose an Availability Zone (AZ) if desired.
        -   `Automatic Tasks`: The wizard automatically attaches an Internet Gateway, providing internet connectivity for your public subnet.

    -   **Option 2**: VPC with Public and Private Subnets

        -   `Configuration`:
            -   This option creates both public and private subnets.
            -   You get a Network Address Translation (NAT) gateway for your private instances to access the internet.
            -   You need to allocate an Elastic IP for the NAT gateway.
        -   `Automatic Tasks`: The wizard configures the subnets and the NAT gateway.

    -   **Option 3**: VPC with Public and Private Subnets and Hardware VPN Access

        -   `Configuration`:
            -   This option includes public and private subnets, and also sets up a VPN tunnel to your corporate data center.
            -   You need to provide the customer gateway IP, which is the IP address of your VPN device in your corporate data center.
        -   `Automatic Tasks`: The wizard configures the subnets, NAT gateway, and the VPN connection.

    -   **Option 4**: VPC with a Private Subnet Only and Hardware VPN Access
        -   `Configuration`:
            -   Similar to the previous option, but only a private subnet is created.
            -   There is no internet access from this private subnet; it only has VPN connectivity to your corporate data center.
            -   You need to provide the customer gateway IP.
        -   `Automatic Tasks`: The wizard configures the private subnet and the VPN connection.

#### Creating a VPC with the Wizard

Let's walk through creating a VPC using the second option, "VPC with Public and Private Subnets".

-   **Select the Option**:On the VPC wizard page, select VPC with Public and Private Subnets.

-   **Configuration Details**:

    -   Enter a name for your VPC.
    -   Optionally, modify the CIDR block for the VPC and subnets, or leave the defaults.
    -   Choose an AZ if desired.
    -   Allocate an Elastic IP for the NAT gateway.

-   **Create the VPC**:

    -   Click Create VPC.
    -   The wizard will automatically create and configure the VPC, subnets, Internet Gateway, and NAT gateway.

#### Summary

-   The VPC wizard simplifies the process of creating VPCs with various configurations.

-   You can create VPCs with different combinations of public and private subnets, NAT gateways, and VPN connections.

-   Use the wizard to quickly set up your networking environment in AWS with minimal manual configuration.

</details>

<details><summary style="font-size:25px;color:Orange">Create a Custom VPC with Subnets</summary>

#### What We're Going to Create

We'll use a CIDR block of 10.0.0.0/16 for our VPC, and within this, we'll create the following subnets:

-   **Public Subnets**:

    -   Public Subnet 1A in us-east-1a with CIDR 10.0.1.0/24
    -   Public Subnet 1B in us-east-1b with CIDR 10.0.2.0/24

-   **Private Subnets**:
    -   Private Subnet 1A in us-east-1a with CIDR 10.0.3.0/24
    -   Private Subnet 1B in us-east-1b with CIDR 10.0.4.0/24

The public subnets will have an Internet Gateway attached for internet access, and we'll configure route tables accordingly.

#### Step-by-Step Guide

-   **Create the VPC**:

    -   Go to the AWS Management Console and navigate to Networking & Content Delivery > VPC.
    -   On the VPC dashboard, select Your VPCs.
    -   Click Create VPC.
    -   In the VPC creation screen, enter the following details:
        -   Name tag: Custom-VPC
        -   IPv4 CIDR block: 10.0.0.0/16
        -   Leave the IPv6 CIDR block and Tenancy as default (No IPv6 and default tenancy).
    -   Click Create VPC.
    -   Once created, go to Actions > Edit DNS hostnames and enable DNS hostnames for your VPC.

-   **Create the Subnets**:

    -   Navigate to Subnets in the VPC dashboard.
    -   Click Create subnet.
    -   Select your VPC (Custom-VPC) and enter the following details for each subnet:
    -   `Public Subnet 1A`:
        -   Name tag: Public-Subnet-1A
        -   Availability Zone: us-east-1a
        -   IPv4 CIDR block: 10.0.1.0/24
    -   `Public Subnet 1B`:
        -   Name tag: Public-Subnet-1B
        -   Availability Zone: us-east-1b
        -   IPv4 CIDR block: 10.0.2.0/24
    -   `Private Subnet 1A`:
        -   Name tag: Private-Subnet-1A
        -   Availability Zone: us-east-1a
        -   IPv4 CIDR block: 10.0.3.0/24
    -   `Private Subnet 1B`:
        -   Name tag: Private-Subnet-1B
        -   Availability Zone: us-east-1b
        -   IPv4 CIDR block: 10.0.4.0/24
    -   Click Create after entering the details for each subnet.

-   **Enable Auto-assign Public IP for Public Subnets**:

    -   For each public subnet, go to Actions > Modify auto-assign IP settings.
    -   Enable auto-assign public IPv4 addresses.

-   **Create Route Tables**:

    -   Navigate to Route Tables in the VPC dashboard.
    -   Click Create route table.
    -   Enter the following details for the private route table:
        -   Name tag: Private-RT
        -   VPC: Custom-VPC
    -   Click Create.
    -   For the private route table, go to Subnet associations > Edit subnet associations.
    -   Select Private Subnet 1A and Private Subnet 1B.

-   **Create an Internet Gateway**:

    -   Navigate to Internet Gateways in the VPC dashboard.
    -   Click Create Internet Gateway.
    -   Enter a name for the Internet Gateway: Custom-IGW.
    -   Click Create and then Actions > Attach to VPC.
    -   Select your VPC (Custom-VPC) and attach the Internet Gateway.

-   **Configure Routes for Public Subnets**:

    -   In the Route Tables section, select the main route table (the one associated with the public subnets).
    -   Go to Routes > Edit routes.
    -   Add a route with:
        -   Destination: 0.0.0.0/0
        -   Target: Select the Internet Gateway (Custom-IGW).
    -   Save the changes.

#### Summary

-   We created a custom VPC with a CIDR block of 10.0.0.0/16.
-   We created public and private subnets within two availability zones.
-   Configured auto-assign public IP for the public subnets.
-   Created route tables for routing traffic within the VPC.
-   Set up an Internet Gateway and configured routing for internet access for the public subnets.
-   Now you've set up a custom VPC with both public and private subnets, complete with proper routing and internet connectivity. In the next lesson, we'll deploy resources into this VPC and explore more advanced configurations. See you then!

</details>

<details><summary style="font-size:25px;color:Orange">Security Groups and Network ACL</summary>

Hi everyone! In this lesson, we're going to explore the differences between Security Groups and Network Access Control Lists (ACLs) in AWS. These are two types of firewalls you can use to control traffic in your AWS environment. Let's break down how they work and how to configure them.

-   **Security Groups**: Apply at the instance level, specifically at the network interface of an EC2 instance. They are stateful firewalls, meaning they automatically allow return traffic for an outgoing request.
-   **Network ACLs**: Apply at the subnet level and control ingress and egress traffic at the subnet boundary. They are stateless, meaning you need to explicitly allow both inbound and outbound traffic.

-   **Diagram Explanation**: Imagine we have a VPC with two availability zones. Each zone has both public and private subnets, and we have several EC2 instances launched into these subnets.

    -   `Network ACLs`
        -   Network ACLs are positioned at the edge of the subnets.
        -   All traffic entering and exiting a subnet passes through its Network ACL.
        -   They filter traffic for both ingress and egress.
    -   `Security Groups`
        -   Security Groups apply at the network interface of EC2 instances.
        -   They can be assigned to instances in different subnets.
        -   Security Groups filter traffic between instances in the same or different subnets.

-   **Stateful vs. Stateless Firewalls**

    -   Stateful Firewall (Security Groups): Tracks the state of connections. If an incoming request is allowed, the return traffic is automatically allowed.
    -   Stateless Firewall (Network ACLs): Does not track connections. Rules must explicitly allow both inbound and outbound traffic.

-   **Example Scenario**

    -   Consider a client connecting to a web server:

        -   Inbound Traffic: Client to Web Server
            -   Source Port: Dynamic high number (e.g., 65123)
            -   Destination Port: 80 (HTTP)
        -   Outbound Traffic: Web Server to Client
            -   Source Port: 80 (HTTP)
            -   Destination Port: Dynamic high number (e.g., 65123)

    -   In a stateful firewall (Security Group):

        -   Only an inbound rule for port 80 is needed. Return traffic is automatically allowed.

    -   In a stateless firewall (Network ACL):

        -   Both an inbound rule for port 80 and an outbound rule for the dynamic port are needed.

-   **Security Groups Configuration**

    -   Security Groups can have rules defined for both inbound and outbound traffic.
    -   They support only allow rules.
    -   They can use sources such as IP addresses, CIDR ranges, or other Security Group IDs.

-   **Best Practices for Security Groups**

    -   Public Subnet: Allow traffic from any source (0.0.0.0/0) to port 80 on the public-facing load balancer.
    -   Application Layer: Allow traffic only from the public load balancer’s Security Group to the application instances.
    -   Database Layer: (not shown) Allow traffic only from the application layer’s Security Group to the database instances.

-   **Network ACLs Configuration**

    -   Network ACLs can have both allow and deny rules.
    -   Rules are processed in numerical order, and the first matching rule is applied.
    -   If an allow rule is matched, subsequent deny rules are ignored.

-   **Example of Network ACL Rules**

    -   Inbound Rule: Allow HTTP traffic (port 80) from any IP.
    -   Outbound Rule: Allow traffic to any IP from port 80.

#### Summary

-   Security Groups: Best used for fine-grained control at the instance level. They are stateful and only need inbound rules for allowing return traffic.
-   Network ACLs: Best used for broad control at the subnet level. They are stateless and need explicit rules for both inbound and outbound traffic.

-   We discussed the differences between Security Groups and Network ACLs.

-   We covered how they function, their stateful/stateless nature, and how to configure them.

-   We looked at a practical example to understand how they handle traffic.

</details>
