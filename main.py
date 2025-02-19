import asyncio
import os
from email_handler import EmailHandler
from parser import TestResultParser
from marvin_bot import DiscordBot
from dotenv import load_dotenv
import time

load_dotenv()

class MarvinMonitor:
    def __init__(self):
        self.email_handler = EmailHandler()
        self.discord_bot = DiscordBot()
        self.last_check_time = 0
        self.check_interval = 300

    async def process_new_results(self):
        try:
            # Connexion à la boîte mail
            if self.email_handler.connect_to_outlook():
                # Récupération du fichier de résultats
                trace_file = self.email_handler.fetch_latest_test_result()
                
                if trace_file and os.path.exists(trace_file):
                    # Parser le fichier
                    parser = TestResultParser(trace_file)
                    parser.parse()
                    
                    # Formater et envoyer le message Discord
                    discord_message = parser.format_for_discord()
                    await self.discord_bot.send_test_results(discord_message)
                    
                    # Nettoyer le fichier temporaire
                    os.remove(trace_file)
                
                # Déconnexion de la boîte mail
                if self.email_handler.mail:
                    self.email_handler.mail.logout()

        except Exception as e:
            print(f"Erreur lors du traitement : {str(e)}")

    async def run(self):
        @self.discord_bot.event
        async def on_ready():
            print(f"Bot connecté en tant que {self.discord_bot.user}")
            
            while True:
                current_time = time.time()
                
                # Vérifier si le temps d'intervalle s'est écoulé
                if current_time - self.last_check_time >= self.check_interval:
                    print("Vérification des nouveaux résultats...")
                    await self.process_new_results()
                    self.last_check_time = current_time
                
                # Attendre 1 minute avant la prochaine vérification
                await asyncio.sleep(60)

        # Démarrer le bot Discord
        await self.discord_bot.start(os.getenv("DISCORD_TOKEN"))

if __name__ == "__main__":
    monitor = MarvinMonitor()
    
    try:
        asyncio.run(monitor.run())
    except KeyboardInterrupt:
        print("\nArrêt du programme...")
    except Exception as e:
        print(f"Erreur fatale : {str(e)}")
