# !pip install sendgrid
import os
import shutil
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)
import base64

from logic_functions.general_utils import ensure_dir

def send_mail(body_data=None, subject=None, file_location=None, file_name=None, recipients = []):
    os.environ["SENDGRID_API_KEY"] = "INSERT YOUR SECRET KEY HERE"
    to_emails = recipients

    message = Mail(
            from_email='INSERT YOUR FROM EMAIL',
            to_emails=to_emails,
            subject=subject or file_name.split('.')[0],
            html_content=body_data
        )

    if file_location and file_name:
        with open(file_location, 'rb') as f:
            data = f.read()
            f.close()

        encoded_file = base64.b64encode(data).decode()

        attachedFile = Attachment(
            FileContent(encoded_file),
            FileName(file_name),
            FileType('application/pdf'),
            Disposition('attachment')
        )
        message.attachment = attachedFile

    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    return {
        "Status": response.status_code,
        "Body": response.body,
        "Headers": response.headers
    }
    

def build_email(recipients: list=None, email_subject: str=None, email_body: str=None):
    print("Building Email...")
    send_to_mails = recipients or [
        ('INSERT RECIPIENT EMAIL', 'INSERT RECIPIENT NAME'),
        ('INSERT RECIPIENT EMAIL', 'INSERT RECIPIENT NAME'),
        ('INSERT RECIPIENT EMAIL', 'INSERT RECIPIENT NAME'),
        ('INSERT RECIPIENT EMAIL', 'INSERT RECIPIENT NAME')
    ]
    _name = "reqs.txt"
    dir_name = 'emails_files'
    ensure_dir(dir_name)
    _location = f'{os.getcwd()}\\{dir_name}\\' + _name
    body_template = email_body or "<b><u>Example <i>HTML</i></u></b>"
    _subject = email_subject or "Example Subject"
    print("Build Completed, Sending Email Now...")
    email_result = send_mail(body_data=body_template, subject=_subject, file_location=None, file_name=None, recipients=send_to_mails)
    try:
        shutil.rmtree(dir_name)
    except FileNotFoundError:
        try:
            os.rmdir(dir_name)
        except:
            pass # The folder did not got created
    print("Email Sent.")
    return email_result["Status"]


def dummy_email():
    sbj = "SendGrid Email About the AutoScraper Process Request Creation"
    bdy = """
        <h2><u>Hello There,</u></h2>
        <p>
            This is a sample email sent to you by your <b>precious colleague!</b>
            <br>
            <i>&#128513; Please send him a Teams message in order to confirm that this email reached you all &#128526;</i>
        </p>
        <hr>
        <p>In your response please specify if that format of an email is suitable &#128406;</p>
        <hr>
        <sup>This Was Sent via The API</sup>
        <br>
        <sub>Or to his email, which is <INSERT EMAIL HERE></sub>
    """
    return build_email(recipients=None, email_subject=sbj, email_body=bdy)
