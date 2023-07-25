# Week 10 — CloudFormation Part 1

In this week and next week, the required infrastructure are created in AWS using cloudformation templates.
By executing the CFN templates, stacks are created which allow to organize the infrastructure into different categories and create for the application
Following categories are made
1) Networking - all basic networking components like VPC, Subnet, Route table etc
2) Cluster (ECS Fargate cluster) - The ECS Fargate cluster is created
3) Service (ECS Fargate Service) - The ECS Fargate service for the cluster (in step 2) is created along with SG, Service role and Task execution role
4) Postgres (RDS) - The RDS (Postgres) for user and activitiies data
5) DDB (Dynamodb) - The DDB, DDB stream, GSI, Lambda code for update are created
6) Frontend (for frontend code to be uploaded in S3 and linked to CF) - The react-js frontend is build and the build is pushed to S3 , linked to CF
7) CICD (for continous build, integration and deployment) - Create Code Build project and code pipeline that will be triggered automatically when there is merge of pull request in prod branch

we will be using `cfn-lint` to validate the template files that creates infrastructure. this need to be installed / added to gitpod.yml for future
we will be using cf-toml library created by Andrew in ruby for all the config data for infrastructures created using CFN templates
we will also explore usage of cfn-guard

2 s3 buckets `cfn-artifacts-cruddur.in` and `codedeploy-cruddur.in` to store the required artifacts

- Networking - ([code](https://github.com/Samba73/aws-bootcamp-cruddur-2023/tree/prod/aws/cfn/networking))
- Cluster - ([code](https://github.com/Samba73/aws-bootcamp-cruddur-2023/tree/prod/aws/cfn/cluster))
- Service - ([code](https://github.com/Samba73/aws-bootcamp-cruddur-2023/tree/prod/aws/cfn/service))
- Postgres (RDS) - ([code](https://github.com/Samba73/aws-bootcamp-cruddur-2023/tree/prod/aws/cfn/postgres))
- DynamoDB - ([code](https://github.com/Samba73/aws-bootcamp-cruddur-2023/tree/prod/aws/sam/ddb))
- Frontend - ([code](https://github.com/Samba73/aws-bootcamp-cruddur-2023/tree/prod/aws/cfn/frontend))
- CICD - ([code](https://github.com/Samba73/aws-bootcamp-cruddur-2023/tree/prod/aws/cfn/cicd))

The Dynamodb is created in SAM template and follows different approach. Build, package and deploy unlike CFN template which are executed directly
The CICD has nested stack which has parameters passed between them

Config file for these templates (CFN), ([code](https://github.com/Samba73/aws-bootcamp-cruddur-2023/blob/prod/aws/cfn/config.toml))
I'm using single config toml file for all CFN templates
Separate toml config file for SAM template (DDB)

Create all the infrastructure by executing the templates for each stack listed above ([code](https://github.com/Samba73/aws-bootcamp-cruddur-2023/tree/prod/bin/cfn)
The DDB is created following Build, Package and Deploy executions 

Edit Route53 Type A record for `api.cruddur.in` to point to ALB created

Check the following post CFN executions
1) Create Env sec in Parameter store
2) SG for ALB - Inbound for HTTP and HTTPS
3) SG for RDS (Postgres) - should allow inbound to ECS service SG and also initially GITPOD ip to allow seeding tables
4) SG for ECS that allows ALB SG as inbound
5) The ALB health checks
6) ECS health check (shoud be Healthy state)
7) Route 53 settings
8) CF Origin settings

### For frontend I did not follow Andrew ruby code but add script in package -json that build and use aws cli to upload (s3 sync command) to upload the build into s3 bucket `cruddur.in` . Bucket `www.cruddur.in` is redirected to `cruddur.in`

### Also the post confirmation lambda need to be updated to e inside the VPC created using networking CFN. Create a new SG that has inbound of RDS SG and map this new SG to lambda SG

### For the reply_activity column datatype in activities table, I updated the schema file directly to have correct datatype of UUID in the initial setup

From Gitpod connect to AWS instance of RDS and create tables

