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

INITIAL_CUR = 0

def utf8(byte):
    if byte:
        return str(byte, 'utf-8')

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    elif message.content.startswith('/set') and type(message.channel) == discord.DMChannel and client.user == message.channel.me:
        name = str(message.author)
        answer = str(message.content)
        answer = answer.strip("/set")
        
        result = r.set(name,answer)
        
        info = (f'{name}さんの回答{answer}を、ちよ覚えました。')
        await message.channel.send(info)
        
    elif message.content.startswith('/show') and type(message.channel) == discord.DMChannel and client.user == message.channel.me:
        name = str(message.author)
        answer = r.get(name)
        answer = answer.decode(encoding = 'utf-8')
        
        info = (f'{name}さんの回答は現在{answer}です。')
        await message.channel.send(info)
        
    elif message.content.startswith('/open') and type(message.channel) != discord.DMChannel:
        next_cur = INITIAL_CUR
        
        while True:
            res_scan = r.scan(next_cur)             # SCAN
            next_cur = res_scan[0]
            if res_scan[1]:
                res_mget = r.mget(res_scan[1])      # MGET
                for key, val in zip(res_scan[1], res_mget):
                    info = (f'{utf8(key)}さんの回答は{utf8(val)}です。')
                    await message.channel.send(info)
            if next_cur == INITIAL_CUR:
                break
        pass
    
    elif message.content.startswith('/flushdb') and type(message.channel) != discord.DMChannel:
        r.flushdb
        info = ("ちよはすべてを忘れてしまいました・・・。")
        await message.channel.send(info)
        
client.run(token)
