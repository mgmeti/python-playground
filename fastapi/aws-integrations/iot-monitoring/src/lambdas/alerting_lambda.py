import json
import boto3
import os

sns = boto3.client("sns")
ses = boto3.client("ses")

SNS_TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]
SES_FROM_EMAIL = os.environ["SES_FROM_EMAIL"]
SES_TO_EMAIL = os.environ["SES_TO_EMAIL"]  # must be verified in sandbox

def lambda_handler(event, context):
    print("Event:", json.dumps(event))

    for record in event["Records"]:
        if record["eventName"] == "INSERT":
            new_image = record["dynamodb"]["NewImage"]
            device_id = new_image["DeviceId"]["S"]
            alert_type = new_image["AlertType"]["S"]
            timestamp = new_image["Timestamp"]["S"]

            message = f"🚨 IoT Alert!\nDevice: {device_id}\nType: {alert_type}\nTime: {timestamp}"

            # 1) Publish to SNS
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=message,
                Subject="IoT Device Alert"
            )

            # 2) Send SES Email
            ses.send_email(
                Source=SES_FROM_EMAIL,
                Destination={"ToAddresses": [SES_TO_EMAIL]},
                Message={
                    "Subject": {"Data": f"IoT Alert: {alert_type}"},
                    "Body": {"Text": {"Data": message}}
                }
            )

    return {"status": "ok"}
