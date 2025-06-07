from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from email_sender import EmailSender

app = FastAPI(
    title="Email Sender API",
    description="Microservice for sending emails",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmailRequest(BaseModel):
    recipient: EmailStr
    subject: str
    content: str

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/send-email")
async def send_email(request: EmailRequest):
    """
    Send an email to the specified recipient
    
    Args:
        request (EmailRequest): Email request containing recipient, subject, and content
        
    Returns:
        dict: Status of the email sending operation
    """
    try:
        email_sender = EmailSender()
        email_sender.send_email(
            recipient=request.recipient,
            subject=request.subject,
            content=request.content
        )
        return {
            "status": "success",
            "message": "Email sent successfully"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to send email") 