# -*- coding: utf-8 -*-
from discord.ext import commands
import os
import traceback
import random
import gspread
import json
import sys
import re
import requests

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']

from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

#認証情報設定
#ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
credential = {
                "type": "service_account",
                "project_id": os.environ['SHEET_PROJECT_ID'],
                "private_key_id": os.environ['SHEET_PRIVATE_KEY_ID'],
                "private_key": os.environ.get('SHEET_PRIVATE_KEY').replace('\\n', '\n'),
                "client_email": os.environ['SHEET_CLIENT_EMAIL'],
                "client_id": os.environ['SHEET_CLIENT_ID'],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url":  os.environ['SHEET_CLIENT_X509_CERT_URL']
             }

credentials = ServiceAccountCredentials.from_json_keyfile_dict(credential, scope)

#OAuth2の資格情報を使用してGoogle APIにログインします。
gc = gspread.authorize(credentials)

#共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
SPREADSHEET_KEY = '1cRNckSIqC3N9R7M3auoC9Uq_SCBXssgv7FaCU-xwFuY'

#共有設定したワークブックを開く
workbook = gc.open_by_key(SPREADSHEET_KEY)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error,commands.MissingRequiredArgument):
       await ctx.send('ホットサンドメーカー買いました（引数がないエラーです）')
    else:
       orig_error = getattr(error, "original", error)
       error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
       await ctx.send(error_msg)

@bot.event
async def on_message(message):
    # 送り主がBotだった場合反応したくないので
    if message.author.bot:
        return
      
    if message.content == 'はつみの図鑑':
        message_send = "このbotの作成者"
    
    # 「図鑑」で始まるか調べる
    elif re.match('.+の図鑑$', message.content):
      
        worksheet = workbook.sheet1
        m = message.content[0:len(message.content)-3]
    
        try:
            cell = worksheet.find(m)
        except gspread.exceptions.CellNotFound:
            await message.channel.send("いないポケモンだよ")
        return
 
        # メッセージが送られてきたチャンネルへメッセージを送ります
        message_send = "```"
        row_list = worksheet.row_values(cell.row)
        del row_list[0:2]
        row_list = str(row_list)
        message_send = message_send + m + " \n"  + '  HP   攻撃   防御   特攻   特防   素早   合計\n'
        message_send = message_send + row_list
    
    elif re.match('.+のとくせい$', message.content):
      
        message_send = "```"
      
        worksheet = workbook.get_worksheet(2)
        m = message.content[0:len(message.content)-5]

        try:
            cell = worksheet.find(m)
        except gspread.exceptions.CellNotFound:
            await message.channel.send("ないとくせいだよ")
            return
          
        yumetokusei = ""
        
        tokusei1 = worksheet.cell(cell.row,3).value
        tokusei2 = worksheet.cell(cell.row,4).value
        tokusei3 = worksheet.cell(cell.row,5).value
    
        tokusei1 = str(tokusei1)
        tokusei2 = str(tokusei2)
        tokusei3 = str(tokusei3)
    
        worksheet = workbook.get_worksheet(3)
    
        try:
            cell = worksheet.find(tokusei1)
        except gspread.exceptions.CellNotFound:
            pass
        
        tokusei1info = worksheet.cell(cell.row,2).value
        
        if "*" in tokusei2:
            tokusei2 = tokusei2[1:]
            yumetokusei = tokusei2
        else:
            pass
    
        try:
            cell = worksheet.find(tokusei2)
        except gspread.exceptions.CellNotFound:
            pass
        
        tokusei2info = worksheet.cell(cell.row,2).value
    
        if "*" in tokusei3:
            tokusei3 = tokusei3[1:]
            yumetokusei = tokusei3
        else:
            pass
      
        try:
            cell = worksheet.find(tokusei3)
        except gspread.exceptions.CellNotFound:
            pass
        
        tokusei3info = worksheet.cell(cell.row,2).value
    
        if yumetokusei == "":
            yumetokusei = "なし"
        else:
            pass
        
        yumetokusei = str(yumetokusei)
       
        tokuseimessage = "とくせいは" + " \n" + tokusei1 + "：" + tokusei1info +  " \n" + tokusei2 + "：" + tokusei2info +  " \n" + tokusei3 + "：" + tokusei3info +  " \n"+ "夢特性は" + yumetokusei
        message_send = message_send + tokuseimessage
        message_send = message_send + "```"
       
    elif re.match('.+のすばやさ$', message.content):
      
         message_send = "```"
        
         worksheet = workbook.sheet1
         m = message.content[0:len(message.content)-5]
    
         try:
             cell = worksheet.find(m)
         except gspread.exceptions.CellNotFound:
             await ctx.send("いないポケモンだよ")
             return
        
         speed1 = worksheet.cell(cell.row,8).value
         speed1 = int(speed1)
         speed1MAX = int((speed1+52)*1.1)
    
         saisoku1 = str(speed1MAX)
    
         text = "{}のすばやさは{}、最速実数値{}"
         message_send = message_send + text.format(m,speed1,saisoku1)
         message_send = message_send + "```"

    await message.channel.send(message_send)
            
bot.run(token)
