# Week 9 — CI/CD with CodePipeline, CodeBuild and CodeDeploy

### As initial step created following 2
1) `Buildspec.yml` file under backend-flask (we have only backend-flask in ECS fargate). ([code](https://github.com/Samba73/aws-bootcamp-cruddur-2023/blob/main/backend-flask/buildspec.yml))
2) `ecr-codebuild-role.json` ([code](https://github.com/Samba73/aws-bootcamp-cruddur-2023/blob/main/aws/policies/ecrcodebuild.json))
3) Create a new branch `prod`. Idea is to trigger code pipeline when there is pull request to this branch

### In AWS CodeBuild we need to create project which will be used in Code Piepline flow
Create a Build Project
1) Name the project & enable the build badge (get it in the GitHub for prod branch)
2) Choose source as GitHub, select repository, and source version to `prod`
3) select option rebuild every time a code change is pushed to this branch, select sigle build (important), select event type as `PULL_REQUEST_MERGED` (this indicates when the pull request is merged the trigger initiated)
4) for environment select managed image, select Amazon Linux 2 as OS, select standatd runtime, select latest image (4.0 , this varies according to region), select env type as Linux, select priveleged (important), select new service role, select option to use `buildspec.yml`, create cw logs as `cruddur`

### Code Pipeline
Create pipeline

1) Name it as `cruddur-backend-fargate`, allow to create a new service role automatically named as `AWSCodePipelineServiceRole-us-east-1-cruddur-backend-fargate`, select default location and default managed key in advanced settings
2) Select source stage from GitHub (Version 2), click "Connect to GitHub", set connection name as `cruddur`, install a new app, select the cruddur repo, in the end finish "Connect to GitHub" and back to the pipeline page
3) Select the bootcamp repo and select branch `prod`, select "start the pipeline on source code change" and default output artifact format
4) For build stage, select AWS CodeBuild as build provider, select your region, select the newly created project `cruddur-backend-flask-bake-image`
5) For deploy stage, select ECS as deploy provide, choose `cruddur` cluster, `backend-flask` service

### Test the pipeline
1) Make change in the code and push the change to remote repo
2) Create a new pull request from main to prod
3) Merge the new pull request
4) The pipeline should be triggered
