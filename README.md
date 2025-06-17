# Email Sender Microservice

A lightweight microservice for sending emails via SMTP. Containerized with Docker and supports multiple email accounts.

## Quick Start

1. Run with Docker Compose:
   ```bash
   docker compose up --build
   ```

2. Service available at `http://localhost:8001`

## API Endpoints

### Health Check
```http
GET /health
Response: {"status": "healthy"}
```

### Send Email
```http
POST /send-email
Content-Type: application/json

{
    "recipient": "recipient@example.com",
    "subject": "Email Subject",
    "content": "Email Content",
    "smtp_username": "sender@example.com",
    "smtp_password": "your_password",
    "smtp_server": "smtp.example.com",
    "smtp_port": 587
}

Response: {
    "status": "success",
    "message": "Email sent successfully"
}
```

## Error Handling

- 400: Bad Request (invalid email format or missing SMTP credentials)
- 422: Unprocessable Entity (missing required fields)
- 500: Internal Server Error (SMTP issues) 