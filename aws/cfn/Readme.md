## Architecture deploy guice

Before running any templates to deploy, make sure to create S3 bucket to have all CFN artifacts

aws s3 mk s3://cfn-artifacts-cruddur.in
export CFN_BUCKET="cfn-artifacts-cruddur.in"
gp env CFN_BUCKET="cfn-artifacts-cruddur.in"
