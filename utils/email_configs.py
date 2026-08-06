import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))       # .../falcontransportation/utils
ENV_PATH = os.path.join(BASE_DIR, "..", ".env")               # up one level, to project root
load_dotenv(ENV_PATH, override=True)

SMTPEMAIL = os.getenv("EMAIL")
SMTPPASSWORD = os.getenv("PASSWORD")
SERVER = os.getenv("SERVER")
PORT = int(os.getenv("PORT", 465))
async def send_contact_email(
    user_name: str,
    user_email: str,
    user_message: str,
    support_emails: list=["supplychain@greenfalcon.com.sa"],
    smtp_email: str=SMTPEMAIL,
    smtp_password: str=SMTPPASSWORD,
    smtp_server: str = SERVER,
    port: int = PORT,
):
    """
    Send a contact form email to support inbox.

    Args:
        user_name (str): Name of the user submitting the form.
        user_email (str): User's email address.
        user_message (str): Message typed by the user.
        support_email (str): Where the message should be delivered (your support inbox).
        smtp_email (str): The email account used for SMTP login (e.g., noreply@domain.com).
        smtp_password (str): Password or app password for the smtp_email account.
        smtp_server (str): SMTP server host (default: Gmail).
        port (int): SMTP port (default: 465 for SSL).
    """
    try:
        # Create the email
        msg = MIMEMultipart()
        msg["From"] = smtp_email
        msg["To"] = ", ".join(support_emails)
        msg["Subject"] = f"New Contact Form Message from {user_name}"
        msg["Reply-To"] = user_email  # so replies go to the user

        # Email body
        body = f"""
        You have received a new message from your website contact form:

        Name: {user_name}
        Email: {user_email}
        Message:
        {user_message}
        """
        msg.attach(MIMEText(body, "plain"))

        # Connect and send
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(smtp_email, smtp_password)
            server.sendmail(smtp_email, support_emails, msg.as_string())

        return {"success": True, "message": "Thank you! Your message has been received. We’ll get back to you soon."}

    except Exception as e:

        return {"success": False, "message": "An error occurred while sending your message. Please try again later."}
