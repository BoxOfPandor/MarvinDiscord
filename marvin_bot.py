import discord
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

class DiscordBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)

    async def on_ready(self):
        print(f'✅ Connecté en tant que {self.user}')

    async def send_test_results(self, message):
        channel = self.get_channel(CHANNEL_ID)
        if channel:
            await channel.send(message)
        else:
            print("❌ Erreur : Salon introuvable")

if __name__ == "__main__":
    bot = DiscordBot()

    test_message = "📝 **Résultats des tests automatiques**\n\n🔹 **Base functions**\n\t🔸 `strlen` - ✅ 100% Passed (3/3)\n\t🔸 `strchr` - ✅ 100% Passed (6/6)"

    @bot.event
    async def on_ready():
        await bot.send_test_results(test_message)
        await bot.close()

    bot.run(TOKEN)