# Email Sender Microservice

A lightweight microservice for sending emails via SMTP. Containerized with Docker and configurable via environment variables.

## Quick Start

1. Set environment variables:
   ```bash
   export EMAIL_USER=your_email@example.com
   export EMAIL_PASSWORD=your_password
   export EMAIL_SMTP_SERVER=smtp.example.com
   export EMAIL_SMTP_PORT=587
   ```

2. Run with Docker Compose:
   ```bash
   docker compose up --build
   ```

3. Service available at `http://localhost:8001`

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
    "content": "Email Content"
}

Response: {
    "status": "success",
    "message": "Email sent successfully"
}
```

## Error Handling

- 400: Bad Request (invalid email format)
- 422: Unprocessable Entity (missing required fields)
- 500: Internal Server Error (SMTP issues) 