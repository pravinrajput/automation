from botocore.vendored import requests
import json 
import logging
import os
import time

from urllib.error import URLError, HTTPError

HOOK_URL = os.environ['HookUrl']
SLACK_CHANNEL = os.environ['slackChannel']

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info("Event: " + str(event))
    message = json.loads(event['Records'][0]['Sns']['Message'])
    logger.info("Message: " + str(message))

    alarm_name = message['AlarmName']
    new_state = message['NewStateValue']
    reason = message['NewStateReason']
    ts = time.time()
    print(ts)
    
    if new_state == "ALARM": 
        thumb_url = "https://pravinrajput.files.wordpress.com/2019/06/alarm.png"
        color = "danger"
    elif new_state == "OK":
        thumb_url = "https://pravinrajput.files.wordpress.com/2019/06/ok.png"
        color = "good"
    else:
        thumb_url = ""
        color = ""    
        
    if 'nexus' in alarm_name:
        footer =  "nexus"
        footer_icon = "https://pravinrajput.files.wordpress.com/2019/06/nexus.png"

    elif 'Nexus' in alarm_name:
        footer =  "nexus"
        footer_icon = "https://pravinrajput.files.wordpress.com/2019/06/nexus.png"

    elif 'gitlab' in alarm_name: 
        footer =  "gitlab"
        footer_icon = "https://pravinrajput.files.wordpress.com/2019/06/gitlab.png"

    elif 'GitLab' in alarm_name: 
        footer =  "gitlab"
        footer_icon = "https://pravinrajput.files.wordpress.com/2019/06/gitlab.png"

    elif 'sonar' in alarm_name:
        footer =  "sonar"
        footer_icon = "https://pravinrajput.files.wordpress.com/2019/06/sonar.png"        

    elif 'Sonar' in alarm_name:
        footer =  "sonar"
        footer_icon = "https://pravinrajput.files.wordpress.com/2019/06/sonar.png"        

    elif 'Jenkins' in alarm_name:
        footer =  "jenkins"
        footer_icon = "https://pravinrajput.files.wordpress.com/2019/06/jenkins.png"

    elif 'jenkins' in alarm_name:
        footer =  "jenkins"
        footer_icon = "https://pravinrajput.files.wordpress.com/2019/06/jenkins.png"
    else:
        footer =  ""
        footer_icon = ""
    
    if 'disk' in alarm_name:
        mount_point = message['Trigger']['Dimensions'][0]['value']
        instance_id = message['Trigger']['Dimensions'][1]['value']
        slack_message = {
            "text": "",
             "attachments": [
                {
                    "fallback": "%s" % (alarm_name),
                    "pretext": "",
                    "title": "%s state is now %s" % (alarm_name, new_state),
                    "title_link": "",
                    "text": "%s" % (reason), 
                    "color": "%s" % (color),
                    "thumb_url": "%s" % (thumb_url),
                    "footer": "%s" % (footer),
                    "footer_icon": "%s" % (footer_icon),
                    "ts": "%d" % (ts),                    
                    "fields": [
                        {
                            "title": "Instance ID",
                            "value": "%s" % (instance_id), 
                            "short": "true"
                        },
                        {
                            "title": "Mount",
                            "value": "%s" % (mount_point),
                            "short": "true"
                        }
                    ],
                }
            ]
        } 


    else:
        instance_id = message['Trigger']['Dimensions'][0]['value']
        slack_message = {
            "text": "",
             "attachments": [
                {
                    "fallback": "%s" % (alarm_name),
                    "pretext": "",
                    "title": "%s state is now %s" % (alarm_name, new_state),
                    "title_link": "",
                    "text": "%s" % (reason), 
                    "color": "%s" % (color),
                    "thumb_url": "%s" % (thumb_url),
                    "footer": "%s" % (footer),
                    "footer_icon": "%s" % (footer_icon),
                    "ts": "%d" % (ts),
                    "fields": [
                        {
                            "title": "Instance ID",
                            "value": "%s" % (instance_id), 
                            "short": "true"
                        }
                    ],
                }
            ]
        } 

    response = requests.post(HOOK_URL,data=json.dumps(slack_message))
    
    http_reply = {
        "statusCode": 200,
        "body": response.text
    }

    try:
        logger.info("Message posted to %s", SLACK_CHANNEL)
        return http_reply
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)
