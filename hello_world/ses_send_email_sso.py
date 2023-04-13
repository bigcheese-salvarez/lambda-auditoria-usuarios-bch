import os.path
import boto3
import email
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
s3 = boto3.client("s3")
def lambda_handler(event, context):
    RECIPIENTS = ["salvarez@bigcheese.com.uy"]
    for RECIPIENT in RECIPIENTS:
        SENDER = "salvarez@bigcheese.com.uy"
        AWS_REGION = "us-east-1"
        SUBJECT = "Email desde S3"
        FILEOBJ = event["Records"][0]
        BUCKET_NAME = str(FILEOBJ['s3']['bucket']['name'])
        KEY = str(FILEOBJ['s3']['object']['key'])
        FILE_NAME = os.path.basename(KEY)
        TMP_FILE_NAME = '/tmp/' + FILE_NAME
        s3.download_file(BUCKET_NAME, KEY, TMP_FILE_NAME)
        ATTACHMENT = TMP_FILE_NAME
        BODY_TEXT = "El siguiente archivo fue subido a S3"
        client = boto3.client('ses',region_name=AWS_REGION)
        msg = MIMEMultipart()
        # Add subject, from and to lines.
        msg['Subject'] = SUBJECT 
        msg['From'] = SENDER 
        msg['To'] = RECIPIENT
        textpart = MIMEText(BODY_TEXT)
        msg.attach(textpart)
        att = MIMEApplication(open(ATTACHMENT, 'rb').read())
        att.add_header('Content-Disposition','attachment',filename=FILE_NAME)
        msg.attach(att)
        print(msg)
        try:
            response = client.send_raw_email(
                Source=SENDER,
                Destinations=[RECIPIENT],
                RawMessage={ 'Data':msg.as_string() }
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:",response['MessageId'])
