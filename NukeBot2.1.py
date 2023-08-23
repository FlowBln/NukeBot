# Nukes Berlin Discord Bot by Florian Kondrot (and ChatGPT)
import discord
import random
import datetime
import json
from discord.ext import commands

# Connect to the Discord client
intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False
bot = commands.Bot(command_prefix='!', intents=intents)

def get_bot_token():
    with open('Testconfig.json', 'r') as config_file:
        data = json.load(config_file)
        return data['token']
        
# Databases
DukeNukem = ['Hail to the king, baby!', 'Yeah, piece of cake!', 'Groovy!', 'Let’s rock!', 'Come get some!', 'Damn I’m good.', 'Shake it, baby! ', 'Sometimes I even amaze myself.', 'Wohoo!']
Saison23_24 = ['01.10.23', '22.10.23', '19.11.23', '21.01.24', '18.02.24', '24.03.24', '21.04.24', '02.06.24']
spielergebnisse = {}
lottery_results = {}

# Variables



#Log in message in terminal
@bot.event
async def on_ready():
    print(f'Successfully logged in as {bot.user.name}')

# random response to messages
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if 'nukes' in message.content.lower():
        await message.channel.send(random.choice(DukeNukem))
    await bot.process_commands(message)

#wuerfelbude
@bot.command()
async def roll(ctx):
    dice = random.randint(1,6)
    await ctx.send(f'{random.choice(DukeNukem)} {ctx.author.display_name}, hat eine {dice} gewürfelt!')

#Abfrage Spieltage
@bot.command()
async def Spieltag(ctx, position: int):
    if position < 1 or position > len(Saison23_24):
        await ctx.send('Spieltag nicht gefunden!')
    else:
        gameday = Saison23_24[position -1]
        await ctx.send(f'{random.choice(DukeNukem)} Der {position}.Spieltag ist am {gameday}.')

#hinzufuegen von Spielergebnissen zu Spieltagen
@bot.command()
async def addresults(ctx, Spieltag: str, position: int, *, results: str):
    if position < 1 or position > len(Saison23_24):
        await ctx.send('Spieltag nicht gefunden!')
    else:
        gameday = Saison23_24[position -1]
        spielergebnisse.setdefault(gameday, {}).setdefault(ctx.author.display_name, []).append(results)
        await ctx.send(f'{random.choice(DukeNukem)} Die Ergebnisse {results} für den {position}.Spieltag wurden für {ctx.author.display_name} gespeichert.')

#Spielergebnisse anzeigen lassen
@bot.command()
async def results(ctx):
    result_message = "Eingetragene Ergebnisse:\n"
    
    for gameday, ergebnisse in spielergebnisse.items():
        result_message += f'\n**{gameday}:**\n'
        for user, ergebnis_list in ergebnisse.items():
            ergebnis_text = ', '.join(ergebnis_list)
            result_message += f'{user}: {ergebnis_text}\n'
    
    await ctx.send(result_message)
 
#Lottery für die Spieltage
@bot.command()
async def lottery(ctx, Spieltag: str, position: int):
    gameday = Saison23_24[position -1]
    if position < 1 or position > len(Saison23_24):
        await ctx.send("Spieltag nicht gefunden!")
        return
    
    if gameday in lottery_results:
        random_number, winner = lottery_results[gameday]
    else:
        if gameday not in spielergebnisse:
            await ctx.send(f"Keine Spiele für den {position}.Spieltag am {gameday} gefunden")
            return

    random_number = random.randint(100, 300)
    winner = None
    for user, results in spielergebnisse[gameday].items():
        for result in results:
            result_numbers = [int(num.strip()) for num in result.split()]
            if random_number in result_numbers:
                winner = user
                break

    lottery_results[gameday] = (random_number, winner)

    if winner:
        await ctx.send(f"{random.choice(DukeNukem)} Der Gewinner für den {position}.Spieltag, mit einem Ergebnis von {random_number} ist... \n{winner.upper()}")
    else:
        await ctx.send(f"Gelost wurde ein Spielergebnis von {random_number}. Für den {position}.Spieltag gibt es also keinen Gewinner. Viel erfolg beim nächsten Spieltag!")


# Start the bot with the token
bot.run(get_bot_token())
