# import os
# import smtplib
# from email import encoders
# from email.mime.base import MIMEBase
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# import sys

# # You need to fill in your email details here.
# # For Gmail, you must use an "App Password" for security, NOT your regular password.
# SENDER_EMAIL = "srujanag521@gmail.com"  # <--- Your Gmail address
# SENDER_PASSWORD = "wunlmpnkpvqhlvou"  # <--- Your Gmail App Password
# SMTP_SERVER = "smtp.gmail.com"
# SMTP_PORT = 587

# def send_email_with_attachment(recipient_email, report_name, attachment_path):
#     """
#     Connects to the SMTP server and sends the email with the attached report.
#     """
#     try:
#         msg = MIMEMultipart()
#         msg['From'] = SENDER_EMAIL
#         msg['To'] = recipient_email
#         msg['Subject'] = f"Financial Report: {report_name}"

#         body = f"Hello,\n\nPlease find the requested financial report attached.\n\nReport Name: {report_name}\n\nBest regards,\nYour Reporting App"
#         msg.attach(MIMEText(body, 'plain'))

#         with open(attachment_path, "rb") as attachment:
#             part = MIMEBase("application", "octet-stream")
#             part.set_payload(attachment.read())

#         encoders.encode_base64(part)
#         part.add_header("Content-Disposition", f"attachment; filename= {os.path.basename(attachment_path)}")
#         msg.attach(part)

#         server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
#         server.starttls()
#         server.login(SENDER_EMAIL, SENDER_PASSWORD)
#         text = msg.as_string()
#         server.sendmail(SENDER_EMAIL, recipient_email, text)
#         server.quit()
#         print(f"Email sent successfully to {recipient_email}")
#         return True
#     except Exception as e:
#         print(f"Error sending email: {e}")
#         return False



import os
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName,
    FileType, Disposition, ContentId
)
import sys

# Use environment variables for API key and sender email
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')

def send_email_with_attachment(recipient_email, report_name, attachment_path):
    """
    Sends an email with an attached report using the SendGrid API.
    """
    if not SENDGRID_API_KEY:
        print("SendGrid API key not found. Cannot send email.")
        return False
    
    try:
        # Read the file content and encode it to base64
        with open(attachment_path, 'rb') as f:
            file_content_base64 = base64.b64encode(f.read()).decode()

        # Create the SendGrid Mail object
        message = Mail(
            from_email=SENDER_EMAIL,
            to_emails=recipient_email,
            subject=f"Financial Report: {report_name}",
            html_content=f"Hello,<br><br>Please find the requested financial report attached.<br><br>Report Name: {report_name}<br><br>Best regards,<br>Your Reporting App"
        )
        
        # Add the attachment
        attached_file = Attachment(
            FileContent(file_content_base64),
            FileName(os.path.basename(attachment_path)),
            FileType('application/octet-stream'),
            Disposition('attachment')
        )
        message.attachment = attached_file

        # Send the email via SendGrid API
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)

        print(f"Email sent successfully. Status Code: {response.status_code}")
        return response.status_code in [200, 202]
        
    except Exception as e:
        print(f"Error sending email with SendGrid: {e}")
        return False