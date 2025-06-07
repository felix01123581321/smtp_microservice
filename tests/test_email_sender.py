import pytest
from email_sender import EmailSender
import os
from unittest.mock import patch, MagicMock

class TestEmailSender:
    @pytest.fixture
    def email_sender(self):
        # Mock environment variables
        with patch.dict(os.environ, {
            'EMAIL_USER': 'test@example.com',
            'EMAIL_PASSWORD': 'test_password',
            'EMAIL_SMTP_SERVER': 'smtp.example.com',
            'EMAIL_SMTP_PORT': '587'
        }):
            return EmailSender()

    def test_initialization(self, email_sender):
        """Test if EmailSender initializes with correct credentials"""
        assert email_sender.smtp_server == 'smtp.example.com'
        assert email_sender.smtp_port == 587
        assert email_sender.username == 'test@example.com'
        assert email_sender.password == 'test_password'

    def test_send_email_success(self, email_sender):
        """Test successful email sending"""
        with patch('smtplib.SMTP') as mock_smtp:
            # Setup mock
            mock_smtp_instance = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_smtp_instance

            # Test sending email
            result = email_sender.send_email(
                recipient="recipient@example.com",
                subject="Test Subject",
                content="Test Content"
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
                content="Test Content"
            )

    def test_send_email_missing_credentials(self):
        """Test initialization with missing credentials"""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError):
                EmailSender() 