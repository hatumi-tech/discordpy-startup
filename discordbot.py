from discord.ext import commands
import discord
import os
import traceback

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    elif type(message.channel) == discord.DMChannel and client.user == message.channel.me:
        print(message.content)
    
bot.run(token)
