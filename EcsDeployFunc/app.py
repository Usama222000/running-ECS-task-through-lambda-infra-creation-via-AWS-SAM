import json
import os
import boto3


def lambda_handler(event, context):
  cluster_name = os.environ['CLUSTER_NAME']
  subnet1='subnet-0d01a821f62f57b90'
  subnet2='subnet-08fee488f19c2be9f'
  sg='sg-0c7c3fdf7afa23db6'
  client = boto3.client('ecs')
  ec2 = boto3.client('ec2')
  log = boto3.client('logs')
  log_client = boto3.client('logs')
  ec2_client = boto3.client('ec2')
  ##check is task is in public subnet
  subnet_response = ec2.describe_subnets(
    Filters=[
        {
            'Name': 'subnet-id',
            'Values': [
               subnet1 ,
            ]
        },
    ],
  )
  chk_pub_subnet=subnet_response['Subnets'][0]['MapPublicIpOnLaunch']
  P_IP = ""
  if chk_pub_subnet:
    print("public")
    P_IP = "ENABLED"
  else:
    print("private")
    P_IP = "DISABLED"
  response = client.run_task(
  cluster= os.environ['CLUSTER_NAME'], 
  launchType = 'FARGATE',
  taskDefinition= os.environ['TASK_Def'], 
  count = 1,
  platformVersion='LATEST',
  networkConfiguration={
        'awsvpcConfiguration': {
            
            'subnets': [
                subnet1, 
                subnet2
            ],
             'securityGroups': [
                   sg
                ],
            'assignPublicIp': P_IP
        }
    })
  task_arn = response['tasks'][0]['taskArn']
  waiter = client.get_waiter('tasks_running')
  waiter.wait(cluster=os.environ['CLUSTER_NAME'], tasks=[task_arn])

  task_status = response['tasks'][0]['lastStatus']
  container_arn = response['tasks'][0]['containers'][0]['containerArn']
  response = log.describe_log_streams (
    logGroupName='usama-cloudwatch-log-group',
    logStreamNamePrefix='usama-task-definition',
    descending=True)
  log_stream_name = response['logStreams'][0]['logStreamName']
  response = log.get_log_events(
    logGroupName='usama-cloudwatch-log-group',
    logStreamName=log_stream_name
  )
  for event in response['events']:
    print(event['message'])
  return {
            'statusCode': 200,
            'body': '{ "response": "' + str(event['message']) + '"}'
        }