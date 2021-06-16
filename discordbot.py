from discord.ext import commands
from redis import Redis
import discord
import os
import redis
import csv

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
    
    elif message.content.startswith('/kawasaki'):
        info = ("KAWASAKI HELL CITYへようこそ！")
        await message.channel.send(info)
    
    elif message.content.startswith('/help'):
        embed=discord.Embed(title="ちよのヘルプ", description="生まれ変わったちよちゃんのヘルプです。", color=0xff0000)
        embed.set_author(name="hatumichan")
        embed.add_field(name="/kawasaki", value="hell city", inline=False)
        embed.set_footer(text="よろしくな")
        await message.channel.send(embed=embed)

    elif message.content.startswith('/gamestart') and type(message.channel) != discord.DMChannel:
        r.flushdb()

        reader = csv.reader(open("./競走馬リスト.csv"))
        for row in reader:
            r.sadd("horse_name_all",str(row))

        info = ("ちよは競馬ポーカーの準備を完了しました。")
        await message.channel.send(info)

    elif message.content.endswith('頭の馬配って'):
        name = str(message.author)
        horse_num = message.content[0:len(message.content)-6]
        horse_num = int(horse_num)

        if horse_num > 10:
            info = ("ちよは10以上の数字がわかりません・・・。")
            await message.channel.send(info)
            return

        elif horse_num < 0:
            info = ("ちよは0以下の数字がわかりません・・・。")
            await message.channel.send(info)
            return

        else:
            for i in range(horse_num):
                info = r.spop("horse_name_all")
                info = utf8(info)
                await message.channel.send(info)
        
client.run(token)
