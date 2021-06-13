from discord.ext import commands
from redis import Redis
import discord
import os
import redis

REDIS_URL = os.environ.get('REDIS_URL')
# データベースの指定
DATABASE_INDEX = 1  # 0じゃなくあえて1
# コネクションプールから１つ取得
pool = redis.ConnectionPool.from_url(REDIS_URL, db=DATABASE_INDEX)
# コネクションを利用
r = redis.StrictRedis(connection_pool=pool)

token = os.environ['DISCORD_BOT_TOKEN']
client = discord.Client()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    elif message.content.startswith('/set') and type(message.channel) == discord.DMChannel and client.user == message.channel.me:
        result = r.set('タイトル', message.content)
        print(message.content)
        print(result)
        
    elif message.content.startswith('/open'):
        result = r.get("タイトル")
        result = result.decode('unicode-escape')
        await message.channel.send(result)

client.run(token)
