# import smtplib
# import os
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from datetime import datetime
# import logging

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class EmailService:
#     def __init__(self):
#         # Email configuration - use environment variables for security
#         self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
#         self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
#         self.sender_email = os.getenv('SENDER_EMAIL', 'your-email@gmail.com')
#         self.sender_password = os.getenv('SENDER_PASSWORD', 'your-app-password')
#         self.recipient_emails = os.getenv('RECIPIENT_EMAILS', 'admin@company.com').split(',')
        
#     def send_deadline_alert(self, deadline_message, deadline_type='general', urgency='medium'):
#         """
#         Send email alert for deadlines
#         """
#         try:
#             # Create message
#             msg = MIMEMultipart()
#             msg['From'] = self.sender_email
#             msg['To'] = ', '.join(self.recipient_emails)
            
#             # Set subject based on urgency and type
#             urgency_prefix = {
#                 'high': '🚨 URGENT: ',
#                 'medium': '⚠️ REMINDER: ',
#                 'low': 'ℹ️ NOTICE: '
#             }
            
#             msg['Subject'] = f"{urgency_prefix.get(urgency, '')}Deadline Alert - {deadline_type.upper()}"
            
#             # Create HTML email body
#             html_body = self._create_deadline_email_template(deadline_message, deadline_type, urgency)
#             msg.attach(MIMEText(html_body, 'html'))
            
#             # Send email
#             server = smtplib.SMTP(self.smtp_server, self.smtp_port)
#             server.starttls()
#             server.login(self.sender_email, self.sender_password)
            
#             text = msg.as_string()
#             server.sendmail(self.sender_email, self.recipient_emails, text)
#             server.quit()
            
#             logger.info(f"Deadline email sent successfully to {self.recipient_emails}")
#             return True
            
#         except Exception as e:
#             logger.error(f"Failed to send deadline email: {str(e)}")
#             return False
    
#     def _create_deadline_email_template(self, message, deadline_type, urgency):
#         """
#         Create HTML email template for deadline alerts
#         """
#         urgency_colors = {
#             'high': '#facc15',    # Yellow
#             'medium': '#facc15',  # Orange
#             'low': '#facc15'      # Blue
#         }

        
#         urgency_icons = {
#             'high': '🚨',
#             'medium': '⚠️',
#             'low': 'ℹ️'
#         }
        
#         color = urgency_colors.get(urgency, '#2563eb')
#         icon = urgency_icons.get(urgency, 'ℹ️')
        
#         html_template = f"""
#         <!DOCTYPE html>
#         <html>
#         <head>
#             <meta charset="UTF-8">
#             <meta name="viewport" content="width=device-width, initial-scale=1.0">
#             <title>Deadline Alert</title>
#         </head>
#         <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
#             <div style="background: linear-gradient(135deg, {color} 0%, {color}dd 100%); padding: 30px; border-radius: 10px; margin-bottom: 20px;">
#                 <h1 style="color: white; margin: 0; text-align: center; font-size: 24px;">
#                     {icon} Deadline Alert
#                 </h1>
#                 <p style="color: white; margin: 10px 0 0 0; text-align: center; opacity: 0.9;">
#                     {deadline_type.upper()} - {urgency.upper()} Priority
#                 </p>
#             </div>
            
#             <div style="background: #f8f9fa; padding: 25px; border-radius: 8px; border-left: 4px solid {color};">
#                 <h2 style="color: {color}; margin-top: 0; font-size: 18px;">Deadline Details:</h2>
#                 <p style="font-size: 16px; margin: 15px 0; background: white; padding: 15px; border-radius: 5px; border: 1px solid #e0e0e0;">
#                     {message}
#                 </p>
                
#                 <div style="margin: 20px 0; padding: 15px; background: white; border-radius: 5px; border: 1px solid #e0e0e0;">
#                     <p style="margin: 0; color: #666; font-size: 14px;">
#                         <strong>Alert Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#                     </p>
#                 </div>
                
#                 <div style="margin-top: 25px; padding: 15px; background: #fff3cd; border-radius: 5px; border: 1px solid #ffeaa7;">
#                     <p style="margin: 0; color: #856404; font-size: 14px;">
#                         <strong>⏰ Action Required:</strong> Please review and take necessary action before the deadline.
#                     </p>
#                 </div>
#             </div>
            
#             <div style="margin-top: 20px; padding: 15px; text-align: center; color: #666; font-size: 12px; border-top: 1px solid #eee;">
#                 <p>This is an automated alert from your Notifications & Alerts System</p>
#                 <p>Dashboard: <a href="http://127.0.0.1:5502/frontend/index.html" style="color: {color};">View Dashboard</a></p>
#             </div>
#         </body>
#         </html>
#         """
        
#         return html_template
    
#     def send_test_email(self):
#         """
#         Send a test email to verify configuration
#         """
#         test_message = "This is a test deadline alert to verify email configuration."
#         return self.send_deadline_alert(test_message, 'TEST', 'low')

# # Utility function to determine urgency based on deadline content
# def determine_urgency(deadline_message):
#     """
#     Analyze deadline message to determine urgency level
#     """
#     message_lower = deadline_message.lower()
    
#     # High urgency keywords
#     high_urgency_keywords = ['urgent', 'today', '1 day', 'tomorrow', 'overdue', 'expired']
#     # Medium urgency keywords  
#     medium_urgency_keywords = ['5 days', '3 days', '1 week', 'soon', 'reminder']
    
#     if any(keyword in message_lower for keyword in high_urgency_keywords):
#         return 'high'
#     elif any(keyword in message_lower for keyword in medium_urgency_keywords):
#         return 'medium'
#     else:
#         return 'low'

# def extract_deadline_type(deadline_message):
#     """
#     Extract deadline type from message for better categorization
#     """
#     message_lower = deadline_message.lower()
    
#     if 'vat' in message_lower:
#         return 'VAT Filing'
#     elif 'invoice' in message_lower:
#         return 'Invoice'
#     elif 'report' in message_lower:
#         return 'Report'
#     elif 'tax' in message_lower:
#         return 'Tax'
#     elif 'deadline' in message_lower:
#         return 'General Deadline'
#     else:
#         return 'Business Task'








import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To, From, Subject, HtmlContent
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        # Email configuration - use environment variables for security
        self.sendgrid_api_key = os.getenv('SENDGRID_API_KEY')
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.recipient_emails = os.getenv('RECIPIENT_EMAILS', 'admin@company.com').split(',')

    def send_deadline_alert(self, deadline_message, deadline_type='general', urgency='medium'):
        """
        Send email alert for deadlines using SendGrid API.
        """
        if not self.sendgrid_api_key:
            logger.error("SendGrid API key not configured.")
            return False

        try:
            subject_prefix = {
                'high': '🚨 URGENT: ',
                'medium': '⚠️ REMINDER: ',
                'low': 'ℹ️ NOTICE: '
            }
            subject = f"{subject_prefix.get(urgency, '')}Deadline Alert - {deadline_type.upper()}"
            
            html_body = self._create_deadline_email_template(deadline_message, deadline_type, urgency)

            message = Mail(
                from_email=From(self.sender_email, 'Reporting & Alerts'),
                to_emails=To(self.recipient_emails),
                subject=Subject(subject),
                html_content=HtmlContent(html_body)
            )

            # Send email via SendGrid
            sg = SendGridAPIClient(self.sendgrid_api_key)
            response = sg.send(message)
            
            logger.info(f"Deadline email sent successfully to {self.recipient_emails}. Status Code: {response.status_code}")
            return response.status_code in [200, 202]

        except Exception as e:
            logger.error(f"Failed to send deadline email: {str(e)}")
            return False
    
    def _create_deadline_email_template(self, message, deadline_type, urgency):
        """
        Create HTML email template for deadline alerts
        """
        urgency_colors = {
            'high': '#facc15',    # Yellow
            'medium': '#facc15',  # Orange
            'low': '#facc15'      # Blue
        }

        urgency_icons = {
            'high': '🚨',
            'medium': '⚠️',
            'low': 'ℹ️'
        }
        
        color = urgency_colors.get(urgency, '#2563eb')
        icon = urgency_icons.get(urgency, 'ℹ️')
        
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Deadline Alert</title>
        </head>
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, {color} 0%, {color}dd 100%); padding: 30px; border-radius: 10px; margin-bottom: 20px;">
                <h1 style="color: white; margin: 0; text-align: center; font-size: 24px;">
                    {icon} Deadline Alert
                </h1>
                <p style="color: white; margin: 10px 0 0 0; text-align: center; opacity: 0.9;">
                    {deadline_type.upper()} - {urgency.upper()} Priority
                </p>
            </div>
            
            <div style="background: #f8f9fa; padding: 25px; border-radius: 8px; border-left: 4px solid {color};">
                <h2 style="color: {color}; margin-top: 0; font-size: 18px;">Deadline Details:</h2>
                <p style="font-size: 16px; margin: 15px 0; background: white; padding: 15px; border-radius: 5px; border: 1px solid #e0e0e0;">
                    {message}
                </p>
                
                <div style="margin: 20px 0; padding: 15px; background: white; border-radius: 5px; border: 1px solid #e0e0e0;">
                    <p style="margin: 0; color: #666; font-size: 14px;">
                        <strong>Alert Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    </p>
                </div>
                
                <div style="margin-top: 25px; padding: 15px; background: #fff3cd; border-radius: 5px; border: 1px solid #ffeaa7;">
                    <p style="margin: 0; color: #856404; font-size: 14px;">
                        <strong>⏰ Action Required:</strong> Please review and take necessary action before the deadline.
                    </p>
                </div>
            </div>
            
            <div style="margin-top: 20px; padding: 15px; text-align: center; color: #666; font-size: 12px; border-top: 1px solid #eee;">
                <p>This is an automated alert from your Notifications & Alerts System</p>
                <p>Dashboard: <a href="http://127.0.0.1:5502/frontend/index.html" style="color: {color};">View Dashboard</a></p>
            </div>
        </body>
        </html>
        """
        
        return html_template
    
    def send_test_email(self):
        """
        Send a test email to verify configuration
        """
        test_message = "This is a test deadline alert to verify email configuration."
        return self.send_deadline_alert(test_message, 'TEST', 'low')

# Utility function to determine urgency based on deadline content
def determine_urgency(deadline_message):
    """
    Analyze deadline message to determine urgency level
    """
    message_lower = deadline_message.lower()
    
    # High urgency keywords
    high_urgency_keywords = ['urgent', 'today', '1 day', 'tomorrow', 'overdue', 'expired']
    # Medium urgency keywords  
    medium_urgency_keywords = ['5 days', '3 days', '1 week', 'soon', 'reminder']
    
    if any(keyword in message_lower for keyword in high_urgency_keywords):
        return 'high'
    elif any(keyword in message_lower for keyword in medium_urgency_keywords):
        return 'medium'
    else:
        return 'low'

def extract_deadline_type(deadline_message):
    """
    Extract deadline type from message for better categorization
    """
    message_lower = deadline_message.lower()
    
    if 'vat' in message_lower:
        return 'VAT Filing'
    elif 'invoice' in message_lower:
        return 'Invoice'
    elif 'report' in message_lower:
        return 'Report'
    elif 'tax' in message_lower:
        return 'Tax'
    elif 'deadline' in message_lower:
        return 'General Deadline'
    else:
        return 'Business Task'