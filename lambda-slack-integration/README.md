Slack Integration with AWS Lambda
----------------

Slack Notification using Cloudwatch and AWS Lambda

### AWS Services
* CloudWatch
* AWS Lambda
* SNS

![AWS-Arch](https://pravinrajput.files.wordpress.com/2019/06/slack-lambda.png)

**CloudWatch** will trigger an alarm to send a message to an **SNS** topic if the monitoring data gets out of range. A **Lambda** function will be invoked in response of **SNS** receiving the message and will call the **Slack API** to post a message to **Slack channel**.

## Create Slack Webhook 
Follow these steps to configure the webhook in Slack:
  1. Navigate to https://**your-team-domain**.slack.com/services/new
  2. Search for and select "Incoming WebHooks".
  3. Choose the default channel where messages will be sent and click "Add Incoming WebHooks Integration".
  4. Copy the webhook URL from the setup instructions and use it in the next section

Webhook URL will be like: https://hooks.slack.com/services/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R 
This is not actual URL :P

## Create SNS Topic
Follow link to create SNS Topic and SNS Subscriber https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/US_SetupSNS.html

## Create Lambda Function
To get started, create lambda function refer https://docs.aws.amazon.com/lambda/latest/dg/getting-started-create-function.html

![lambda1](https://pravinrajput.files.wordpress.com/2019/06/lambda1.png)

1. Go to AWS Console and navigate to Lambda service then click on **"Create function"**
2. Choose option **"Author from scratch"**
3. Enter your function name into Function Name box
4. Choose Runtime **Python 3.6** (you may choose Python 3.7, but following python code is tested with python3.6)
5. In Permissions section, leave the setting as it is. i.e. **Execution role** will be **"Create a new role with basic Lambda permissions"**
6. Click on "Create function"

![lambda2](https://pravinrajput.files.wordpress.com/2019/06/lambda2.png)

7. Next, Add trigger, choose SNS from list
8. Now configure SNS, choose SNS Topic which we created in last step i.e. **slackSNS** and select **"Enable Trigger"**
9. Hit Add button 

![lambda3](https://pravinrajput.files.wordpress.com/2019/06/lambda3.png)

10. Click on myfunction and copy & paste content of lambda_slack_notify_utilization.py into lambda-editor
11. Provide Environment variables, **HookUrl & slackChannel**

## Create Cloudwatch Alarm for EC2 CPU Utilization
Refer link to create https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/US_AlarmAtThresholdEC2.html

![lambda4](https://pravinrajput.files.wordpress.com/2019/06/lambda4.png)

In above link, in step 5.d under Actions, ensure that you are selecting SNS topic which we created in previous steps. We also need to configure alarm when state is ok, just click on +notification and follow second step i.e. recovery. So we can get slack notification for both when alert get trigger and it's recovery.  Refer above image.

Alert:
1. Under Actions, for Whenever this alarm, choose State is ALARM. For Send notification to, select an existing SNS topic i.e. slackSNS

Recovery:
2. Under Actions, for Whenever this alarm, choose State is OK. For Send notification to, select an existing SNS topic i.e. slackSNS


Slack Outputs
------------------
Just like CPU Utilization, we can send slack notification of Memory, Disk & Site Healthcheck using route53(Up/Down). 

#### CPU-Utilization

![CPU](https://pravinrajput.files.wordpress.com/2019/06/cpu-slack-notification.png)

#### Memory-Utilization

![Memory](https://pravinrajput.files.wordpress.com/2019/06/memory-slack-notification.png)

#### Disk-Utilization

![Disk](https://pravinrajput.files.wordpress.com/2019/06/disk-slack-notification.png)

#### Healthcheck

![Healthcheck](https://pravinrajput.files.wordpress.com/2019/06/healthcheck-slack-notification.png)

Other Links
------------------
* Slack Message Attachment: https://api.slack.com/docs/message-attachments

Note
------------------ 
I know, there are lots of AWS docs links as steps are straight forward. Just follow them step by step, I believe you can configure it. 

Author Information
------------------

This doc was created in 2019 by Pravinsingh Rajput

