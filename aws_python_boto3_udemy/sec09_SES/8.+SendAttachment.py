import boto3

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email_attachment():
    msg = MIMEMultipart()

    msg["Subject"]="This is python with boto3 course"
    msg["From"]="youremail@com.com"
    msg["To"]="youremail2@com.com"

    body = MIMEText("Aws with Python & Boto3, Thanks for buying the course")
    msg.attach(body)


    filename = "file.pdf"

    with open(filename, "rb") as f:
        part = MIMEApplication(f.read())
        part.add_header("Content-Disposition",
                        "attachment",
                        filename=filename)

    msg.attach(part)


    ses_client = boto3.client('ses')
    response = ses_client.send_raw_email(
        Source="youremail@com.com",
        Destinations=["youremail@com.com","youremail2@com.com"],
        RawMessage={"Data":msg.as_string()}

    )

    print(response)



send_email_attachment()
