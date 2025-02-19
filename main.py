import asyncio
import os
from email_handler import EmailHandler
from parser import TestResultParser
from marvin_bot import DiscordBot
from dotenv import load_dotenv
import time
from tqdm import tqdm
import math

load_dotenv()

class MarvinMonitor:
    def __init__(self):
        self.email_handler = EmailHandler()
        self.discord_bot = DiscordBot()
        self.last_check_time = 0
        self.check_interval = 300  # 5 minutes
        self.last_processed_email_id = None

    async def process_new_results(self):
        try:
            if self.email_handler.connect_to_outlook():
                trace_file, email_id = self.email_handler.fetch_latest_test_result()
                
                if email_id and email_id != self.last_processed_email_id:
                    if trace_file and os.path.exists(trace_file):
                        parser = TestResultParser(trace_file)
                        parser.parse()
                        
                        discord_message = parser.format_for_discord()
                        await self.discord_bot.send_test_results(discord_message)
                        
                        os.remove(trace_file)
                        self.last_processed_email_id = email_id
                else:
                    print("Pas de nouvelle trace à traiter")
                
                if self.email_handler.mail:
                    self.email_handler.mail.logout()
    
        except Exception as e:
            print(f"Erreur lors du traitement : {str(e)}")

    async def wait_with_progress(self, seconds):
        """Affiche une barre de progression pendant l'attente"""
        with tqdm(total=seconds, desc="⏳ En attente", unit="s", bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} secondes') as pbar:
            for _ in range(seconds):
                await asyncio.sleep(1)
                pbar.update(1)

    async def run(self):
        @self.discord_bot.event
        async def on_ready():
            print(f"✅ Bot connecté en tant que {self.discord_bot.user}")
            
            while True:
                current_time = time.time()
                
                if current_time - self.last_check_time >= self.check_interval:
                    print("\n🔍 Vérification des nouveaux résultats...")
                    await self.process_new_results()
                    self.last_check_time = current_time
                    print("\n✨ Prochaine vérification dans 5 minutes")
                
                # Calculer le temps restant jusqu'à la prochaine vérification
                time_to_wait = math.ceil(self.check_interval - (time.time() - self.last_check_time))
                await self.wait_with_progress(time_to_wait)

        await self.discord_bot.start(os.getenv("DISCORD_TOKEN"))

if __name__ == "__main__":
    monitor = MarvinMonitor()
    
    try:
        print("🚀 Démarrage du bot Marvin...")
        asyncio.run(monitor.run())
    except KeyboardInterrupt:
        print("\n👋 Arrêt du programme...")
    except Exception as e:
        print(f"❌ Erreur fatale : {str(e)}")
