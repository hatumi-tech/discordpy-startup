# -*- coding: utf-8 -*-
from discord.ext import commands
import os
import traceback
import random
import gspread
import json
import sys
import re

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
    
    # 「図鑑」で始まるか調べる
    if message.content == 'はつみの図鑑':
       message_send = "このbotの作成者"

    elif re.match('.+の図鑑$', message.content):
         
        worksheet = workbook.sheet1
        m = message.content[0:len(message.content)-3]
    
        try:
          cell = worksheet.find(m)
        except gspread.exceptions.CellNotFound:
          await ctx.send("いないポケモンだよ")
          return
 
        # メッセージが送られてきたチャンネルへメッセージを送ります
        message_send = "```"
            
        row_list = worksheet.row_values(cell.row)
        message_send = message_send + m + " \n"  + '  HP   攻撃   防御   特攻   特防   素早   合計\n'
        del row_list[0:2]
        row_list = str(row_list)
        message_send = message_send + row_list
        message_send = message_send + "```"

    await message.channel.send(message_send)
            
@bot.command()
async def tae(ctx,arg1,arg2,arg3):
    """耐えるかな？ツールです。AのポケモンがBにCの威力の技を打った時のダメージを計算します。"""
    
    worksheet = workbook.sheet1
    
    try:
        cell = worksheet.find(arg1)
    except gspread.exceptions.CellNotFound:
            await ctx.send("いないポケモンだよ")
            return
    
    atk2 = worksheet.cell(cell.row,4).value
    spatk2 = worksheet.cell(cell.row,6).value
    
    try:
        cell = worksheet.find(arg2)
    except gspread.exceptions.CellNotFound:
            await ctx.send("いないポケモンだよ")
            return
        
    def1 = worksheet.cell(cell.row,5).value
    spdef1 = worksheet.cell(cell.row,7).value
    
    def1 = int(def1)
    spdef1 = int(spdef1)
    atk2 = int(atk2)
    spatk2 = int(spatk2)
    arg3 = int(arg3)
    waza = int(arg3/50)

    butsuri = (22*(waza))*((atk2)/(def1))
    butsuri = int((int(butsuri)+2)*1.5)
    butsuri = str(butsuri)
    tokushu = (22*(waza))*((spatk2)/(spdef1))
    tokushu = int((int(tokushu)+2)*1.5)
    tokushu = str(tokushu)
    
    text = "{}の威力{}の技が{}に与える物理ダメージはだいたい{}です。特殊ダメージはだいたい{}です。タイプ一致技は1.5倍してください。"
    result = text.format(arg1,arg3,arg2,butsuri,tokushu)
    
    await ctx.send(result)

@bot.command()
async def spc(ctx,arg1,arg2):
    """すばやさの種族値を比較します"""
    worksheet = workbook.sheet1
    
    try:
        cell = worksheet.find(arg1)
    except gspread.exceptions.CellNotFound:
           await ctx.send("いないポケモンだよ")
           return
        
    speed1 = worksheet.cell(cell.row,8).value
    
    try:
        cell = worksheet.find(arg2)
    except gspread.exceptions.CellNotFound:
           await ctx.send("いないポケモンだよ")
           return
        
    speed2 = worksheet.cell(cell.row,8).value
    
    speed1 = int(speed1)
    speed2 = int(speed2)
    
    speed1MAX = int((speed1+52)*1.1)
    speed2MAX = int((speed2+52)*1.1)
    saisoku1 = str(speed1MAX)
    saisoku2 = str(speed2MAX)
    
    text = "{}のすばやさは{}、最速実数値{}\n{}のすばやさは{}、最速実数値{}"
    result = text.format(arg1,speed1,saisoku1,arg2,speed2,saisoku2)
        
    await ctx.send(result)
    
@bot.command()
async def sp(ctx,arg):
    """すばやさの種族値を表示します"""
    worksheet = workbook.sheet1

    try:
        cell = worksheet.find(arg)
    except gspread.exceptions.CellNotFound:
           await ctx.send("いないポケモンだよ")
           return
        
    speed1 = worksheet.cell(cell.row,8).value
    
    speed1 = int(speed1)
    
    speed1MAX = int((speed1+52)*1.1)
    saisoku1 = str(speed1MAX)
    
    text = "{}のすばやさは{}、最速実数値{}"
    result = text.format(arg,speed1,saisoku1)
        
    await ctx.send(result)
    
@bot.command()
async def tokusei(ctx,arg):
    """ポケモンを指定するとそのとくせいを表示します"""
    worksheet = workbook.get_worksheet(2)

    try:
        cell = worksheet.find(arg)
    except gspread.exceptions.CellNotFound:
           await ctx.send("ないとくせいだよ")
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
        
    yumetokusei = str(yumetokusei)
    
    text = "{}のとくせいは\n{}:{}\n{}:{}\n{}:{}\n夢特性は{}"
    result = text.format(arg,tokusei1,tokusei1info,tokusei2,tokusei2info,tokusei3,tokusei3info,yumetokusei)
        
    await ctx.send(result)
    
@bot.command()
async def waza(ctx,arg):
    """わざについて表示します"""
    worksheet = workbook.get_worksheet(1)

    try:
        cell = worksheet.find(arg)
    except gspread.exceptions.CellNotFound:
           await ctx.send("第８世代に存在しないわざだよ")
           return
        
    wazatype = worksheet.cell(cell.row,2).value
    wazapower = worksheet.cell(cell.row,3).value
    wazaaccu = worksheet.cell(cell.row,4).value
    wazapp = worksheet.cell(cell.row,5).value
    wazaclass = worksheet.cell(cell.row,6).value
    
    wazatype = str(wazatype)
    wazapower = str(wazapower)
    wazaaccu = str(wazaaccu)
    wazapp = str(wazapp)
    wazaclass = str(wazaclass)
    
    text = "{}はタイプ：{}、いりょく{}、めいちゅう{}、PP{}の{}技。"
    result = text.format(arg,wazatype,wazapower,wazaaccu,wazapp,wazaclass)
        
    await ctx.send(result)
    
@bot.command()
async def olgacha(ctx):
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
    
@bot.command()
async def ping(ctx):
    """ぴんぽん"""
    await ctx.send('pong')

bot.run(token)
