import os
import discord
from dotenv import load_dotenv
import requests

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

BASE = "http://127.0.0.1:5000/"
SEASON = 2021
NBA_API = f"http://data.nba.net/data/10s/prod/v1/{SEASON}/players.json"


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connecting to the following guild: \n'
        f'{guild.name} (id: {guild.id})'
    )


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Player Stat_type Stat_time_type
    message_split = message.content.split('/')
    if message_split[0] == '!gopher':
        player_data = requests.get(NBA_API)
        player_data = player_data.json()['league']['standard']
        player_name = message_split[1]
        stat_type = message_split[2]
        stat_time = message_split[3]
        player_data = list(filter(
            lambda player: player['firstName'].lower() + ' ' + player['lastName'].lower() == player_name.lower(), player_data))[0]
        player_id = player_data['personId']
        response = requests.get(
            BASE + f'player/{player_id}_{stat_type}_{stat_time}').json()
        embed = discord.Embed(
            title=player_name,
            color=discord.Color.blue()
        )
        if (stat_type == 'basic'):
            embed.add_field(name="PTS",
                            value=response['ppg'])
            embed.add_field(name="AST",
                            value=response['apg'])
            embed.add_field(name="REB",
                            value=response['rpg'])
        await message.channel.send(embed=embed)


client.run(TOKEN)
