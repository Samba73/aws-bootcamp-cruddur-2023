# Week 0 — Billing and Architecture

## Required Homework

### Week 0 - Live streamed video

  ***Attended the entire live streamed video***

### Week 0 - Chirag's Spend Considerations

  ***Activated Billing for IAM users***
      <sub>
        Logged as root user 
        Goto Account
        Scroll down to IAM User and Role Access to Billing Information and click Edit
        Check 'Activate IAM Access' and click Update button
        This enable IAM users wth admin access or IAM users that has Billing policy attached to view billing dashboard for this account
      </sub>

  ***Setting up billing alert***
      <sub>Login as Admin user
          Navigate to billing dashboard and click billing preference
          provide email for Free Tier alert (Im exhausted free tier)
          Enable Billing Receive alerts
          Save preferences and click Manage billing alerts link
          Cloudwatch dashboard is loaded (ensure N.Virgina is selected in the region dropdown)
          In cloudwatch dashboard create new alarm
          Select metric -> Billing -> Total Estimated charge -> Select the Estimatedcharges -> select metrics -> Select Static -> select choice -> click Next
          The billing alter require SNS topic to trigger the alarm. Create a new topic (or use existing if one available) provide topic name and email to create a new topic
          Click next and give alarm name
          Complete the steps and create alarm
          _10 alarms can be created in free tier_
          The alarm takes some time before it gets activated (initially will show as insufficient data</sub>
          
   ***Setup Cost allocation tags***
      <sub>Tags are free text entered and associated with AWS service(s) / resources
          Tags allows to uniquely identify each service / resource
          Click Cost Allocation tags and activate the tags that need allocation</sub>
    
   ***Create a budget alarm***
      <sub>Click budgets and go the Budget dashboard
          By default it will be Global region (it is global service (2 Budget alarm are free and anything more than that are chargeable)
          Select  use a template (AWS provided templates) or customized( Template -> Monthly cost budget widely used)
          Provide budget name, budget amount and provide email(s)
          Under Customized, Cost / Usage budget can be setup</sub>
    
   ***Difference between Billing alert and Budget Alarm***
     <sub>Billing alert is triggered for billed service charges whereas budget is forecasted estimate of cost alarms.
          Checked cost explorer and reports as part review of billing dashboard
          I do not have any credit to check, so skipped this. Any credit can be viewed  and redeeemed here
          Explore Free tier (12 month free, always free services)</sub>
  
  ### Week 0 - Ashish video on Security Considerations
  
   ***Creating IAM user with admin***
      <sub>Created 2 IAM user with Admin privelege</sub>
      <sub>Created a new group for admin and attached admin policy to the group. Added the 2 IAM user from previous step to admin group</sub>
      
   ***Create access key for IAM users (use with CLI, CDK etc)***
      <sub>Navigate to security credentials from AWS console main page</sub>
      <sub>Scroll down to create access keys and click create access key</sub>
      <sub>Only 2 Access key can be active at a time</sub>
      <sub>Before deleting an access key, it should be deactivated</sub>
      ####Note: Download the .csv file and make sure to save this which is required while configuring aws for CLI access####
   
   ***Create AWS Organizations and add OU(Organizational Units)***
      <sub>Created same structure as explained by Ashish</sub>
   ***AWS Cloud Trail***
      <sub>Went to cloud Train and explored the entries based on few services I used</sub>
   ***SCP - AWS Organization***
      
  ### Conceptual Diagaram in Lucid Charts### 
  
    <sub>did this along with everyone during the live session</sub>
  
https://lucid.app/lucidchart/966366bf-c705-4e3a-b9aa-c057c6f6e6fd/edit?page=0_0&invitationId=inv_9162ee28-d7ec-412e-8f02-38f7cddaad92#

  ### Recreate Logical Architectural Diagram in Lucid charts 
  
      <sub>Watched the video to rethink about the design and added some ideas. </sub>
      <sub>Thought scalibility, traffic distribution and load are key components as much as security</sub>
  ### Create Admin user
      <sub>Watched and created amdin user. Logging to console and cli using this admin user</sub>
  ### CloudShell
    Cloudshell is available only for selected region. Ensure the region selection to use cloudshell
    aws --cli-auto-prompt enables auto prompt and make it easy to type aws cli commands
    
  ***Install aws ali in gitpod
     _Execute the following in gitpod terminal_
           _curl -fSsl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"_
            _unzip -qq awscliv2.zip_
            _sudo ./aws/install --update_
            _rm awscliv2.zip  _***
            
  ### Generate AWS credentials
      <sub>Created AWS credentials for admin and used that to work cli in gitpod</sub>
  ### Create a Billing Alarm
  
      <sub>Followed the video and was able to create billing alarm using CLI</sub>
   ***By mistake the commits were made to Week-0 branch in my github. The aws/json folder were json file for CLI command refer is created under Week-0 folder.***
   
   ### Create a budget
   
      <sub>Followed the video and created budget</sub>
      
   ***Unfortunately, I couldnt save environment variable with AWS credenntials and everytime try the cli command in gotpod, had to configure. This I felt I was doing something wrong. Need to get this correct***
      
   
            
            
    
    
