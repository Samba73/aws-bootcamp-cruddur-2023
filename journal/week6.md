# Week 6 — Deploying Containers

Before ECS cluster, ECR (Elastic Container Repository) in AWS was updated with images for
1) Node (required for Frontend React)
2) Python (required for Backend image)
3) Nginx (Server for Frontend to run)
4) Frontend (React)
5) Backend (Flask)

To log in into ECR run this command in terminal

```
aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com"
```

Create repositories in ECR
```
aws ecr create-repository \
  --repository-name cruddur/backend-flask

aws ecr create-repository \
  --repository-name cruddur/frontend-react-js
```
Update the Dockerfile - Here the base image which is node is already created locally and pushed to ECR

```
# Base Image ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
FROM 623053391718.dkr.ecr.ap-southeast-1.amazonaws.com/cruddur-node:16.18 AS build

ARG REACT_APP_BACKEND_URL
ARG REACT_APP_AWS_PROJECT_REGION
ARG REACT_APP_AWS_COGNITO_REGION
ARG REACT_APP_AWS_USER_POOLS_ID
ARG REACT_APP_CLIENT_ID

ENV REACT_APP_BACKEND_URL=$REACT_APP_BACKEND_URL
ENV REACT_APP_AWS_PROJECT_REGION=$REACT_APP_AWS_PROJECT_REGION
ENV REACT_APP_AWS_COGNITO_REGION=$REACT_APP_AWS_COGNITO_REGION
ENV REACT_APP_AWS_USER_POOLS_ID=$REACT_APP_AWS_USER_POOLS_ID
ENV REACT_APP_CLIENT_ID=$REACT_APP_CLIENT_ID

COPY . ./frontend-react-js
WORKDIR /frontend-react-js
RUN npm install
RUN npm run build

# New Base Image ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
FROM 623053391718.dkr.ecr.ap-southeast-1.amazonaws.com/cruddur-nginx:1.23.3-alpine

# --from build is coming from the Base Image
COPY --from=build /frontend-react-js/build /usr/share/nginx/html
COPY --from=build /frontend-react-js/nginx.conf /etc/nginx/nginx.conf

EXPOSE 3000
```

For Frontend we need the nginx server, the nginx configuration need to be updated for Cruddur app as below
```
# Set the worker processes
worker_processes 1;

# Set the events module
events {
  worker_connections 1024;
}

# Set the http module
http {
  # Set the MIME types
  include /etc/nginx/mime.types;
  default_type application/octet-stream;

  # Set the log format
  log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

  # Set the access log
  access_log  /var/log/nginx/access.log main;

  # Set the error log
  error_log /var/log/nginx/error.log;

  # Set the server section
  server {
    # Set the listen port
    listen 3000;

    # Set the root directory for the app
    root /usr/share/nginx/html;

    # Set the default file to serve
    index index.html;

    location / {
        # First attempt to serve request as file, then
        # as directory, then fall back to redirecting to index.html
        try_files $uri $uri/ $uri.html /index.html;
    }

    # Set the error page
    error_page  404 /404.html;
    location = /404.html {
      internal;
    }

    # Set the error page for 500 errors
    error_page  500 502 503 504  /50x.html;
    location = /50x.html {
      internal;
    }
  }
}
```

Backend-flask Docker file - Python image already created locally and pushed to ECR
```
FROM 623053391718.dkr.ecr.ap-southeast-1.amazonaws.com/cruddur-python:latest    

WORKDIR /backend-flask

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .


ENV ROLLBAR_ACCESS_TOKEN='644e2ee76ca64c2eb5cbc5f1c7021483'

EXPOSE ${PORT}

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=4567","--no-debug", "--no-debugger", "--no-reload" ]
```
### Deploy an ECS Cluster using ECS Service Connect

1) Create cluster
     i) Provide cluster name
     ii) Choose VPC and Subnets
     iii) Provide namespace (cruddur). This enables service connect
     iv) Create Cluster
2) Create Task Definition
     i) create task definition for backend-flask and frontend-react-js using json   
4) Create Service
    i) Select the created cluster
    ii) Click Create Service
    iii) Select Launch Type
    iv) Select Fargate
     v) Select Latest as platform version
     vi) Select Task as Application type
     vii) For Family select the corresponding task (backend-flask / Frontend-ract-js)
     viii) Click Turn on service connect
     ix) Select the created namespace
     x) Select use log collection
     xi) create service
        

### Deploy serverless containers using Fargate for the Backend and Frontend Application

1) Create Service using Json and bash script
        service json for backend
   
     ```
     {
      "cluster": "cruddur",
      "launchType": "FARGATE",
      "desiredCount": 1,
      "enableECSManagedTags": true,
      "enableExecuteCommand": true,
      "loadBalancers": [
        {
            "targetGroupArn": "arn:aws:elasticloadbalancing:ap-southeast-1:623053391718:targetgroup/backend-flask-TG/68dbd585f81c0bc9",
            "containerName": "backend-flask",
            "containerPort": 4567
        }
    ],
      "networkConfiguration": {
        "awsvpcConfiguration": {
          "assignPublicIp": "ENABLED",
          "securityGroups": [
            "sg-057f45caf743feeac"
          ],
          "subnets": [
            "subnet-077825ba320801964",
            "subnet-04d9b4cc597eb5f00",
            "subnet-063f0069eb52454e9"
          ]
        }
      },
      "serviceConnectConfiguration": {
        "enabled": true,
        "namespace": "cruddur",
        "services": [
          {
            "portName": "backend-flask",
            "discoveryName": "backend-flask",
            "clientAliases": [{"port": 4567}]
          }
        ]
      },
      "propagateTags": "SERVICE",
      "serviceName": "backend-flask",
      "taskDefinition": "backend-flask"
    }
    ```
         service json for frontend
        ```
        {
            "cluster": "cruddur",
            "launchType": "FARGATE",
            "desiredCount": 1,
            "enableECSManagedTags": true,
            "enableExecuteCommand": true,
            "loadBalancers": [
              {
                  "targetGroupArn": "arn:aws:elasticloadbalancing:ap-southeast-1:623053391718:targetgroup/frontend-react-js-TG/7db165c943235414",
                  "containerName": "frontend-react-js",
                  "containerPort": 3000
              }
          ],
            "networkConfiguration": {
              "awsvpcConfiguration": {
                "assignPublicIp": "ENABLED",
                "securityGroups": [
                  "sg-057f45caf743feeac"
                ],
                "subnets": [
                    "subnet-077825ba320801964",
                    "subnet-04d9b4cc597eb5f00",
                    "subnet-063f0069eb52454e9"
                ]
              }
            },
            "propagateTags": "SERVICE",
            "serviceName": "frontend-react-js",
            "taskDefinition": "frontend-react-js",
            "serviceConnectConfiguration": {
              "enabled": true,
              "namespace": "cruddur",
              "services": [
                {
                  "portName": "frontend-react-js",
                  "discoveryName": "frontend-react-js",
                  "clientAliases": [{"port": 3000}]
                }
              ]
            }
          }
        ```
Bash script to create backend service
      ```
      #! /usr/bin/bash
      
      aws ecs create-service --cli-input-json file://aws/json/service-backend-flask.json

      aws ecs create-service --cli-input-json file://aws/json/service-frontend-react-js.json

       ```

3) Register Task Definition

backend-flask task definition
```
{
    "family": "backend-flask",
    "executionRoleArn": "arn:aws:iam::AWS_ACCOUNT_ID:role/CruddurServiceExecutionRole",
    "taskRoleArn": "arn:aws:iam::AWS_ACCOUNT_ID:role/CruddurTaskRole",
    "networkMode": "awsvpc",
    "containerDefinitions": [
      {
        "name": "backend-flask",
        "image": "AWS_ACCOUNT_ID.dkr.ecr.AWS_DEFAULT_REGION.amazonaws.com/backend-flask:latest",
        "cpu": 256,
        "memory": 512,
        "essential": true,
        "portMappings": [
          {
            "name": "backend-flask",
            "containerPort": 4567,
            "protocol": "tcp", 
            "appProtocol": "http"
          }
        ],
        "logConfiguration": {
          "logDriver": "awslogs",
          "options": {
              "awslogs-group": "cruddur",
              "awslogs-region": "ap-southeast-1",
              "awslogs-stream-prefix": "backend-flask"
          }
        },
        "environment": [
          {"name": "OTEL_SERVICE_NAME", "value": "backend-flask"},
          {"name": "OTEL_EXPORTER_OTLP_ENDPOINT", "value": "https://api.honeycomb.io"},
          {"name": "AWS_COGNITO_USER_POOL_ID", "value": ""},
          {"name": "AWS_COGNITO_USER_POOL_CLIENT_ID", "value": ""},
          {"name": "FRONTEND_URL", "value": ""},
          {"name": "BACKEND_URL", "value": ""},
          {"name": "AWS_DEFAULT_REGION", "value": ""}
        ],
        "secrets": [
          {"name": "AWS_ACCESS_KEY_ID"    , "valueFrom": "arn:aws:ssm:AWS_DEFAULT_REGION:AWS_ACCOUNT_ID:parameter/cruddur/backend-flask/AWS_ACCESS_KEY_ID"},
          {"name": "AWS_SECRET_ACCESS_KEY", "valueFrom": "arn:aws:ssm:AWS_DEFAULT_REGION:AWS_ACCOUNT_ID:parameter/cruddur/backend-flask/AWS_SECRET_ACCESS_KEY"},
          {"name": "CONNECTION_URL"       , "valueFrom": "arn:aws:ssm:AWS_DEFAULT_REGION:AWS_ACCOUNT_ID:parameter/cruddur/backend-flask/CONNECTION_URL" },
          {"name": "ROLLBAR_ACCESS_TOKEN" , "valueFrom": "arn:aws:ssm:AWS_DEFAULT_REGION:AWS_ACCOUNT_ID:parameter/cruddur/backend-flask/ROLLBAR_ACCESS_TOKEN" },
          {"name": "OTEL_EXPORTER_OTLP_HEADERS" , "valueFrom": "arn:aws:ssm:AWS_DEFAULT_REGION:AWS_ACCOUNT_ID:parameter/cruddur/backend-flask/OTEL_EXPORTER_OTLP_HEADERS" }
          
        ]
      }
    ]
  }
```
frontend-react-js task definition 
```
{
    "family": "frontend-react-js",
    "executionRoleArn": "arn:aws:iam::AWS_ACCOUNT_ID:role/CruddurServiceExecutionRole",
    "taskRoleArn": "arn:aws:iam::AWS_ACCOUNT_ID:role/CruddurTaskRole",
    "networkMode": "awsvpc",
    "containerDefinitions": [
      {
        "name": "frontend-react-js",
        "image": "AWS_ACCOUNT_ID.dkr.ecr.ap-southeast-1.amazonaws.com/frontend-react:latest",
        "cpu": 256,
        "memory": 256,
        "essential": true,
        "portMappings": [
          {
            "name": "frontend-react-js",
            "containerPort": 3000,
            "protocol": "tcp", 
            "appProtocol": "http"
          }
        ],
  
        "logConfiguration": {
          "logDriver": "awslogs",
          "options": {
              "awslogs-group": "cruddur",
              "awslogs-region": "ap-southeast-1",
              "awslogs-stream-prefix": "frontend-react"
          }
        }
      }
    ]
  }
```

### Route traffic to the frontend and backend on different subdomains using Application Load Balancer

1) Go to EC2 in AWS console
2) On left panel select Load Balancers
3) Click Create Load Balancer
4) Choose Application Load Balancer (the traffic is limited to http and https and at request level)
5) Provide LB name, select internet-facing, IPv4 address type, select vpc and subnets, create a new SG, create Listeners (will take you to TG creation page) - follow below for TG creation
6) Select HTTP / 3000 and select Frontend TG
7) Select HTTP / 4567 and select Backend TG
8) Create Load balancer

Create Target Group from Load Balancer creation page
1) Select IP addresses (for ECS Fargate it will be IP addresses, if we were implementing in EC2 instances would have been the selection)
2) Select protocol (HTTP2 is good)
3) Provide health check details
4) In advanced heath check settings you can change the threshold for healthy and unhealthy, timeout, interval etc
6) In next page enter the IPv4 address (from ECS Fargate task IP address) for both the target group (TG) backend and frontend and complete creating TG (do this for both backend and frontend containers that would be running in ECS Fargate)

Confirm load balancer in ECS
1) Go back to ECS in console
2) Select the cluster
3) Switch to Task tab
4) Select the task
5) In the header section Load Balancer that is mapped, SG for LB etc should match with the LB and SG create in previous steps

### Securing our flask container



### Creating several bash utility scripts to easily work with serverless containers.

Create backend service
```
#! /usr/bin/bash

aws ecs create-service --cli-input-json file://aws/json/service-backend-flask.json
```
Create frontend service
```
#! /usr/bin/bash

aws ecs create-service --cli-input-json file://aws/json/service-frontend-react-js.json
```
Register / update backend task definition
```
#! /usr/bin/bash

ABS_PATH=$(readlink -f "$0")
FRONTEND_PATH=$(dirname $ABS_PATH)
BIN_PATH=$(dirname $FRONTEND_PATH)
PROJECT_PATH=$(dirname $BIN_PATH)
TASK_DEF_PATH="$PROJECT_PATH/aws/taskdefinitions/backend-flask.json"

echo $TASK_DEF_PATH

aws ecs register-task-definition \
--cli-input-json "file://$TASK_DEF_PATH"
```
```
#! /usr/bin/bash

CLUSTER_NAME="CrdClusterFargateCluster"
SERVICE_NAME="backend-flask"
TASK_DEFINTION_FAMILY="backend-flask"


LATEST_TASK_DEFINITION_ARN=$(aws ecs describe-task-definition \
--task-definition $TASK_DEFINTION_FAMILY \
--query 'taskDefinition.taskDefinitionArn' \
--output text)

echo "TASK DEF ARN:"
echo $LATEST_TASK_DEFINITION_ARN

aws ecs update-service \
--cluster $CLUSTER_NAME \
--service $SERVICE_NAME \
--task-definition $LATEST_TASK_DEFINITION_ARN \
--force-new-deployment
```
Register/ update frontend task definition
```
#! /usr/bin/bash

ABS_PATH=$(readlink -f "$0")
FRONTEND_PATH=$(dirname $ABS_PATH)
BIN_PATH=$(dirname $FRONTEND_PATH)
PROJECT_PATH=$(dirname $BIN_PATH)
TASK_DEF_PATH="$PROJECT_PATH/aws/taskdefinitions/frontend-react-js.json"

echo $TASK_DEF_PATH

aws ecs register-task-definition \
--cli-input-json "file://$TASK_DEF_PATH"
```
```
#! /usr/bin/bash

CLUSTER_NAME="cruddur"
SERVICE_NAME="frontend-react-js"
TASK_DEFINTION_FAMILY="frontend-react-js"


LATEST_TASK_DEFINITION_ARN=$(aws ecs describe-task-definition \
--task-definition $TASK_DEFINTION_FAMILY \
--query 'taskDefinition.taskDefinitionArn' \
--output text)

echo "TASK DEF ARN:"
echo $LATEST_TASK_DEFINITION_ARN

aws ecs update-service \
--cluster $CLUSTER_NAME \
--service $SERVICE_NAME \
--task-definition $LATEST_TASK_DEFINITION_ARN \
--force-new-deployment
```
