import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re

class EmailSender:
    def __init__(self):
        pass

    def _validate_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def send_email(self, recipient: str, subject: str, content: str, 
                  smtp_username: str, smtp_password: str, 
                  smtp_server: str, smtp_port: int = 587) -> bool:
        """
        Send an email to the specified recipient
        
        Args:
            recipient (str): Email address of the recipient
            subject (str): Subject of the email
            content (str): Content of the email
            smtp_username (str): SMTP username/email
            smtp_password (str): SMTP password
            smtp_server (str): SMTP server address
            smtp_port (int): SMTP server port (default: 587)
            
        Returns:
            bool: True if email was sent successfully, False otherwise
            
        Raises:
            ValueError: If recipient email is invalid or SMTP credentials are missing
        """
        if not self._validate_email(recipient):
            raise ValueError("Invalid recipient email address")
        
        if not all([smtp_username, smtp_password, smtp_server]):
            raise ValueError("Missing required SMTP credentials")

        # Create message
        message = MIMEMultipart()
        message['From'] = smtp_username
        message['To'] = recipient
        message['Subject'] = subject

        # Add content
        message.attach(MIMEText(content, 'plain'))

        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(message)

        return True 