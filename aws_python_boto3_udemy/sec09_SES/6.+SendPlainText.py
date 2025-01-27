import boto3


def send_email_text():
    ses_client = boto3.client('ses')
    CHARSET='UTF-8'

    response = ses_client.send_email(
        Destination={
            "ToAddresses":[
                "youremail@com.com",
                "youremail2@com.com"
            ]
        },
        Message={
            "Body":{
                "Text":{
                    "Charset":CHARSET,
                    "Data":"Thanks for buying the course"
                }
            },
            "Subject":{
                "Charset":CHARSET,
                "Data":"AWS Course with Python & Boto3"
            }
        },
        Source = "youremail@com.com"
    )

    print(response)


send_email_text()