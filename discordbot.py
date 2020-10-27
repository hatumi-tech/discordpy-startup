import discord
import os
Token = os.environ['DISCORD_BOT_TOKEN']

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    
    if message.content == '教えてチヨチャン':
        embed = discord.Embed(title="チヨチャンのヘルプ", description="コマンドリストです。",color=0xff0000)
        embed.add_field(name="教えてチヨチャン", value="このヘルプを表示します。",inline=False)
        embed.add_field(name="（ポケモン名）の図鑑", value="ポケモンのタイプ、種族値、特性を表示します。",inline=False)
        embed.add_field(name="（ポケモン名）の種族値", value="種族値を表示します。",inline=False)
        embed.add_field(name="（ポケモン名）のすばやさ", value="すばやさ、最速実数値、最遅実数値を表示します。",inline=False)
        embed.add_field(name="（ポケモン名）のとくせい", value="とくせいを表示します。夢特性もわかります。",inline=False)
        embed.add_field(name="（ポケモン名）の弱点", value="技を受ける際のタイプ別のダメージ倍率を表示します。",inline=False)
        await message.channel.send(embed=embed)
        
    

client.run(Token)
