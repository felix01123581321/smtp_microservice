import pytest
from email_sender import EmailSender
import os
from unittest.mock import patch, MagicMock

class TestEmailSender:
    @pytest.fixture
    def email_sender(self):
        return EmailSender()

    def test_send_email_success(self, email_sender):
        """Test successful email sending with provided credentials"""
        with patch('smtplib.SMTP') as mock_smtp:
            # Setup mock
            mock_smtp_instance = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_smtp_instance

            # Test sending email
            result = email_sender.send_email(
                recipient="recipient@example.com",
                subject="Test Subject",
                content="Test Content",
                smtp_username="test@example.com",
                smtp_password="test_password",
                smtp_server="smtp.example.com",
                smtp_port=587
            )

            # Verify SMTP was called correctly
            mock_smtp.assert_called_once_with('smtp.example.com', 587)
            mock_smtp_instance.starttls.assert_called_once()
            mock_smtp_instance.login.assert_called_once_with('test@example.com', 'test_password')
            mock_smtp_instance.send_message.assert_called_once()
            assert result is True

    def test_send_email_invalid_recipient(self, email_sender):
        """Test email sending with invalid recipient"""
        with pytest.raises(ValueError):
            email_sender.send_email(
                recipient="invalid-email",
                subject="Test Subject",
                content="Test Content",
                smtp_username="test@example.com",
                smtp_password="test_password",
                smtp_server="smtp.example.com",
                smtp_port=587
            )

    def test_send_email_missing_credentials(self, email_sender):
        """Test email sending with missing credentials"""
        with pytest.raises(ValueError, match="Missing required SMTP credentials"):
            email_sender.send_email(
                recipient="test@example.com",
                subject="Test Subject",
                content="Test Content",
                smtp_username="test@example.com",
                smtp_password=None,  # Pass None to test missing credentials
                smtp_server="smtp.example.com",
                smtp_port=587
            ) 