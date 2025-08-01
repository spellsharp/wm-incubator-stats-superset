import smtplib
from email.mime.text import MIMEText
from email.header import Header
import logging


logger = logging.getLogger(__name__)

def send_graduation_alert(
    project_type: str,
    language_code: str,
    active_users: int,
    edits: int,
    consecutive_months_met_criteria: int,
    recipient_email: str,
    sender_email: str,
    # --- Toolforge SMTP defaults  ---
    smtp_server: str = 'mail.tools.wmcloud.org', # Toolforge SMTP server
    smtp_port: int = 25                       # Toolforge SMTP port
) -> bool:
    """
    Sends an email alert using Toolforge SMTP.
    This function does NOT require SMTP authentication (username/password)
    when running on Toolforge and sending from a Toolforge address.

    Args:
        project_type (str): The type of the project.
        language_code (str): The language code of the project.
        active_users (int): The number of active users for the most recent month.
        edits (int): The number of edits for the most recent month.
        consecutive_months_met_criteria (int): Consecutive months criteria was met.
        recipient_email (str): The email address of the recipient (e.g., langcom@lists.wikimedia.org or your Toolforge email).
        sender_email (str): The sender's email address (e.g., incubator-dashboard.alerts@toolforge.org).
        smtp_server (str): The SMTP server address. Default for Toolforge.
        smtp_port (int): The SMTP server port. Default for Toolforge.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    subject = f"Wikimedia Incubator - Project potentially close to graduation: {project_type} ({language_code})"
    body = f"""
Dear LangCom,

This is an automated alert to inform you that the project for **{project_type} ({language_code})**
appears to have met the minimum criteria for potential graduation from the Incubator.

Based on recent metrics, the project has shown consistent activity:
- Active Users (last month): {active_users}
- Edits (last month): {edits}
- Consecutive Months Meeting Criteria (at least 4 active users with 15 edits): {consecutive_months_met_criteria}

Please review the project's status and consider it for graduation.

This alert was generated by the Incubator Dashboard monitoring system.

Best regards,
Incubator Dashboard Alerts
"""

    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = sender_email
    msg['To'] = recipient_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # --- IMPORTANT: No server.starttls() or server.login() needed for Toolforge outbound SMTP ---
            server.send_message(msg)
        logger.info(
            f"Successfully sent graduation alert for '{project_type} ({language_code})' "
            f"to {recipient_email} from {sender_email} using Toolforge SMTP."
        )
        return True
    except smtplib.SMTPException as e:
        logger.error(
            f"SMTP error sending alert for '{project_type} ({language_code})' with Toolforge SMTP: {e}"
        )
        return False
    except Exception as e:
        logger.error(
            f"An unexpected error occurred while sending alert for '{project_type} ({language_code})' with Toolforge SMTP: {e}"
        )
        return False