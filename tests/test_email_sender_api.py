import pytest
from fastapi.testclient import TestClient
from api import app
from unittest.mock import patch
import os

client = TestClient(app)

class TestEmailSenderAPI:
    @pytest.fixture(autouse=True)
    def patch_env(self):
        with patch.dict(os.environ, {
            'EMAIL_USER': 'test@example.com',
            'EMAIL_PASSWORD': 'test_password',
            'EMAIL_SMTP_SERVER': 'smtp.example.com',
            'EMAIL_SMTP_PORT': '587'
        }):
            yield

    def test_health_check(self):
        """Test the health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    @patch('email_sender.EmailSender.send_email')
    def test_send_email_success(self, mock_send_email):
        """Test successful email sending through API"""
        mock_send_email.return_value = True
        
        response = client.post(
            "/send-email",
            json={
                "recipient": "test@example.com",
                "subject": "Test Subject",
                "content": "Test Content",
                "smtp_username": "sender@example.com",
                "smtp_password": "test_password",
                "smtp_server": "smtp.example.com",
                "smtp_port": 587
            }
        )
        
        assert response.status_code == 200
        assert response.json() == {"status": "success", "message": "Email sent successfully"}
        mock_send_email.assert_called_once_with(
            recipient="test@example.com",
            subject="Test Subject",
            content="Test Content",
            smtp_username="sender@example.com",
            smtp_password="test_password",
            smtp_server="smtp.example.com",
            smtp_port=587
        )

    @patch('email_sender.EmailSender.send_email')
    def test_send_email_invalid_input(self, mock_send_email):
        """Test email sending with invalid input"""
        response = client.post(
            "/send-email",
            json={
                "recipient": "invalid-email",
                "subject": "Test Subject",
                "content": "Test Content",
                "smtp_username": "sender@example.com",
                "smtp_password": "test_password",
                "smtp_server": "smtp.example.com",
                "smtp_port": 587
            }
        )
        
        assert response.status_code == 422  # FastAPI validation error
        mock_send_email.assert_not_called()

    def test_send_email_missing_fields(self):
        """Test email sending with missing required fields"""
        response = client.post(
            "/send-email",
            json={
                "recipient": "test@example.com",
                "subject": "Test Subject",
                "content": "Test Content"
                # missing SMTP credentials
            }
        )
        
        assert response.status_code == 422  # FastAPI validation error 