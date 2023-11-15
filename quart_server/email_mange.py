import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import private_config


def send_email(file_id: str, file_name: str, email: str):
    link = f"https://drive.google.com/file/d/{file_id}/view"

    html_content = f"""
    <a href="{link}" style="text-decoration: none;">
    <p> {file_name} </p>
    </a>
    """

    sender_email = private_config['sender_email']
    sender_password = private_config['email_password']

    subject = "מצורף הסרט שביקשת"

    # Create message object
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = subject

    message.attach(MIMEText(html_content, 'html', 'utf-8'))

    # Create SMTP session
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)

    # Send email
    server.sendmail(sender_email, email, message.as_string())

    # Terminate SMTP session
    server.quit()


if __name__ == '__main__':
    send_email('1vHruoyu5YVtq_bL0iJ3Vyqm7AH_f6rOh', 'חגיגה בסנוקר', 'marworm1@gmail.com')
