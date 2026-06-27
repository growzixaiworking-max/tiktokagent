import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

load_dotenv()

class EmailNotifier:
    def __init__(self):
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("SENDER_PASSWORD") # This must be a Gmail App Password
        self.receiver_email = "alishbarehman526@gmail.com"

    def send_video_email(self, video_path, caption):
        if not self.sender_email or not self.sender_password:
            print("❌ Email credentials missing in .env. Skipping email.")
            return False

        print(f"📧 Sending video to {self.receiver_email}...")
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = self.receiver_email
        msg['Subject'] = f"🚀 New TikTok Video Ready: {os.path.basename(video_path)}"

        # Body text
        body = f"Aapki nayi TikTok video tayyar hai!\n\n--- CAPTION & HASHTAGS ---\n\n{caption}\n\nAgent is working for you! 🤖"
        msg.attach(MIMEText(body, 'plain'))

        # Attachment
        try:
            with open(video_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(video_path)}")
                msg.attach(part)

            # SMTP Server settings (Gmail example)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            text = msg.as_string()
            server.sendmail(self.sender_email, self.receiver_email, text)
            server.quit()
            print("✅ Email sent successfully!")
            return True
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            return False
