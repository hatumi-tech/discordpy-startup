from discord.ext import commands
import discord
import os
import redis
import r

conn = r.connect() # このconnを通じて操作する

def connect():
    return redis.from_url(
        url=os.environ.get('REDIS_URL'), # 環境変数にあるURLを渡す
        decode_responses=True, # 日本語の文字化け対策のため必須
    )

token = os.environ['DISCORD_BOT_TOKEN']
client = discord.Client()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    elif type(message.channel) == discord.DMChannel and client.user == message.channel.me:
        result = r.set('タイトル', message.content)
        print(message.content)
        print(result)

client.run(token)
