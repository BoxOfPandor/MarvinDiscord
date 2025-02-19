import imaplib
import email
from email.header import decode_header
import os
import sys
from dotenv import load_dotenv

load_dotenv()

class EmailHandler:
    def __init__(self):
        self.username = os.getenv("EMAIL")
        self.password = os.getenv("PASSWORD")
        self.mail = None

    def connect_to_outlook(self):
        """Se connecte à Outlook via IMAP."""
        try:
            imap_server = "imap.free.fr"
            self.mail = imaplib.IMAP4_SSL(imap_server)
            self.mail.login(self.username, self.password)
            return self.mail
        except imaplib.IMAP4.error as e:
            print(f"Erreur de connexion: Impossible de se connecter. Vérifiez vos identifiants.")
            return None
        except Exception as e:
            print(f"Erreur inattendue lors de la connexion: {str(e)}")
            return None

    def fetch_latest_test_result(self):
        """Récupère le dernier email contenant un fichier de résultat de test envoyé par Marvin."""
        if self.mail is None:
            return None
    
        try:
            self.mail.select("inbox")
            search_criteria = '(FROM "thibault.pouch@epitech.eu" SUBJECT "TR: [Marvin]")'
            status, messages = self.mail.search(None, search_criteria)
            email_ids = messages[0].split()
    
            if not email_ids:
                return None
    
            latest_email_id = email_ids[-1]
            status, msg_data = self.mail.fetch(latest_email_id, '(RFC822)')
    
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    # Parcourir les pièces jointes
                    for part in msg.walk():
                        if part.get_content_maintype() == 'multipart':
                            continue
                        if part.get('Content-Disposition') is None:
                            continue
    
                        filename = part.get_filename()
                        if filename and filename == "trace.txt":
                            filepath = os.path.join(os.getcwd(), "marvin_result.txt")
                            payload = part.get_payload(decode=True)
                            if payload:
                                with open(filepath, "wb") as f:
                                    f.write(payload)
                                return filepath
            return None
        except Exception as e:
            print(f"Erreur lors de la récupération du fichier: {str(e)}")
            return None
    
    def get_trace(self):

        handler = EmailHandler(self.username, self.password)
        handler.connect_to_outlook()
        file_path = handler.fetch_latest_test_result()
        if file_path:
            print(f"Fichier de test récupéré : {file_path}")
        else:
            print("Aucun fichier de test trouvé.")
        handler.mail.logout()
