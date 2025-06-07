import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re

class EmailSender:
    def __init__(self):
        # Get credentials from environment variables
        self.username = os.getenv('EMAIL_USER')
        self.password = os.getenv('EMAIL_PASSWORD')
        self.smtp_server = os.getenv('EMAIL_SMTP_SERVER')
        self.smtp_port = int(os.getenv('EMAIL_SMTP_PORT', '587'))

        # Validate required environment variables
        if not all([self.username, self.password, self.smtp_server]):
            raise ValueError("Missing required email configuration in environment variables")

    def _validate_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def send_email(self, recipient: str, subject: str, content: str) -> bool:
        """
        Send an email to the specified recipient
        
        Args:
            recipient (str): Email address of the recipient
            subject (str): Subject of the email
            content (str): Content of the email
            
        Returns:
            bool: True if email was sent successfully, False otherwise
            
        Raises:
            ValueError: If recipient email is invalid
        """
        if not self._validate_email(recipient):
            raise ValueError("Invalid recipient email address")

        # Create message
        message = MIMEMultipart()
        message['From'] = self.username
        message['To'] = recipient
        message['Subject'] = subject

        # Add content
        message.attach(MIMEText(content, 'plain'))

        # Send email
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(message)

        return True 