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

    if alarm_name == "nexus-healthcheck" and new_state == "ALARM":
        text = "Nexus - site is DOWN" 
        footer =  "nexus"
        footer_icon = "https://pravinrajput.files.wordpress.com/2019/06/nexus.png"

    elif alarm_name == "nexus-healthcheck" and new_state == "OK":
        text = "Nexus - site is UP" 
        footer =  "nexus"
        footer_icon = "https://pravinrajput.files.wordpress.com/2019/06/nexus.png"

    elif alarm_name == "gitlab-healthcheck" and new_state == "ALARM":
        text = "GitLab - site is DOWN" 
        footer =  "gitlab"
        footer_icon = "https://pravinrajput.files.wordpress.com/2019/06/gitlab.png"

    elif alarm_name == "gitlab-healthcheck" and new_state == "OK":
        text = "GitLab - site is UP" 
        footer =  "gitlab"
        footer_icon = "https://pravinrajput.files.wordpress.com/2019/06/gitlab.png"

    elif alarm_name == "sonar-healthcheck" and new_state == "ALARM":
        text = "Sonar - site is DOWN" 
        footer =  "sonar"
        footer_icon = "https://pravinrajput.files.wordpress.com/2019/06/sonar.png"        

    elif alarm_name == "sonar-healthcheck" and new_state == "OK":
        text = "Sonar - site is UP" 
        footer =  "sonar"
        footer_icon = "https://pravinrajput.files.wordpress.com/2019/06/sonar.png"        

    elif alarm_name == "jenkins-healthcheck" and new_state == "ALARM":
        text = "Jenkins - site is DOWN" 
        footer =  "jenkins"
        footer_icon = "https://pravinrajput.files.wordpress.com/2019/06/jenkins.png"

    elif alarm_name == "jenkins-healthcheck" and new_state == "OK":
        text = "Jenkins - site is UP" 
        footer =  "jenkins"
        footer_icon = "https://pravinrajput.files.wordpress.com/2019/06/jenkins.png"

    else:
        text = "" 
        footer =  ""
        footer_icon = ""

    slack_message = {
    "text": "",
    "attachments": [
        {
            "fallback": "%s" % (alarm_name),
            "pretext": "",
            "title": "%s state is now %s" % (alarm_name, new_state),
            "title_link": "",
            "text": "%s" % (text), 
            "color": "%s" % (color),
            "thumb_url": "%s" % (thumb_url),
            "footer": "%s" % (footer),
            "footer_icon": "%s" % (footer_icon),
            "ts": "%d" % (ts) 
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

