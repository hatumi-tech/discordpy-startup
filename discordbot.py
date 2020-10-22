# -*- coding: utf-8 -*-
from discord.ext import commands
import os
import traceback
import random

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def roll(dice : str):
    """サイコロはNdNの形式でお願いします"""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('サイコロはNdNの形式でお願いします')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)
    
@bot.command()
async def gacha(ctx):
    """オーナーズリーグ2010のガチャ結果を返します"""
    OLver = random.randint(1,4)
    
    if OLver == 1:
        CARDno=random.randint(1,240)
    elif OLver == 2:
        CARDno=random.randint(1,144)
    elif OLver == 3:
        CARDno=random.randint(1,186)
    elif OLver == 4:
        CARDno=random.randint(1,144)
                    
    gachakekka=( 'OL0%d,%d' % (OLver,CARDno) )                
    await ctx.send(gachakekka)
    
bot.run(token)
