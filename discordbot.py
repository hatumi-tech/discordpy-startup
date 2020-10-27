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
import discord

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

message_send = ""

@bot.event
async def on_message(message):
    # 送り主がBotだった場合反応したくないので
    if message.author.bot:
        return
      
    if message.content == 'はつみの図鑑':
        message_send = "https://yakkun.com/swsh/zukan/n763"
        await message.channel.send(message_send)
        return
        
    if message.content == 'スピーカの図鑑':
        message_send = "https://ja.wikipedia.org/wiki/%E3%83%9B%E3%83%83%E3%83%88%E3%82%B5%E3%83%B3%E3%83%89%E3%83%A1%E3%83%BC%E3%82%AB%E3%83%BC"
        await message.channel.send(message_send)
        return
        
    if message.content == 'こにしの図鑑':
        message_send = "https://yakkun.com/swsh/zukan/n701"
        await message.channel.send(message_send)
        return
      
    if message.content == '教えてチヨチャン':
        embed = discord.Embed(title="チヨチャンのヘルプ", description="コマンドリストです。",color=0xff0000)
        embed.add_field(name="教えてチヨチャン", value="このヘルプを表示します。",inline=False)
        embed.add_field(name="（ポケモン名）の図鑑", value="ポケモンのタイプ、種族値、特性を表示します。",inline=False)
        embed.add_field(name="（ポケモン名）の種族値", value="種族値を表示します。",inline=False)
        embed.add_field(name="（ポケモン名）のすばやさ", value="すばやさ、最速実数値、最遅実数値を表示します。",inline=False)
        embed.add_field(name="（ポケモン名）のとくせい", value="とくせいを表示します。夢特性もわかります。",inline=False)
        embed.add_field(name="（ポケモン名）の弱点", value="技を受ける際のタイプ別のダメージ倍率を表示します。",inline=False)
        await message.channel.send(embed=embed)
        return
        
    if message.content == 'ちーちくの図鑑':
        message_send = "https://yakkun.com/swsh/zukan/n128"
        await message.channel.send(message_send)
        return
     
    if re.match('.+の図鑑$', message.content):
      
         message_send = "```"
        
         worksheet = workbook.sheet1
         m = message.content[0:len(message.content)-3]
        
         if m == "":
            return
    
         try:
             cell = worksheet.find(m)
         except gspread.exceptions.CellNotFound:
             await message.channel.send("いないポケモン。私に価値はありません。ここにあるのは無です")
             return
         
         hp1 = worksheet.cell(cell.row,3).value
         atk1 = worksheet.cell(cell.row,4).value
         def1 = worksheet.cell(cell.row,5).value
         spatk1 = worksheet.cell(cell.row,6).value
         spdef1 = worksheet.cell(cell.row,7).value
         speed1 = worksheet.cell(cell.row,8).value
         all1 = worksheet.cell(cell.row,9).value
         type1 = worksheet.cell(cell.row,11).value
         type2 = worksheet.cell(cell.row,12).value
         
         tetsuurl = "https://yakkun.com/swsh/zukan/"
         id1 = worksheet.cell(cell.row,10).value
         id1 = str(id1)
         
         worksheet = workbook.get_worksheet(2)
        
         try:
             cell = worksheet.find(m)
         except gspread.exceptions.CellNotFound:
             await message.channel.send("ないとくせい。お前は馬鹿ですね。あるいは…ばーか。お嬢さまならそう言うでしょう")
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
         
         text = "{}はタイプ{}、{}" +  " \n" + "H{}-A{}-B{}-C{}-D{}-S{}-ALL{}" +  " \n"
         
         message_send = text.format(m,type1,type2,hp1,atk1,def1,spatk1,spdef1,speed1,all1) + tokuseimessage + " \n"  + tetsuurl + id1
        
         message_send = message_send + "```"
    
    # 「種族値」で始まるか調べる
    elif re.match('.+の種族値$', message.content):
      
         message_send = "```"
        
         worksheet = workbook.sheet1
         m = message.content[0:len(message.content)-4]
        
         if m == "":
            return
          
         try:
             cell = worksheet.find(m)
         except gspread.exceptions.CellNotFound:
             await message.channel.send("いないポケモン。お前は馬鹿ですね。あるいは…ばーか。お嬢さまならそう言うでしょう")
             return
        
         hp1 = worksheet.cell(cell.row,3).value
         atk1 = worksheet.cell(cell.row,4).value
         def1 = worksheet.cell(cell.row,5).value
         spatk1 = worksheet.cell(cell.row,6).value
         spdef1 = worksheet.cell(cell.row,7).value
         speed1 = worksheet.cell(cell.row,8).value
         all1 = worksheet.cell(cell.row,9).value
        
         text = "{}の種族値はH{}-A{}-B{}-C{}-D{}-S{}-ALL{}"
         message_send = message_send + text.format(m,hp1,atk1,def1,spatk1,spdef1,speed1,all1)
         message_send = message_send + "```"
    
    elif re.match('.+のとくせい$', message.content):
      
        message_send = "```"
      
        worksheet = workbook.get_worksheet(2)
        m = message.content[0:len(message.content)-5]
        
        if m == "":
            return

        try:
            cell = worksheet.find(m)
        except gspread.exceptions.CellNotFound:
            await message.channel.send("ないとくせい。お前は馬鹿ですね。あるいは…ばーか。お嬢さまならそう言うでしょう")
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
        chiyo = " \n"+ "ごきげんよう。……次があるかは分かりませんが"
        
        message_send = message_send + chiyo
       
    elif re.match('.+のすばやさ$', message.content):
      
         message_send = "```"
        
         worksheet = workbook.sheet1
         m = message.content[0:len(message.content)-5]
        
         if m == "":
            return
    
         try:
             cell = worksheet.find(m)
         except gspread.exceptions.CellNotFound:
             await message.channel.send("いないポケモン。何をしようとしているのですか。その行為に意味はありますか")
             return
        
         speed1 = worksheet.cell(cell.row,8).value
         speed1 = int(speed1)
         speed1MAX = int((speed1+52)*1.1)
         speed1MIN = int((speed1+5)*0.9)
    
         saisoku1 = str(speed1MAX)
         saiti1 = str(speed1MIN)
    
         text = "{}のすばやさは{}、最速実数値{}、最遅実数値{}"
         message_send = message_send + text.format(m,speed1,saisoku1,saiti1)
         message_send = message_send + "```"
          
         chiyo = " \n"+ "お嬢さまに感謝してください。"
         message_send = message_send + chiyo
          
    elif re.match('.+の弱点$', message.content):
      
         message_send = "```"
        
         worksheet = workbook.sheet1
         m = message.content[0:len(message.content)-3]
        
         if m == "":
            return
    
         try:
             cell = worksheet.find(m)
         except gspread.exceptions.CellNotFound:
             await message.channel.send("いないポケモン。何をしようとしているのですか。その行為に意味はありますか")
             return
        
         type1 = worksheet.cell(cell.row,11).value
         type2 = worksheet.cell(cell.row,12).value
         
         ###倍率は最初1倍###

         normal = 1
         fire = 1
         water = 1
         grass = 1
         electric = 1
         ice = 1
         fighting = 1
         poison = 1
         ground = 1
         flying = 1
         psychic = 1
         bug = 1
         rock = 1
         ghost = 1
         dragon = 1
         dark = 1
         steel = 1
         fairy = 1
                
         if type1 == "ノーマル":
             fighting = fighting*2
             ghost = ghost*0
                    
         elif type1 == "ほのお":
             water = water*2
             ground = ground*2
             rock = rock*2
             fire = fire*0.5
             grass = grass*0.5
             ice = ice*0.5
             bug = bug*0.5
             steel = steel*0.5
             fairy = fairy*0.5
                    
         elif type1 == "みず":
             electric = electric*2
             grass = grass*2
             fire = fire*0.5
             water = water*0.5
             ice = ice*0.5
             steel = steel*0.5
                    
         elif type1 == "でんき":
             ground = ground*2
             electric = electric*0.5
             flying = flying*0.5
             steel = steel*0.5
                    
         elif type1 == "くさ":
             fire = fire*2
             ice = ice*2
             poison = poison*2
             flying = flying*2
             bug = bug*2
             water = water*0.5
             electric = electric*0.5
             grass = grass*0.5
             ground = ground*0.5
                    
         elif type1 == "こおり":
             fire = fire*2
             fighting = fighting*2
             rock = rock*2
             steel = steel*2
             ice = ice*0.5
                    
         elif type1 == "かくとう":
             flying = flying*2
             psychic = psychic*2
             fairy = fairy*2
             bug = bug*0.5
             rock = rock*0.5
             dark = dark*0.5
                    
         elif type1 == "どく":
             ground = ground*2
             psychic = psychic*2
             grass = grass*0.5
             fighting = fighting*0.5
             poison = poison*0.5
             bug = bug*0.5
             fairy = fairy*0.5
                    
         elif type1 == "じめん":
             water = water*2
             grass = grass*2
             ice = ice*2
             poison = poison*0.5
             rock = rock*0.5
             electric = electric*0
                    
         elif type1 == "ひこう":
             electric = electric*2
             ice = ice*2
             rock = rock*2
             grass = grass*0.5
             fighting = fighting*0.5
             bug = bug*0.5
             ground = ground*0
                    
         elif type1 == "エスパー":
             bug = bug*2
             ghost = ghost*2
             dark = dark*2
             fighting = fighting*0.5
             psychic = psychic*0.5
                    
         elif type1 == "むし":
             fire = fire*2
             flying = flying*2
             rock = rock*2
             grass = grass*0.5
             fighting = fighting*0.5
             ground = ground*0.5
                    
         elif type1 == "いわ":
             water = water*2
             grass = grass*2
             fighting = fighting*2
             ground = ground*2
             steel = steel*2
             normal = normal*0.5
             fire = fire*0.5
             poison = poison*0.5
             flying = flying*0.5
                    
         elif type1 == "ゴースト":
             ghost = ghost*2
             dark = dark*2
             poison = poison*0.5
             bug = bug*0.5
             normal = normal*0
             fighting = fighting*0
                    
         elif type1 == "ドラゴン":
             ice = ice*2
             dragon = dragon*2
             fairy = fairy*2
             fire = fire*0.5
             water = water*0.5
             electric = electric*0.5
             grass = grass*0.5
                    
         elif type1 == "あく":
             fighting = fighting*2
             bug = bug*2
             fairy = fairy*2
             ghost = ghost*0.5
             dark = dark*0.5
             psychic = psychic*0
                    
         elif type1 == "はがね":
             fire = fire*2
             fighting = fighting*2
             ground = ground*2
             normal = normal*0.5
             grass = grass*0.5
             ice = ice*0.5
             flying = flying*0.5
             psychic = psychic*0.5
             bug = bug*0.5
             rock = rock*0.5
             dragon = dragon*0.5
             steel = steel*0.5
             fairy = fairy*0.5
             poison = poison*0
                    
         elif type1 == "フェアリー":
             poison = poison*2
             steel = steel*2
             fighting = fighting*0.5
             bug = bug*0.5
             dark = dark*0.5
             dragon = dragon*0
              
         else:
          pass
             
         if type2 == "ノーマル":
             fighting = fighting*2
             ghost = ghost*0
                    
         elif type2 == "ほのお":
             water = water*2
             ground = ground*2
             rock = rock*2
             fire = fire*0.5
             grass = grass*0.5
             ice = ice*0.5
             bug = bug*0.5
             steel = steel*0.5
             fairy = fairy*0.5
                    
         elif type2 == "みず":
             electric = electric*2
             grass = grass*2
             fire = fire*0.5
             water = water*0.5
             ice = ice*0.5
             steel = steel*0.5
                    
         elif type2 == "でんき":
             ground = ground*2
             electric = electric*0.5
             flying = flying*0.5
             steel = steel*0.5
                    
         elif type2 == "くさ":
             fire = fire*2
             ice = ice*2
             poison = poison*2
             flying = flying*2
             bug = bug*2
             water = water*0.5
             electric = electric*0.5
             grass = grass*0.5
             ground = ground*0.5
                    
         elif type2 == "こおり":
             fire = fire*2
             fighting = fighting*2
             rock = rock*2
             steel = steel*2
             ice = ice*0.5
                    
         elif type2 == "かくとう":
             flying = flying*2
             psychic = psychic*2
             fairy = fairy*2
             bug = bug*0.5
             rock = rock*0.5
             dark = dark*0.5
                    
         elif type2 == "どく":
             ground = ground*2
             psychic = psychic*2
             grass = grass*0.5
             fighting = fighting*0.5
             poison = poison*0.5
             bug = bug*0.5
             fairy = fairy*0.5
                    
         elif type2 == "じめん":
             water = water*2
             grass = grass*2
             ice = ice*2
             poison = poison*0.5
             rock = rock*0.5
             electric = electric*0
                    
         elif type2 == "ひこう":
             electric = electric*2
             ice = ice*2
             rock = rock*2
             grass = grass*0.5
             fighting = fighting*0.5
             bug = bug*0.5
             ground = ground*0
                    
         elif type2 == "エスパー":
             bug = bug*2
             ghost = ghost*2
             dark = dark*2
             fighting = fighting*0.5
             psychic = psychic*0.5
                    
         elif type2 == "むし":
             fire = fire*2
             flying = flying*2
             rock = rock*2
             grass = grass*0.5
             fighting = fighting*0.5
             ground = ground*0.5
                    
         elif type2 == "いわ":
             water = water*2
             grass = grass*2
             fighting = fighting*2
             ground = ground*2
             steel = steel*2
             normal = normal*0.5
             fire = fire*0.5
             poison = poison*0.5
             flying = flying*0.5
                    
         elif type2 == "ゴースト":
             ghost = ghost*2
             dark = dark*2
             poison = poison*0.5
             bug = bug*0.5
             normal = normal*0
             fighting = fighting*0
                    
         elif type2 == "ドラゴン":
             ice = ice*2
             dragon = dragon*2
             fairy = fairy*2
             fire = fire*0.5
             water = water*0.5
             electric = electric*0.5
             grass = grass*0.5
                    
         elif type2 == "あく":
             fighting = fighting*2
             bug = bug*2
             fairy = fairy*2
             ghost = ghost*0.5
             dark = dark*0.5
             psychic = psychic*0
                    
         elif type2 == "はがね":
             fire = fire*2
             fighting = fighting*2
             ground = ground*2
             normal = normal*0.5
             grass = grass*0.5
             ice = ice*0.5
             flying = flying*0.5
             psychic = psychic*0.5
             bug = bug*0.5
             rock = rock*0.5
             dragon = dragon*0.5
             steel = steel*0.5
             fairy = fairy*0.5
             poison = poison*0
                    
         elif type2 == "フェアリー":
             poison = poison*2
             steel = steel*2
             fighting = fighting*0.5
             bug = bug*0.5
             dark = dark*0.5
             dragon = dragon*0
              
         else:
          pass
        
         normal = float(normal)
         fire = float(fire)
         water = float(water)
         grass = float(grass)
         electric = float(electric)
         ice = float(ice)
         fighting = float(fighting)
         poison = float(poison)
         ground = float(ground)
         flying = float(flying)
         psychic = float(psychic)
         bug = float(bug)
         rock = float(rock)
         ghost = float(ghost)
         dragon = float(dragon)
         dark = float(dark)
         steel = float(steel)
         fairy = float(fairy)
                    
         text = "{}のダメージ倍率"+" \n"+"ノーマル:{}倍、ほのお:{}倍、みず:{}倍、でんき:{}倍"+" \n"+"くさ:{}倍、こおり:{}倍、かくとう:{}倍、どく:{}倍"+" \n"
         text2 = "じめん:{}倍、ひこう:{}倍、エスパー:{}倍、むし:{}倍"+" \n"+"いわ:{}倍、ゴースト:{}倍、ドラゴン:{}倍、あく:{}倍"+" \n"+"はがね:{}倍、フェアリー:{}倍"                
         
         message_send = message_send + text.format(m,normal,fire,water,electric,grass,ice,fighting,poison)
         message_send = message_send + text2.format(ground,flying,psychic,bug,rock,ghost,dragon,dark,steel,fairy)
         message_send = message_send + "```"
          
         chiyo = " \n"+ "お嬢さまに感謝してください。"
         message_send = message_send + chiyo
          
    elif re.match('.+のすばやさ$', message.content):
      
         message_send = "```"
        
         worksheet = workbook.sheet1
         m = message.content[0:len(message.content)-5]
        
         if m == "":
            return
    
         try:
             cell = worksheet.find(m)
         except gspread.exceptions.CellNotFound:
             await message.channel.send("いないポケモン。何をしようとしているのですか。その行為に意味はありますか")
             return
        
         speed1 = worksheet.cell(cell.row,8).value
         speed1 = int(speed1)
         speed1MAX = int((speed1+52)*1.1)
         speed1MIN = int((speed1+5)*0.9)
    
         saisoku1 = str(speed1MAX)
         saiti1 = str(speed1MIN)
    
         text = "{}のすばやさは{}、最速実数値{}、最遅実数値{}"
         message_send = message_send + text.format(m,speed1,saisoku1,saiti1)
         message_send = message_send + "```"
          
         chiyo = " \n"+ "お嬢さまに感謝してください。"
         message_send = message_send + chiyo
                  
    await message.channel.send(message_send)
    
bot.run(token)
