# AWS SAM Template for Fargate Deployment

This AWS SAM template sets up an ECS Fargate Task Definition and a Lambda function that interacts with it.

## SAM Template Explanation

### SAM Template Sections

- **AWSTemplateFormatVersion**: Defines the AWS CloudFormation template version.
- **Transform**: Indicates the CloudFormation transform to apply (in this case, AWS Serverless Application Model).
- **Description**: Provides a description of the template.

### Globals

Defines global configurations for functions and APIs.

- Function:
  - Timeout: 3 seconds
  - MemorySize: 128 MB
  - Tracing: Active
- API:
  - TracingEnabled: Enabled

### Resources

#### MyTaskDefinition

Defines an ECS Task Definition for the Fargate launch type.

- Uses an existing execution role.
- Specifies resource requirements, image, ports, and logging configuration.

#### LogGroup

Creates a CloudWatch Log Group for logging.

#### ECSCluster

Creates an ECS Cluster with Fargate and Fargate Spot capacity providers.

#### EcsDeployFunction

Defines a Lambda function with required permissions.

- Code is located in the `EcsDeployFunc/` directory.
- It interacts with ECS to run tasks.

### Outputs

- **HelloWorldApi**: API Gateway endpoint URL for Prod stage for Hello World function.
- **HelloWorldFunction**: Hello World Lambda Function ARN.
- **HelloWorldFunctionIamRole**: Implicit IAM Role created for Hello World function.

## Lambda Function Explanation

The Lambda function (`EcsDeployFunc/app.py`) is written in Python. It interacts with ECS to run a Fargate task.

- Retrieves necessary environment variables (Cluster name, Task Definition ARN).
- Uses Boto3 to interact with AWS services (ECS, EC2, CloudWatch Logs).

## How to Use

1. Make sure you have the necessary IAM roles and permissions set up.
2. Deploy the SAM template using AWS CLI or CloudFormation console.
3. Once deployed, you can invoke the Lambda function, which will interact with ECS to run tasks.
