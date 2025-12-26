import smtplib
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

logger = logging.getLogger(__name__)
from dotenv import load_dotenv
import os
load_dotenv()



def send_credentials_email(to_email: str, user_name: str, plain_password: str):

    sender_email = os.getenv("SMTP_EMAIL")
    sender_password = os.getenv("SMTP_PASSWORD")
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    subject = "Your Investigator App Credentials"
    body = f"""
Hello,

Your account has been created successfully.

Username: {user_name}
Password: {plain_password}

Please change your password after logging in for the first time.

Regards,
Team Britsure
    """

    try:
        logger.info(f"Preparing to send email to: {to_email}")

        # Create message
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Create SMTP session with timeout
        logger.info("Connecting to SMTP server...")
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=30)  # 30 second timeout
        server.starttls()

        logger.info("Logging into SMTP server...")
        server.login(sender_email, sender_password)

        logger.info("Sending email...")
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()

        logger.info("Email sent successfully")

    except socket.timeout:
        logger.error("SMTP connection timed out")
        raise Exception("Email service timeout")
    except smtplib.SMTPAuthenticationError:
        logger.error("SMTP authentication failed")
        raise Exception("Email authentication failed")
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error: {e}")
        raise Exception(f"Email sending failed: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected email error: {e}")
        raise Exception(f"Email sending failed: {str(e)}")
