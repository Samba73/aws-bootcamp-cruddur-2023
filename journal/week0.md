# Week 0 — Billing and Architecture

I use AWS account that is already out of free tier but explored the billing dashboard going through video from Chirag. It was a good start to the bootcamp.

As pre-requisite to billing (before setting cloudwatch alarm and creating budget), an IAM user was created (root user access to console and services is not advisable). So it is recommendation to create IAM user(s) with admin privelege and provide billing access to the admin IAM user

I created 2 users and grouped these users under group admin. The users individually have admin policy attached. (It is possible to create group with admin policy attached and users under the group will also have same policy applied).

 ### Activate Billing for IAM users
  Logged as root user 
  Goto Account
  Scroll down to IAM User and Role Access to Billing Information and click Edit
  Check 'Activate IAM Access' and click Update button
  This enable IAM users wth admin access or IAM users that has Billing policy attached to view billing dashboard for this account
  
Note: It is recommended to access AWS console as Admin IAM user and avoid ROOT user access

### Setting up billing alert

   Login as Admin user
   Navigate to billing dashboard and click billing preference
   provide email for Free Tier alert (Im exhausted free tier)
   Enable Billing Receive alerts
   Save preferences and click Manage billing alerts link
   Cloudwatch dashboard is loaded (ensure N.Virgina is selected in the region dropdown)
   In cloudwatch dashboard create new alarm
   Select metric -> Billing -> Total Estimated charge -> Select the Estimatedcharges -> select metrics -> Select Static -> select choice -> click Next
   The billing alter require SNS topic to trigger the alarm. Create a new topic (or use existing if one available) provide topic name and email to create a new topic
   Click next and give alarm name
   complete the steps and create alarm
   10 alarms can be created in free tier
   The alarm takes some time before it gets activated (initially will show as insufficient data)
   
 ### Setup Cost allocation tags
    Tags are free text entered and associated with AWS service(s) / resources
    Tags allows to uniquely identify each service / resource
    Click Cost Allocation tags and activate the tags that need allocation
    
 ### Create a budget alarm
    Click budgets and go the Budget dashboard
    By default it will be Global region (it is global service (2 Budget alarm are free and anything more than that are chargeable)
    Select  use a template (AWS provided templates) or customized( Template -> Monthly cost budget widely used)
    Provide budget name, budget amount and provide email(s)
    Under Customized, Cost / Usage budget can be setup
    
  ## Difference between Billing alert and Budget Alarm
     Billing alert is triggered for billed service charges whereas budget is forecasted estimate of cost alarms.
  Checked cost explorer and reports as part review of billing dashboard
  I do not have any credit to check, so skipped this. Any credit can be viewed  and redeeemed here
  Explore Free tier (12 month free, always free services)
  
  
    
    
    
