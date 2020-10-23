# -*- coding: utf-8 -*-
from discord.ext import commands
import os
import traceback
import random
import gspread
import json

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

#共有設定したスプレッドシートのシート1を開く
worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

@bot.command()
async def psc(ctx,arg1,arg2):
    """すばやさの種族値を比較します"""
    cell = worksheet.find(arg1)
    speed1 = worksheet.cell(cell.row, 8).value
    cell = worksheet.find(arg2)
    speed2 = worksheet.cell(cell.row, 8).value
    
    if speed1 > speed2:
        kekka =( '%f,%fで%fが速いです。' % (speed1,speed2,arg1) ) 
    elif speed1 < speed2:
        kekka =( '%f,%fで%fが速いです。' % (speed1,speed2,arg2) ) 
    elif speed1 == speed2:
        kekka =( 'どちらも%fで同速です。' % (speed1) ) 
        
    await ctx.send(kekka)
    
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
    
@bot.command()
async def ping(ctx):
    """ぴんぽん"""
    await ctx.send('pong')

bot.run(token)
