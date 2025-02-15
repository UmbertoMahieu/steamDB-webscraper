import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
load_dotenv()


class MailManager:
    def __init__(self):
        self.MY_EMAIL = os.getenv("MY_EMAIL")
        self.MY_PWD = os.getenv("MY_PWD")

    def send_email(self, subject, content, email_to):
        # Créer un message multipart
        message = MIMEMultipart()
        message["From"] = self.MY_EMAIL
        message["To"] = email_to
        message["Subject"] = subject

        # Attacher le contenu sous forme de texte
        message.attach(MIMEText(content, "html"))

        # Connexion au serveur SMTP
        try:
            connexion = smtplib.SMTP("smtp.gmail.com", port=587)
            connexion.starttls()
            connexion.login(user=self.MY_EMAIL, password=self.MY_PWD)

            # Envoyer l'email
            connexion.sendmail(
                from_addr=self.MY_EMAIL,
                to_addrs=email_to,
                msg=message.as_string()
            )
            print("Email envoyé avec succès!")
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'email : {e}")
        finally:
            connexion.quit()  # Fermer la connexion

