# AWS Lambda Cheatsheet

<h3>This cheatsheet is probably based on Python Written in 2021</h3>

<br>

<table>
  <tr>
    <th colspan="4">Runtime Versions</th>
  </tr>
  <tr>
    <th>Type</th>
    <th>Versions</th>
    <th>AWS SDK</th>
    <th>Operating System</th>
  </tr>
<!-- NodeJS -->
  <tr>
    <td rowspan="2">Node.js</td>
    <td>nodejs10.x</td>
    <td>(JavaScript) 2.712.0</td>
    <td>Amazon Linux 2</td>
  </tr>
  <tr>
    <td>nodejs12.x</td>
    <td>(JavaScript) 2.712.0</td>
    <td>Amazon Linux 2</td>
  </tr>

<!-- Java -->
  <tr>
    <td rowspan="3">Java</td>
    <td>java11</td>
    <td>(JDK) amazon-corretto-11</td>
    <td>Amazon Linux 2</td>
  </tr>
  <tr>
    <td>java8.a12</td>
    <td>(JDK) amazon-corretto-8</td>
    <td>Amazon Linux 2</td>
  </tr>
  <tr>
    <td>java8</td>
    <td>(JDK) java-1.8.0-openjdk</td>
    <td>Amazon Linux</td>
  </tr>

<!-- Python -->
  <tr>
    <td rowspan="4">Python</td>
    <td>python3.8</td>
    <td>(Python) boto3-1.14.40 botocore-1.17.40</td>
    <td>Amazon Linux 2</td>
  </tr>
  <tr>
    <td>python3.7</td>
    <td>(Python) boto3-1.14.40 botocore-1.17.40</td>
    <td>Amazon Linux</td>
  </tr>
  <tr>
    <td>python3.6</td>
    <td>(Python) boto3-1.14.40 botocore-1.17.40</td>
    <td>Amazon Linux</td>
  </tr>
  <tr>
    <td>python2.7</td>
    <td>(Python) boto3-1.14.40 botocore-1.17.40</td>
    <td>Amazon Linux</td>
  </tr>

<!-- Ruby -->
  <tr>
    <td rowspan="2">Ruby</td>
    <td>ruby2.7</td><td>(Ruby) 3.0.3</td>
    <td>Amazon Linux 2</td>
  </tr>
  <tr>
    <td>ruby2.5</td>
    <td>(Ruby) 3.0.3</td>
    <td>Amazon Linux</td>
  </tr>

<!-- .NET -->
  <tr>
    <td rowspan="2">.NET Core</td>
    <td>dotnetcore3.1</td>
    <td>--</td>
    <td>Amazon Linux 2</td>
  </tr>
  <tr>
    <td>dotnetcore2.1</td>
    <td>--</td>
    <td>Amazon Linux</td>
  </tr>

<!-- Go -->
  <tr>
    <td>Go</td>
    <td>go1.x</td>
    <td>--</td>
    <td>Amazon Linux</td>
  </tr>

<!-- Custom runtime -->
  <tr>
    <td rowspan="2">Custom Runtime</td>
    <td>provided.al2</td>
    <td>--</td>
    <td>Amazon Linux 2</td>
  </tr>
  <tr>
    <td>provided</td>
    <td>--</td>
    <td>Amazon Linux</td>
  </tr>
</table>

<br>

<table>
  <tr>
    <th colspan="4">Available Operating System</th>
  </tr>
  <tr>
    <th>Type</th>
    <th>Image</th>
    <th>Kernel</th>
  </tr>
  <tr>
    <td>Amazon Linux</td>
    <td>amzn-ami-hvm-2018.03.0.20181129-x86_64-gp2</td>
    <td>4.14.171-105.231.amzn1.x86_64</td>
  </tr>
  <tr>
    <td>Amazon Linux 2</td>
    <td>Custom</td>
    <td>4.14.165-102.205.amzn2.x86_64</td>
  </tr>
</table>

<br>

<table>
  <tr>
    <th colspan="3">Settings | Limits</th>
  </tr>
  <tr>
    <th>Description</th>
    <th>Settings | Limits | Explained</th>
    <th>Can be increased</th>
  </tr>
  <tr>
    <td>
      <b>Writable Path & Space</b>
    </td>
    <td>/tmp/ 512 MB</td>
    <td>--</td>
  </tr>
  <tr>
    <td><b>Default Memory & Execution Time</b></td>
    <td>128 MB Memory<br>3 Second Timeout</td>
    <td>--</td>
  </tr>
  <tr>
    <td><b>Max Memory & Execution Time</b></td>
    <td>10,240 MB (1 MB increments)<br>900 seconds (15 Minutes) Timeout</td>
    <td>--</td>
  </tr>
  <tr>
    <td><b>Number of processes and threads (Total)</b></td>
    <td>1024</td>
    <td>--</td>
  </tr>
  <tr>
    <td><b>Number of File descriptors (Total)</b></td>
    <td>1024</td>
    <td>--</td>
  </tr>
  <tr>
    <td><b>Maximum deployment package size</b></td>
    <td>
      <br>50 MB (zipped, direct upload)
      <br>250 MB (unzipped, including layers)
    </td>
    <td>--</td>
  </tr>
  <tr>
    <td><b><a href="https://youtu.be/23fE57EFRK4">Container image</a> code package size</b></td>
    <td>
      <br>10 GB
    </td>
    <td>--</td>
  </tr>
  <tr>
    <td><b>Maximum deployment package size for console editor</b></td>
    <td>3 MB</td>
    <td>--</td>
  </tr>
  <tr>
    <td><b>Total size of deployment package per region</b></td>
    <td>75 GB</td>
    <td>Can be increased upto Terabytes</td>
  </tr>
  <tr>
    <td><b>Maximum size of environment variables set</b></td>
    <td>4 KB</td>
    <td>--</td>
  </tr>
  <tr>
    <td><b>Maximum function Layers</b></td>
    <td>5 layers</td>
    <td>--</td>
  </tr>
  <tr>
    <td><b>Environment variables size</b></td>
    <td>4 KB</td>
    <td>--</td>
  </tr>
  <tr>
    <td><b>Maximum test events (Console editor)</b></td>
    <td>10</td>
    <td>--</td>
  </tr>
  <tr>
    <td><b>Invocation payload Limit (request and response)</b></td>
    <td>6 MB (synchronous)<br>256 KB (asynchronous)</td>
    <td>--</td>
  </tr>
  <tr>
    <td><b>Elastic network interpaces per VPC</b></td>
    <td>250</td>
    <td>Can be increased upto Hundreds</td>
  </tr>
  <tr>
    <td><b>Lambda Destinations</b></td>
    <td>
      <ul>
        <li>It sends invocation records to a destination (SQS queue, SNS topic, Lambda function, or EventBridge event bus) when the lambda function is invoked asynchronously</li>
        <li>It also supports stream invocation</li>
      </ul>
    </td>
    <td>Can be increased upto Hundreds</td>
  </tr>
  <tr>
    <td><b>Monitoring tools</b></td>
    <td>
      <ul>
        <li>(Default) CloudWatch Logs stream</li>
        <li>AWS X-Ray</li>
        <li>CloudWatch Lambda Insights (preview)</li>
      </ul>
    </td>
    <td>--</td>
  </tr>
  <tr>
    <td><b>VPC</b></td>
    <td>
      <ul>
        <li>When you enable VPC, your Lambda function will lose default internet access</li>
        <li>If you require external internet access for your function, ensure that your security group allows outbound connections and that your VPC has a NAT gateway</li>
      </ul>
    </td>
    <td>--</td>
  </tr>
  <tr>
    <td><b>Concurrency</b></td>
    <td>
      <ul>
        <li>Concurrent Execution refers to the execution of number of function at a given time. By default the limit is 1000  across all function within a given region</li>
        <li>AWS Lambda keeps 100 for the unreserved function</li>
        <li>So, if there are 1000 then you can select from 900 and reserve concurrency for selected function and rest 100 is used for the unreserved function</li>
      </ul>
    <td>Can be increased upto Hundreds of thousands</td>
  </tr>
  <tr>
    <td><b>DLQ (Dead Letter Queue)</td>
    <td>
      <ul>
        <li>Failed Lambda is invoked twice by default and the event is discarded</li>
        <li>DLQ instruct lamnda to send unprocessed events to AWS SQS or AWS SNS</li>
        <li>DLQ helps you troubleshoot and examine the unprocessed request</li>
      </ul>
    <td>--</td>
  </tr>
  <tr>
    <td><b>Throttle</b></td>
    <td>
      <ul>
        <li>Throttle will set reserved concurrency of the function to zero and it will throttle all future invocation</li>
        <li>If the function is throttled then it will fail to run</li>
        <li>If the fucntion is ran from Lambda console then it will throw "Calling the Invoke API failed with message: Rate Exceeded."</li>
      </ul>
    <td>--</td>
  </tr>
  <tr>
    <td><b>File system</b></td>
    <td>
      <ul>
        <li><a href="https://www.youtube.com/playlist?list=PL5KTLzN85O4L0rYTtGVKxPr4yQ5oHMYOn">File system</a> will allow you to add Amazon EFS file system, which provides distributed network storage for the instances of the function</li>
        <li>To connect to the file system, you need to connect your lambda function to VPC</li>
      </ul>
    <td>--</td>
  </tr>
  <tr>
    <td><b>State machines</b></td>
    <td>
      <ul>
        <li>Step Functions state machines which orchestrate this function</li>
        <li>The Step Functions state machines page lists all state machines in the current AWS region with at least one workflow step that invokes a Lambda function</li>
      </ul>
    <td>--</td>
  </tr>
  <tr>
    <td><b>Database proxies</b></td>
    <td>
      <ul>
        <li>Database proxy manages a pool of database connections and relays queries from a function</li>
        <li>It uses Secrets Manager secret to access credentials for a database</li>
        <li>To connect to the file system, you need to connect your lambda function to VPC</li>
      </ul>
    <td>--</td>
  </tr>
</table>
<br>
<table>
  <tr>
    <th colspan=2>Execution Role (Common Execution Role Available)</th>
  </tr>
  <tr>
    <td><b>AWSLambdaBasicExecutionRole</b></td>
    <td>Grants permissions only for the Amazon CloudWatch Logs actions to write logs.</td>
  </tr>
  <tr>
    <td><b>AWSLambdaKinesisExecutionRole</b></td>
    <td>Grants permissions for Amazon Kinesis Streams actions, and CloudWatch Logs actions.</td>
  </tr>
  <tr>
    <td><b>AWSLambdaDynamoDBExecutionRole</b></td>
    <td>Grants permissions for DynamoDB streams actions and CloudWatch Logs actions.</td>
  </tr>
  <tr>
    <td><b>AWSLambdaVPCAccessExecutionRole</b></td>
    <td>Grants permissions for Amazon Elastic Compute Cloud (Amazon EC2) actions to manage elastic network interfaces (ENIs).</td>
  </tr>
  <tr>
    <td><b>AWSXrayWriteOnlyAccess</b></td>
    <td>Grants permission for X-ray to to upload trace data to debug and analyze.</td>
  </tr>
</table>
<br>
<b>Add new permission</b>

    import boto3
    client = boto3.client('lambda')

    # Role ARN can be found on the top right corner of the Lambda function
    response = client.add_permission(
        FunctionName='string',
        StatementId='string',
        Action='string',
        Principal='string',
        SourceArn='string',
        SourceAccount='string',
        EventSourceToken='string',
        Qualifier='string'
    )

<br>
<table>
  <tr>
    <th colspan="2">Execution | Invoke | Tweaks</th>
  </tr>
  <tr>
    <td>A Lambda can invoke another Lambda</td>
    <td><a href="https://youtu.be/5QwrseYLwNM">Yes</a></td>
  </tr>
  <tr>
    <td>A Lambda in one region can invoke another lambda in other region</td>
    <td>Yes</td>
  </tr>
  <tr>
    <td>A Lambda can invoke same Lambda</td>
    <td>Yes</td>
  </tr>
  <tr>
    <td>Exceed 15 minutes execution time</td>
    <td>Yes (Can Tweak around)</td>
  </tr>
  <tr>
    <td>How to exceed 5 minutes execution time</td>
    <td> <a href="http://www.thetechnologyupdates.com/aws-lambda-going-beyond-5-minutes-execution/">Self-Invoke</a> , SNS, SQS</td>
  </tr>
  <tr>
    <td>Asynchronous Execution</td>
    <td>Yes <a href="http://www.thetechnologyupdates.com/aws-lambda-execute-lambda-asynchronously-parallel/">(Async Exec)</a></td>
  </tr>
  <tr>
    <td>Invoke same Lamba with different version</td>
    <td>Yes</td>
  </tr>
  <tr>
    <td>Setting Lambda Invoke Max Retry attempt to 0</td>
    <td><a href="https://youtu.be/ySVz-9EOKbw">Yes</a></td>
  </tr>
</table>
<br>

<table>
  <tr>
    <th>Triggers</th>
    <th>Description</th>
    <th>Requirement</th>
  </tr>
  <tr>
    <td><b>API Gateway</b></td>
    <td>Trigger AWS Lambda function over HTTPS</td>
    <td>API Endpoint name<br>API Endpoint Deployment Stage<br>Security Role</td>
  </tr>
  <tr>
    <td><b>AWS IoT</b></td>
    <td>Trigger AWS Lambda for performing specific action by mapping your AWS IoT Dash Button (Cloud Programmable Dash Button)</td>
    <td>DSN (Device Serial Number)</td>
  </tr>
  <tr>
    <td><b>Alexa Skill Kit</b></td>
    <td>Trigger AWS Lambda to build services that give new skills to Alexa</td>
    <td>--</td>
  </tr>
  <tr>
    <td><b>Alexa Smart Home</b></td>
    <td>Trigger AWS Lambda with desired skill</td>
    <td>Application ID (Skill)</td>
  </tr>
  <tr>
    <td><b>Application Load Balancer</b></td>
    <td>Trigger AWS Lambda from ALB</td>
    <td>Application Load Balancer<br>Listener (It is the port that ALP receivce traffice)<br>Host<br>Path</td>
  </tr>
  <tr>
    <td><b>CloudFront</b></td>
    <td>Trigger AWS Lambda based on difference CloudFront event.</td>
    <td>CloudFront distribution, Cache behaviour, CloudFront event (Origin request/response, Viewer request/response).<br>To set CloudFront trigger, one need to publish the version of Lambda.<br><b>Limitations:</b><br>Runtime is limited to Node.js 6.10<br>/tmp/ space is not available<br>Environment variables, DLQ & Amazon VPC's cannot be used</td>
  </tr>
  <tr>
    <td><b>CloudWatch Events</b></td>
    <td>Trigger AWS Lambda on desired time interval (rate(1 day)) or on the state change of EC2, RDS, S3, Health.</td>
    <td>Rule based on either Event Pattern (time interval)<br>Schedule Expression (Auto Scaling on events like Instance launch and terminate<br>AWS API call via CloudTrail</td>
  </tr>
  <tr>
    <td><b>CloudWatch Logs</b></td>
    <td>Trigger AWS Lambda based on the CloudWatch Logs</td>
    <td>Log Group Name</td>
  </tr>
  <tr>
    <td><b>Code Commit</b></td>
    <td>Trigger AWS Lambda based on the AWS CodeCommit version control system</td>
    <td>Repository Name<br>Event Type</td>
  </tr>
  <tr>
    <td><b>Cognito Sync Trigger</b></td>
    <td>Trigger AWS Lambda in response to event, each time the dataset is synchronized</td>
    <td>Cognito Identity Pool dataset</td>
  </tr>
  <tr>
    <td><b>DynamoDB</b></td>
    <td>Trigger AWS Lambda whenever the DynomoDB table is updated</td>
    <td>DynamoDB Table name<br>Batch Size(The largest number of records that AWS Lambda will retrieve from your table at the time of invoking your function. Your function receives an event with all the retrieved records)</td>
  </tr>
  <tr>
    <td><b>Kinesis</b></td>
    <td>Trigger AWS Lambda whenever the Kinesis stream is updated</td>
    <td>Kinesis Stream<br>Batch Size</td>
  </tr>
  <tr>
    <td><b>S3</b></td>
    <td>Trigger AWS Lambda in response to file dropped in S3 bucket</td>
    <td>Bucket Name<br>Event Type (Object Removed, Object Created)</td>
  </tr>
  <tr>
    <td><b>SNS</b></td>
    <td>Trigger AWS Lambda whenever the message is published to Amazon SNS Topic</td>
    <td>SNS Topic</td>
  </tr>
  <tr>
    <td><b>SQS</b></td>
    <td>Trigger AWS Lambda on message arrival in SQS</td>
    <td>SQS queue<br>Batch size<br><b>Limitation:</b> It only works with Standard queue and not FIFO queue</td>
  </tr>
</table>
<br>
<table>
  <tr>
    <th colspan="3">Troubleshooting</th>
  </tr>
  <tr>
    <th>Error</th>
    <th>Possible Reason</th>
    <th>Solution</th>
  </tr>
  <tr>
    <td>
    File "/var/task/lambda_function.py", line 2, in lambda_handler<br>return event['demoevent']<br>
    KeyError: 'demoevent'
    </td>
    <td>
      Event does not have the key 'demoevent' or either misspelled
    </td>
    <td>
      Make sure the event is getting the desired key if it is receiving the event from any trigger.<br> Or if the not outside event is passed than check for misspell.<br>Or check the event list by printing event.
    </td>
  </tr>
  <tr>
    <td>botocore.exceptions.ClientError: An error occurred (AccessDeniedException) when calling the GetParameters operation: User: arn:aws:dummy::1234:assumed-role/role/ is not authorized to perform: ssm:GetParameters on resource: arn:aws:ssm:dummy</td>
    <td>Lacks Permission to access</td>
    <td>Assign appropriate permission for accessibility</td>
  </tr>
  <tr>
    <td>ImportError: Missing required dependencies [‘module']</td>
    <td>Dependent module is missing</td>
    <td>Install/Upload the required module</td>
  </tr>
  <tr>
    <td>sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) could not translate host name "host.dummy.region.rds.amazonaws.com" to address: Name or service not known</td>
    <td>RDS Host is unavailable</td>
    <td>Make sure the RDS instance is up and running.<br>Double check the RDS hostname</td>
  </tr>
  <tr>
    <td>[Errno 32] Broken pipe</td>
    <td>Connection is lost (Either from your side or may be some problem from AWS)<br>While invoking another Lambda, if the payload size exceed the mentioned limit</td>
    <td>Make sure if you are passing the payload of right size.<br>Check for the connection.</td>
  </tr>
  <tr>
    <td>Unable to import module ‘lambda_function/index’ No module named ‘lambda_function'</td>
    <td>Handler configuration is not matching the main file name</td>
    <td>Update the handler configuration as per your filename.function_name</td>
  </tr>
  <tr>
    <td>OperationalError: (psycopg2.OperationalError) terminating connection due to administrator command
SSL connection has been closed unexpectedly</td>
    <td>RDS/Database System has been rebooted.<br>In a typical web application using an ORM (SQLAlchemy) Session, the above condition would correspond to a single request failing with a 500 error, then the web application continuing normally beyond that. Hence the approach is “optimistic” in that frequent database restarts are not anticipated.</td>
    <td>Give second try</td>
  </tr>
  <tr>
    <td>Error code 429</td>
    <td>The function is throttled. Basically the reserved concurrency is set to zero or it have reach the account level throttle. <br>(The function that is invoked synchronous and if it is throttled then it will return 429 error. If the lambda function is invoked asynchronously and if it is throttled then it will retry the throttled event for upto 6 hours.) </td>
    <td>Check for the reserved concurrency limit or throttle status for the individual function. Or check for the account level concurrent execution limit</td>
  </tr>
</table>
<br>
<h3>AWS Lambda CLI commands</h3>
<br>
<b>Add Permission</b>
<p>It add mention permission to the Lambda function</p>
<p>Syntax</p>

      add-permission
    --function-name <value>
    --statement-id <value>
    --action <value>
    --principal <value>
    [--source-arn <value>]
    [--source-account <value>]
    [--event-source-token <value>]
    [--qualifier <value>]
    [--cli-input-json <value>]
    [--generate-cli-skeleton <value>]

<p>Example</p>

    add-permission --function-name functionName --statement-id role-statement-id --action lambda:CreateFunction --principal s3.amazonaws.com

<br>
<b>Create Alias</b>
<p>It creates alias for the given Lambda function name</p>
<p>Syntax</p>

      create-alias
    --function-name <value>
    --name <value>
    --function-version <value>
    [--description <value>]
    [--cli-input-json <value>]
    [--generate-cli-skeleton <value>]

<p>Example</p>

    create-alias --function-name functionName --name fliasName --function-version version

<br>
<b>Create Event Source Mapping</b>
<p>It identify event-source from Amazon Kinesis stream or an Amazon DynamoDB stream</p>

      create-event-source-mapping
    --event-source-arn <value>
    --function-name <value>
    [--enabled | --no-enabled]
    [--batch-size <value>]
    --starting-position <value>
    [--starting-position-timestamp <value>]
    [--cli-input-json <value>]
    [--generate-cli-skeleton <value>]

<p>Example</p>

    create-event-source-mapping --event-source-arn arn:aws:kinesis:us-west-1:1111 --function-name functionName --starting-position LATEST

<br>
<b>Create Function</b>
<p>It creates the new function</p>
<p>Syntax</p>

      create-function
    --function-name <value>
    --runtime <value>
    --role <value>
    --handler <value>
    [--code <value>]
    [--description <value>]
    [--timeout <value>]
    [--memory-size <value>]
    [--publish | --no-publish]
    [--vpc-config <value>]
    [--dead-letter-config <value>]
    [--environment <value>]
    [--kms-key-arn <value>]
    [--tracing-config <value>]
    [--tags <value>]
    [--zip-file <value>]
    [--cli-input-json <value>]
    [--generate-cli-skeleton <value>]

<p>Example</p>

    create-function --function-name functionName --runtime python3.6 --role arn:aws:iam::account-id:role/lambda_basic_execution
     --handler main.handler

<br>
<b>Delete Alias</b>
<p>It deletes the alias</p>
<p>Syntax</p>

      delete-alias
    --function-name <value>
    --name <value>
    [--cli-input-json <value>]
    [--generate-cli-skeleton <value>]

<p>Example</p>

    delete-alias --function-name functionName --name aliasName

<br>
<b>Delete Event Source Mapping</b>
<p>It deletes the event source mapping</p>
<p>Syntax</p>

      delete-event-source-mapping
    --uuid <value>
    [--cli-input-json <value>]
    [--generate-cli-skeleton <value>]

<p>Example</p>
    
    delete-event-source-mapping --uuid 12345kxodurf3443
<br>
<b>Delete Function</b>
<p>It will delete the function and all the associated settings</p>
<p>Syntax</p>

      delete-function
    --function-name <value>
    [--qualifier <value>]
    [--cli-input-json <value>]
    [--generate-cli-skeleton <value>]

<p>Example</p>

    delete-function --function-name FunctionName

<br>
<b>Get Account Settings</b>
<p>It will fetch the user’s account settings</p>
<p>Syntax</p>

      get-account-settings
    [--cli-input-json <value>]
    [--generate-cli-skeleton <value>]

<br>
<b>Get Alias</b>
<p>It returns the desired alias information like description, ARN</p>
<p>Syntax</p>

      get-alias
    --function-name <value>
    --name <value>
    [--cli-input-json <value>]
    [--generate-cli-skeleton <value>]

<p>Example</p>

    get-alias --function-name functionName --name aliasName

<br>
<b>Get Event Source Mapping</b>
<p>It returns the config information for the desired event source mapping</p>
<p>Syntax</p>

      get-event-source-mapping
    --uuid <value>
    [--cli-input-json <value>]
    [--generate-cli-skeleton <value>]

<p>Example</p>
    
    get-event-source-mapping --uuid 12345kxodurf3443
<br>
<b>Get Function</b>
<p>It returns the Lambda Function information</p>
<p>Syntax</p>

      get-function
    --function-name <value>
    [--qualifier <value>]
    [--cli-input-json <value>]
    [--generate-cli-skeleton <value>]

<p>Example</p>
    
    get-function --function-name functionName
<br>
<b>Get Function Configuration</b>
<p>It returns the Lambda function configuration</p>
<p>Syntax</p>

      get-function-configuration
    --function-name <value>
    [--qualifier <value>]
    [--cli-input-json <value>]
    [--generate-cli-skeleton <value>]

<p>Example</p>

      get-function-configuration --function-name functionName

<br>
<b>Get Policy</b>
<p>It return the linked policy with Lambda function</p>
<p>Syntax</p>

      get-policy
    --function-name <value>
    [--qualifier <value>]
    [--cli-input-json <value>]
    [--generate-cli-skeleton <value>]

<p>Example</p>

    get-policy --function-name functionName

<br>
<b>Invoke</b>
<p>It invoke the mention Lambda function name</p>
<p><Syntax/p>

      invoke
    --function-name <value>
    [--invocation-type <value>]
    [--log-type <value>]
    [--client-context <value>]
    [--payload <value>]
    [--qualifier <value>]

<p>Example</p>

    invoke --function-name functionName

<br>
<b>List Aliases</b>
<p>It return all the aliases that is created for Lambda function</p>
<p>Syntax</p>

      list-aliases
    --function-name <value>
    [--function-version <value>]
    [--marker <value>]
    [--max-items <value>]
    [--cli-input-json <value>]
    [--generate-cli-skeleton <value>]

<p>Example</p>

      list-aliases --function-name functionName

<br>
<b>List Event Source Mappings</b>
<p>It return all the list event source mappings that is created with create-event-source-mapping</p>
<p>Syntax</p>

      list-event-source-mappings
    [--event-source-arn <value>]
    [--function-name <value>]
    [--max-items <value>]
    [--cli-input-json <value>]
    [--starting-token <value>]
    [--page-size <value>]
    [--generate-cli-skeleton <value>]

<p>Example</p>

      list-event-source-mappings --event-source-arn arn:aws:arn --function-name functionName

<br>
<b>List Functions</b>
<p>It return all the Lambda function</p>
<p>Syntax</p>

      list-functions
    [--master-region <value>]
    [--function-version <value>]
    [--max-items <value>]
    [--cli-input-json <value>]
    [--starting-token <value>]
    [--page-size <value>]
    [--generate-cli-skeleton <value>]

<p>Example</p>

      list-functions --master-region us-west-1 --function-version ALL

<br>
<b>List Tags</b>
<p>It return the list of tags that are assigned to the Lambda function</p>
<p>Syntax</p>

      list-tags
    --resource <value>
    [--cli-input-json <value>]
    [--generate-cli-skeleton <value>]

<p>Example</p>

      list-tags --resource arn:aws:function

<br>
<b>List Versions by functions</b>
<p>It return all the versions of the desired Lambda function</p>
<p>Syntax</p>

      list-versions-by-function
    --function-name <value>
    [--marker <value>]
    [--max-items <value>]
    [--cli-input-json <value>]
    [--generate-cli-skeleton <value>]

<p>Example</p>

    list-versions-by-function --function-name functionName

<br>
<b>Publish Version</b>
<p>It publish the version of the Lambda function from $LATEST snapshot</p>
<p>Syntax</p>

      publish-version
    --function-name <value>
    [--code-sha-256 <value>]
    [--description <value>]
    [--cli-input-json <value>]
    [--generate-cli-skeleton <value>]

<p>Example</p>

      publish-version --function-name functionName

<br>
<b>Remove Permission</b>
<p>It remove the single permission from the policy that is linked with the Lambda function</p>
<p>Syntax</p>

     remove-permission
    --function-name <value>
    --statement-id <value>
    [--qualifier <value>]
    [--cli-input-json <value>]
    [--generate-cli-skeleton <value>]

<p>Example</p>

     remove-permission --function-name functionName --statement-id role-statement-id

<br>
<b>Tag Resource</b>
<p>It creates the tags for the lambda function in the form of key-value pair</p>
<p>Syntax</p>

      tag-resource
    --resource <value>
    --tags <value>
    [--cli-input-json <value>]
    [--generate-cli-skeleton <value>]

<p>Example</p>

    tag-resource --resource arn:aws:arn --tags {‘key’: ‘pair’}

<br>
<b>Untag Resource</b>
<p>It remove tags from the Lambda function</p>
<p>Syntax</p>

     untag-resource
    --resource <value>
    --tag-keys <value>
    [--cli-input-json <value>]
    [--generate-cli-skeleton <value>]

<p>Example</p>

    untag-resource --resource arn:aws:complete --tag-keys [‘key1’, ‘key2’]

<br>
<b>Update Alias</b>
<p>It update the alias name of the desired lambda function</p>
<p>Syntax</p>

      update-alias
    --function-name <value>
    --name <value>
    [--function-version <value>]
    [--description <value>]
    [--cli-input-json <value>]
    [--generate-cli-skeleton <value>]

<p>Example</p>

    update-alias --function-name functionName --name aliasName

<br>
<b>Update Event Source Mapping</b>
<p>It updates the event source mapping incase you want to change the existing parameters</p>
<p>Syntax</p>

      update-event-source-mapping
    --uuid <value>
    [--function-name <value>]
    [--enabled | --no-enabled]
    [--batch-size <value>]
    [--cli-input-json <value>]
    [--generate-cli-skeleton <value>]

<p>Example</p>

    update-event-source-mapping --uuid 12345kxodurf3443

<br>
<b>Update Function Code</b>
<p>It updates the code of the desired Lambda function</p>
<p>Syntax</p>

      update-function-code
    --function-name <value>
    [--zip-file <value>]
    [--s3-bucket <value>]
    [--s3-key <value>]
    [--s3-object-version <value>]
    [--publish | --no-publish]
    [--dry-run | --no-dry-run]
    [--cli-input-json <value>]
    [--generate-cli-skeleton <value>]

<p>Example</p>

    update-function-code --function-name functionName

<br>
<b>Update Function Configuration</b>
<p>It updates the configuration of the desired Lambda function</p>
<p>Syntax</p>

      update-function-configuration
    --function-name <value>
    [--role <value>]
    [--handler <value>]
    [--description <value>]
    [--timeout <value>]
    [--memory-size <value>]
    [--vpc-config <value>]
    [--environment <value>]
    [--runtime <value>]
    [--dead-letter-config <value>]
    [--kms-key-arn <value>]
    [--tracing-config <value>]
    [--cli-input-json <value>]
    [--generate-cli-skeleton <value>]

<p>Example</p>

    update-function-configuration --function-name functionName

<br>
<h4>References</h4>
<ul>
  <li><a href="https://aws.amazon.com/documentation/lambda/">AWS Lambda Docs</a></li>
  <li><a href="https://boto3.readthedocs.io/en/latest/">Boto 3 Docs</a></li>
  <li><a href="http://docs.aws.amazon.com/cli/latest/reference/lambda/">AWS CLI Docs</a></li>
  <li><a href="http://docs.sqlalchemy.org">SQLAlchemy Docs</a></li>
</ul>
<br>
<b>For queries or issues, feel free to contact or open an <a href="https://github.com/srcecde/aws-lambda-cheatsheet/issues">issue</a></b>
