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
    with open('Nukeconfig.json', 'r') as config_file:
        data = json.load(config_file)
        return data['token']
        
# Databases
DukeNukem = ['Hail to the king, baby!', 'Yeah, piece of cake!', 'Groovy!', 'Let’s rock!', 'Come get some!', 'Damn I’m good.', 'Shake it, baby! ', 'Sometimes I even amaze myself.', 'Wohoo!']
Saison23_24 = ['01.10.23', '22.10.23', '19.11.23', '21.01.24', '18.02.24', '24.03.24', '21.04.24', '02.06.24']
spielergebnisse = {}

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
        Spieltag = Saison23_24[position - 1]
        await ctx.send(f'{random.choice(DukeNukem)} Der {position}.Spieltag ist der {Spieltag}.')

#hinzufuegen von Spielergebnissen
@bot.command()
async def add_results(ctx, spieltag: str, position: int, *, results: str):
    if position < 1 or position > len(Saison23_24):
        await ctx.send('Spieltag not found!')
    else:
        spielergebnisse.setdefault(Saison23_24[position - 1], {}).setdefault(ctx.author.display_name, []).append(results)
        await ctx.send(f'{random.choice(DukeNukem)} Ergebnisse {results} für den {position}.Spieltag wurden für {ctx.author.display_name} gespeichert.')

#Spielergebnisse anzeigen lassen
@bot.command()
async def results(ctx):
    result_message = "Eingetragene Ergebnisse:\n"

    for spieltag, ergebnisse in spielergebnisse.items():
        result_message += f'\n**{spieltag}:**\n'
        for user, ergebnis_list in ergebnisse.items():
            ergebnis_text = ', '.join(ergebnis_list)
            result_message += f'{user}: {ergebnis_text}\n'
    
    await ctx.send(result_message)
    
#Lottery für die Spieltage
@bot.command()
@commands.has_permissions(administrator=True)
async def lottery(ctx, spieltag: str, position: int):
    if spieltag not in spielergebnisse:
        await ctx.send("Keine Spiele für den Spieltag gefunden")
        return

    if position < 1 or position > len(spielergebnisse[spieltag]):
        await ctx.send("Spieltag not found!")
        return

    if spieltag in spielergebnisse and len(spielergebnisse[spieltag][position - 1]) > 0:
        if 'lottery_results' not in ctx.bot.data:
            ctx.bot.data['lottery_results'] = {}

        if spieltag not in ctx.bot.data['lottery_results']:
            zufallszahl = random.randint(100, 300)
            gewinner = None
            gewinn_diff = float('inf')
            for user, ergebnisse in spielergebnisse[spieltag][position - 1].items():
                for ergebnis in ergebnisse:
                    diff = abs(int(ergebnis) - zufallszahl)
                    if diff < gewinn_diff:
                        gewinn_diff = diff
                        gewinner = user

            if gewinner:
                ctx.bot.data['lottery_results'][spieltag] = (zufallszahl, gewinner, datetime.datetime.now())
                await ctx.send(f"Der Gewinner für den {spieltag}.Spieltag (Position {position}) ist {gewinner} mit der Zahl {zufallszahl}!")
            else:
                ctx.bot.data['lottery_results'][spieltag] = (zufallszahl, None, datetime.datetime.now())
                await ctx.send(f"Es gibt keinen Gewinner für den (Position {position}){spieltag}.Spieltag .")
        else:
            zufallszahl, gewinner, timestamp = ctx.bot.data['lottery_results'][spieltag]
            if gewinner:
                await ctx.send(f"Die Lotterie für den {spieltag}.Spieltag (Position {position}) wurde bereits ausgeführt.\n"
                               f"Gewinner: {gewinner} mit der Zahl {zufallszahl}.\n"
                               f"Ausgeführt am: {timestamp}")
            else:
                await ctx.send(f"Die Lotterie für den {spieltag}.Spieltag (Position {position}) wurde bereits ausgeführt.\n"
                               f"Es gibt keinen Gewinner.\n"
                               f"Ausgeführt am: {timestamp}")
    else:
        await ctx.send("Keine Ergebnisse für diesen Spieltag und diese Position gefunden!")


# Start the bot with the token
bot.run(get_bot_token())
