import boto3


def send_html_email():
    ses_client = boto3.client('ses')
    CHARSET="UTF-8"
    html_email_content= """
        <html>
            <head></head>
            <h1 style='text_align:center'>AWS with Python & Boto3</h1>
            <p style='color:red'>Welcome to the course and thanks for buying the course</p>
        </html>
    
    """


    response = ses_client.send_email(
        Destination={
            "ToAddresses":[
                "youremail@com.com",
                "youremail2@com.com"
            ]
        },
        Message={
            "Body":{
                "Html":{
                    "Charset":CHARSET,
                    "Data":html_email_content
                }
            },
            "Subject":{
                "Charset":CHARSET,
                "Data":"AWS Course with Python"
            }
        },
        Source="youremail@com.com"
    )

    print(response)


send_html_email()