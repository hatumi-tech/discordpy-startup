from discord.ext import commands
import discord
import os

token = os.environ['DISCORD_BOT_TOKEN']
client = discord.Client()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("川崎"):
        await message.channel.send("Hell City 川崎!")

    elif type(message.channel) == discord.DMChannel and client.user == message.channel.me:
        print(message.content)

client.run(token)
