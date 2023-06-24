# Week 8 — Serverless Image Processing

### Create CDK stack & create s3 bucket to store assets

Firstly, manually create a S3 bucket named `assets.cruddur.in`, which will be used for serving the processed images in the profile page. In this bucket, create a folder named `banners`, and then upload a `banner.jpg` into the folder.

Secondly, export following env vars according to your domain name and another S3 bucket `uploaded-avatars`, which will be created by CDK later for saving the original uploaded avatar images:

```sh
export DOMAIN_NAME=cruddur.in
gp env DOMAIN_NAME=cruddur.in
export UPLOADS_BUCKET_NAME=uploaded-avatars
gp env UPLOADS_BUCKET_NAME=uploaded-avatars
```

In order to process uploaded images into a specific dimension, a Lambda function will be created by CDK. This function and related packages are specified in the scripts 
([repo](https://github.com/Samba73/aws-bootcamp-cruddur-2023/tree/8d3032479c118d7cd87b5df6428acc5e87243c99/aws/lambdas/process-image)) c


Now we can initialize CDK and install related packages:

```sh
cd /workspace/aws-bootcamp-cruddur-2023
mkdir thumbing-serverless-cdk
cd thumbing-serverless-cdk
touch .env.example
npm install aws-cdk -g
cdk init app --language typescript
npm install dotenv
```

In order to let the `sharp` dependency work in Lambda, run the script:

```sh
cd /workspace/aws-bootcamp-cruddur-2023
./bin/avatar/build

cd thumbing-serverless-cdk
```

To create AWS CloudFormation stack `ThumbingServerlessCdkStack`:

- run `cdk synth` you can debug and observe the generated `cdk.out`
- run `cdk bootstrap "aws://${AWS_ACCOUNT_ID}/${AWS_DEFAULT_REGION}"` (just once)
- finally run `cdk deploy`, you can observe your what have been created on AWS CloudFormation

Now, after running `./bin/avatar/upload`, at AWS I can observe that the `data.jpg` can be uploaded into the `uploaded-avatars` S3 bucket, which triggers `ThumbLambda` function to process the image, and then saves the processed image into the `avatars` folder in the `assets.cruddur.in` S3 bucket.


### serve assets behind Cloudfront

Amazon CloudFront is content distribution service in AWS. This delivers content from edge locations to reduce latency.
To create a CloudFront distribution, a certificate in the `us-east-1` zone for `*.cruddur.in` is required. If you don't have one yet, create one via AWS Certificate Manager, and click "Create records in Route 53" after the certificate is issued.

Create a distribution by:

- set the Origin domain to point to `assets.cruddur.in`
- choose Origin access control settings (recommended) and create a control setting
- select Redirect HTTP to HTTPS for the viewer protocol policy
- choose CachingOptimized, CORS-CustomOrigin as the optional Origin request policy, and SimpleCORS as the response headers policy
- set Alternate domain name (CNAME) as `assets.cruddur.in`
- choose the previously created ACM for the Custom SSL certificate.

Remember to copy the created policy to the `assets.cruddur.in` bucket by editing its bucket policy.

In order to visit `https://assets.cruddur.in/avatars/data.jpg` to see the processed image, we need to create a record via Route 53:

- set record name as `assets.cruddur.in`
- turn on alias, route traffic to alias to CloudFront distribution
- in my case, you can see my profile at https://assets.cruddur.in/avatars/data.jpg

Since we don't use versioned file names for a user's avatar, CloudFront edge caches old avatar. Until the old one expires, you will not immediately see the new avatar after updating the profile. Therefore, we need to [invalidate files](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Invalidation.html) by creating an invalidation:

- go to the distribution we created
- under the Invalidations tab, click create
- add object path `/avatars/*`

This ensures that CloudFront will always serve the latest avatar uploaded by the user.

### process images using a javascript lambda running sharpjs

### implement lambda layers
### use s3 event notifications to trigger processing images
### implement HTTP API Gateway using a lambda authorizer
### implement a ruby function to generate a presigned URL
### upload assets to a bucket client side using a resigned URL
