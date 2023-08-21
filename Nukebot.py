# Nukes Berlin Discord Bot by Florian Kondrot (and ChatGPT)
import discord
import random
from discord.ext import commands

# Connect to the Discord client
intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False
bot = commands.Bot(command_prefix='!', intents=intents)

# Databases
diceroll = [1, 2, 3, 4, 5, 6]
DukeNukem = ['Hail to the king, baby!', 'Yeah, piece of cake!', 'Groovy!', 'Let’s rock!', 'Come get some!', 'Damn I’m good.']
Saison23_24 = ['01.10.23', '22.10.23', '19.11.23', '21.01.24', '18.02.24', '24.03.24', '21.04.24', '02.06.24']

#Log in message in terminal
@bot.event
async def on_ready():
    print(f'Successfully logged in as {bot.user.name}')

#Abfrage Spieltage
@bot.command()
async def Spieltag(ctx, position: int):
    if position < 1 or position > len(Saison23_24):
        await ctx.send("Spieltag nicht gefunden!")
    else:
        Spieltag = Saison23_24[position - 1]
        await ctx.send(f"{random.choice(DukeNukem)} {position}.Spieltag ist der {Spieltag}.")

# Start the bot with the token
bot.run('')
