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

# parse !gopher-basic command and creates embed


def parse_command_basic(message):
    message = message[14:]
    message_split = message.split(' ')
    stat_time = message_split[len(message_split)-1]
    player_name = message.replace(stat_time, '').strip()
    player_data = requests.get(NBA_API)
    player_data = player_data.json()['league']['standard']
    player_data = list(filter(
        lambda player: player['firstName'].lower() + ' ' + player['lastName'].lower() == player_name.lower(), player_data))[0]
    player_id = player_data['personId']
    display_name = player_data['firstName'] + ' ' + player_data['lastName']
    response = requests.get(
        BASE + f'player/{player_id}_basic_{stat_time}').json()
    embed = discord.Embed(
        title=display_name,
        color=discord.Color.blue()
    )
    embed.set_image(
        url=f"https://cdn.nba.com/headshots/nba/latest/1040x760/{player_id}.png")
    embed.add_field(name="PTS",
                    value=response['ppg'])
    embed.add_field(name="AST",
                    value=response['apg'])
    embed.add_field(name="REB",
                    value=response['rpg'])
    embed.add_field(name="FG%",
                    value=response['fgp'])
    embed.add_field(name='FT%',
                    value=response['ftp'])
    embed.add_field(name="3P%",
                    value=response['tpp'])

    return embed

# parse !gopher-advanced command and creates embed


def parse_command_advanced(message):
    message = message[17:]
    message_split = message.split(' ')
    stat_time = message_split[len(message_split)-1]
    player_name = message.replace(stat_time, '').strip()
    player_data = requests.get(NBA_API)
    player_data = player_data.json()['league']['standard']
    player_data = list(filter(
        lambda player: player['firstName'].lower() + ' ' + player['lastName'].lower() == player_name.lower(), player_data))[0]
    player_id = player_data['personId']
    display_name = player_data['firstName'] + ' ' + player_data['lastName']
    response = requests.get(
        BASE + f'player/{player_id}_advanced_{stat_time}').json()
    embed = discord.Embed(
        title=display_name,
        color=discord.Color.blue()
    )
    embed.set_image(
        url=f"https://cdn.nba.com/headshots/nba/latest/1040x760/{player_id}.png")
    embed.add_field(name="BPM",
                    value=response['BPM'])
    embed.add_field(name="OBPM",
                    value=response['OBPM'])
    embed.add_field(name="DBPM",
                    value=response['DBPM'])
    embed.add_field(name="WS",
                    value=response['WS'])
    embed.add_field(name='OWS',
                    value=response['OWS'])
    embed.add_field(name="DWS",
                    value=response['DWS'])
    return embed


@ client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connecting to the following guild: \n'
        f'{guild.name} (id: {guild.id})'
    )


@ client.event
async def on_message(message):
    if message.author == client.user:
        return
    message_split = message.content.split(' ')
    command = message_split[0]
    if command == '!gopher-basic':
        embed = parse_command_basic(message.content)
    elif command == '!gopher-advanced':
        embed = parse_command_advanced(message.content)
    await message.channel.send(embed=embed)


client.run(TOKEN)
