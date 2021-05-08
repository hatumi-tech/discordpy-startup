# -*- coding: utf-8 -*-
import discord
import os
import gspread
import math
import random
import redis

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

Token = os.environ['DISCORD_BOT_TOKEN']
client = discord.Client()

def connect():
    return redis.from_url(
        url=os.environ.get('REDIS_URL'), # 環境変数にあるURLを渡す
        decode_responses=True, # 日本語の文字化け対策のため必須
    )
  
>>> import r
>>> conn = r.connect()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/ping'):
        await message.channel.send('ぽん！')
    
    if message.content == '教えてチヨチャン':
        embed = discord.Embed(title="チヨチャンについて", description="チヨチャンにものを聞くときはこうするのです。",color=0xff0000)
        embed.add_field(name="教えてチヨチャン", value="このヘルプを表示します。",inline=False)
        embed.add_field(name="（ポケモン名）の図鑑", value="ポケモンのタイプ、種族値、特性を表示します。",inline=False)
        embed.add_field(name="（ポケモン名）の弱点", value="技を受ける際のタイプ別のダメージ倍率を表示します。",inline=False)
        embed.add_field(name="（ポケモン名）の耐久調整", value="調整先のポケモンとわざを指定すると予想ダメージを計算します。",inline=False)
        embed.add_field(name="（ポケモン名）のすばやさ調整", value="調整先のポケモンを抜くための努力値を計算します。",inline=False)
        embed.add_field(name="（1～10）頭の馬配って", value="指定された数の馬を配ります。",inline=False)
        await message.channel.send(embed=embed)
        
    if message.content.endswith('頭の馬配って'):
        
        for i in range(1, 21):
           r.rpush('key', 'value-%d' % i)
        
        result = r.lrange('key', 0, 10)
        
        for r in result:
           print(r)     
            
    if message.content.endswith('の図鑑'):
      
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
        
        type1 = worksheet.cell(cell.row,3).value
        type2 = worksheet.cell(cell.row,4).value
        hp1 = worksheet.cell(cell.row,5).value
        atk1 = worksheet.cell(cell.row,6).value
        def1 = worksheet.cell(cell.row,7).value
        spatk1 = worksheet.cell(cell.row,8).value
        spdef1 = worksheet.cell(cell.row,9).value
        speed1 = worksheet.cell(cell.row,10).value
        all1 = worksheet.cell(cell.row,11).value
        
        tetsuurl = "https://yakkun.com/swsh/zukan/"
        id1 = worksheet.cell(cell.row,15).value
        id1 = str(id1)
          
        yumetokusei = ""
        
        tokusei1 = worksheet.cell(cell.row,12).value
        tokusei2 = worksheet.cell(cell.row,13).value
        tokusei3 = worksheet.cell(cell.row,14).value
    
        tokusei1 = str(tokusei1)
        tokusei2 = str(tokusei2)
        tokusei3 = str(tokusei3)
    
        worksheet = workbook.get_worksheet(1)
    
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
        
        if tokusei2 != "" and tokusei3 == "":
            tokuseimessage = "とくせいは" + " \n" + tokusei1 + "：" + tokusei1info +  " \n" + tokusei2 + "：" + tokusei2info +  " \n"+ "夢特性は" + yumetokusei
        
        if tokusei2 == "" and tokusei3 == "":
            tokuseimessage = "とくせいは" + " \n" + tokusei1 + "：" + tokusei1info +  " \n" + "夢特性は" + yumetokusei
            
        text = "{}はタイプ{}、{}" +  " \n" + "H{}-A{}-B{}-C{}-D{}-S{}-ALL{}" +  " \n"
        message_send = text.format(m,type1,type2,hp1,atk1,def1,spatk1,spdef1,speed1,all1) + tokuseimessage + " \n"  + tetsuurl + id1
        message_send = message_send + "```"
          
        await message.channel.send(message_send)
        
    if message.content.endswith('の弱点'):
      
         message_send = ""
      
         worksheet = workbook.sheet1
         m = message.content[0:len(message.content)-3]
        
         if m == "":
            return
    
         try:
             cell = worksheet.find(m)
         except gspread.exceptions.CellNotFound:
             await message.channel.send("いないポケモン。何をしようとしているのですか。その行為に意味はありますか")
             return
        
         type1 = worksheet.cell(cell.row,3).value
         type2 = worksheet.cell(cell.row,4).value
         
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
        
         tokusei1 = worksheet.cell(cell.row,12).value
         tokusei2 = worksheet.cell(cell.row,13).value
         tokusei3 = worksheet.cell(cell.row,14).value
    
         tokusei1 = str(tokusei1)
         tokusei2 = str(tokusei2)
         tokusei3 = str(tokusei3)
     
         if "*" in tokusei2:
             tokusei2 = tokusei2[1:]
         else:
             pass
    
         if "*" in tokusei3:
             tokusei3 = tokusei3[1:]
         else:
             pass
        
         mukoutext = ""
        
         if tokusei1 == "かんそうはだ":
             mukoutext = (f"特性{tokusei1}の場合、みず無効。最大HPの1/4回復。")
            
         elif tokusei1 == "そうしょく":
             mukoutext = (f"特性{tokusei1}の場合、くさ無効。攻撃ランク+1。")
            
         elif tokusei1 == "ちくでん":
             mukoutext = (f"特性{tokusei1}の場合、でんき無効。最大HPの1/4回復。")
            
         elif tokusei1 == "ちょすい":
             mukoutext = (f"特性{tokusei1}の場合、みず無効。最大HPの1/4回復。")
            
         elif tokusei1 == "でんきエンジン":
             mukoutext = (f"特性{tokusei1}の場合、でんき無効。素早さランク+1。")
            
         elif tokusei1 == "ひらいしん":
             mukoutext = (f"特性{tokusei1}の場合、でんき無効。特攻ランク+1。")
            
         elif tokusei1 == "もらいび":
             mukoutext = (f"特性{tokusei1}の場合、ほのお無効。攻撃・特攻1.5倍。")
            
         elif tokusei1 == "よびみず":
             mukoutext = (f"特性{tokusei1}の場合、みず無効。特攻ランク+1。")
            
         if tokusei2 == "かんそうはだ":
             mukoutext = mukoutext + (f"特性{tokusei2}の場合、みず無効。最大HPの1/4回復。")
            
         elif tokusei2 == "そうしょく":
             mukoutext = mukoutext + (f"特性{tokusei2}の場合、くさ無効。攻撃ランク+1。")
            
         elif tokusei2 == "ちくでん":
             mukoutext = mukoutext + (f"特性{tokusei2}の場合、でんき無効。最大HPの1/4回復。")
            
         elif tokusei2 == "ちょすい":
             mukoutext = mukoutext + (f"特性{tokusei2}の場合、みず無効。最大HPの1/4回復。")
            
         elif tokusei2 == "でんきエンジン":
             mukoutext = mukoutext + (f"特性{tokusei2}の場合、でんき無効。素早さランク+1。")
            
         elif tokusei2 == "ひらいしん":
             mukoutext = mukoutext + (f"特性{tokusei2}の場合、でんき無効。特攻ランク+1。")
            
         elif tokusei2 == "もらいび":
             mukoutext = mukoutext + (f"特性{tokusei2}の場合、ほのお無効。攻撃・特攻1.5倍。")
            
         elif tokusei2 == "よびみず":
             mukoutext = mukoutext + (f"特性{tokusei2}の場合、みず無効。特攻ランク+1。")
        
         if tokusei3 == "かんそうはだ":
             mukoutext = mukoutext + (f"特性{tokusei3}の場合、みず無効。最大HPの1/4回復。")
            
         elif tokusei3 == "そうしょく":
             mukoutext = mukoutext + (f"特性{tokusei3}の場合、くさ無効。攻撃ランク+1。")
            
         elif tokusei3 == "ちくでん":
             mukoutext = mukoutext + (f"特性{tokusei3}の場合、でんき無効。最大HPの1/4回復。")
            
         elif tokusei3 == "ちょすい":
             mukoutext = mukoutext + (f"特性{tokusei3}の場合、みず無効。最大HPの1/4回復。")
            
         elif tokusei3 == "でんきエンジン":
             mukoutext = mukoutext + (f"特性{tokusei3}の場合、でんき無効。素早さランク+1。")
            
         elif tokusei3 == "ひらいしん":
             mukoutext = mukoutext + (f"特性{tokusei3}の場合、でんき無効。特攻ランク+1。")
            
         elif tokusei3 == "もらいび":
             mukoutext = mukoutext + (f"特性{tokusei3}の場合、ほのお無効。攻撃・特攻1.5倍。")
            
         elif tokusei3 == "よびみず":
             mukoutext = mukoutext + (f"特性{tokusei3}の場合、みず無効。特攻ランク+1。")
        
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
         message_send = message_send + " \n" + mukoutext
          
         chiyo = " \n"+ "お嬢さまに感謝してください。"
         message_send = message_send + chiyo
          
         await message.channel.send(message_send)
        
    if message.content.endswith('のすばやさ調整'):
      
         worksheet = workbook.sheet1
         m = message.content[0:len(message.content)-7]
        
         if m == "":
            return
    
         try:
             cell = worksheet.find(m)
         except gspread.exceptions.CellNotFound:
             await message.channel.send("いないポケモン。何をしようとしているのですか。その行為に意味はありますか")
             return
         
         speed1base = worksheet.cell(cell.row,10).value
         speed1base = int(speed1base)
         
         await message.channel.send("調整先のポケモンを送信してください。")
        
         try:
             m2 = await client.wait_for('message', timeout=60.0,check=None)
         except asyncio.TimeoutError:
             await message.channel.send("時間内にお答えいただきたかったですね。")
             return
              
         m2 = m2.content
    
         if m2 == "":
             await message.channel.send("何をしようとしているのですか。その行為に意味はありますか")
             return
    
         try:
             cell = worksheet.find(m2)
         except gspread.exceptions.CellNotFound:
             await message.channel.send("いないポケモン。何をしようとしているのですか。その行為に意味はありますか")
             return
            
         speed2base = worksheet.cell(cell.row,10).value
         speed2base = int(speed2base)
       
         speedeffort = 0
         nukeru = 0
        
         speed1 = int((int((speed1base*2+31+int(speedeffort/4))*50/100)+5)*1.1)
         speed1MAX = int((speed1base+52)*1.1)
         speed2MAX = int((speed2base+52)*1.1)
         speed2JUN = speed2base+52
         speed2MU = speed2base+20
         speed2saiti = int(int(speed2base+5)*0.9)
          
         while True:
             speed1 = int((int((speed1base*2+31+int(speedeffort/4))*50/100)+5)*1.1)
        
             if speed1 >= speed2MAX+1:
                break
             
             if speedeffort < 252:
                speedeffort = speedeffort + 4
             else:
                 nukeru = 1
                 break
                  
         if nukeru == 0:
             text1 = (f"最速{m}のすばやさが最速の{m2}を抜くのは、\n努力値を{speedeffort}振った時です。実数値は{speed1}")
         else:
             text1 = (f"最速{m}のすばやさは最速の{m2}を抜くことができません。\n最速{m}の実数値は{speed1MAX}、最速{m2}の実数値は{speed2MAX}です。")
         
         nukeru = 0
         speedeffort = 0
                  
         while True:
             speed1 = int((int((speed1base*2+31+int(speedeffort/4))*50/100)+5)*1.1)
        
             if speed1 >= speed2JUN+1:
                break
             
             if speedeffort < 252:
                speedeffort = speedeffort + 4
             else:
                 nukeru = 1
                 break
                  
         if nukeru == 0:
             text2 = (f"最速{m}のすばやさが準速の{m2}を抜くのは、\n努力値を{speedeffort}振った時です。実数値は{speed1}")
         else:
             text2 = (f"最速{m}のすばやさは準速の{m2}を抜くことができません。\n最速{m}の実数値は{speed1MAX}、準速{m2}の実数値は{speed2JUN}です。")
            
         nukeru = 0
         speedeffort = 0
                  
         while True:
             speed1 = int((int((speed1base*2+31+int(speedeffort/4))*50/100)+5)*1.1)
        
             if speed1 >= speed2MU+1:
                break
             
             if speedeffort < 252:
                speedeffort = speedeffort + 4
             else:
                 nukeru = 1
                 break
                  
         if nukeru == 0:
             text3 = (f"最速{m}のすばやさが無振の{m2}を抜くのは、\n努力値を{speedeffort}振った時です。実数値は{speed1}")
         else:
             text3 = (f"最速{m}のすばやさは無振の{m2}を抜くことができません。\n最速{m}の実数値は{speed1MAX}、無振{m2}の実数値は{speed2MU}です。")
         
         nukeru = 0
         speedeffort = 0
                 
         while True:
             speed1 = int((int((speed1base*2+31+int(speedeffort/4))*50/100)+5)*1.1)
        
             if speed1 >= speed2saiti+1:
                break
             
             if speedeffort < 252:
                speedeffort = speedeffort + 4
             else:
                 nukeru = 1
                 break
                  
         if nukeru == 0:
             text4 = (f"最速{m}のすばやさが最遅の{m2}を抜くのは、\n努力値を{speedeffort}振った時です。実数値は{speed1}")
         else:
             text4 = (f"最速{m}のすばやさは最遅の{m2}を抜くことができません。\n最速{m}の実数値は{speed1MAX}、最遅{m2}の実数値は{speed2saiti}です。")
         
         message_send = "```"
         message_send = message_send + text1 + " \n" + text2 + " \n" + text3 + " \n" + text4
         message_send = message_send + "```"
            
         chiyo = " \n"+ "お嬢さまに感謝してください。"
         message_send = message_send + chiyo
                  
         await message.channel.send(message_send)
        
    if message.content.endswith('の耐久調整'):

         worksheet = workbook.sheet1
         m = message.content[0:len(message.content)-5]
        
         if m == "":
            return
    
         try:
             cell = worksheet.find(m)
         except gspread.exceptions.CellNotFound:
             await message.channel.send("いないポケモン。何をしようとしているのですか。その行為に意味はありますか")
             return
        
         type1 = worksheet.cell(cell.row,3).value
         type2 = worksheet.cell(cell.row,4).value
         myhpbase = worksheet.cell(cell.row,5).value
         mydefbase = worksheet.cell(cell.row,7).value
         myspdefbase = worksheet.cell(cell.row,9).value
         
         await message.channel.send("調整先のポケモンを送信してください。")
        
         try:
             m2 = await client.wait_for('message', timeout=60.0,check=None)
         except asyncio.TimeoutError:
             await message.channel.send("時間内にお答えいただきたかったですね。")
             return
              
         m2 = m2.content
    
         if m2 == "":
             await message.channel.send("何をしようとしているのですか。その行為に意味はありますか")
             return
    
         try:
             cell = worksheet.find(m2)
         except gspread.exceptions.CellNotFound:
             await message.channel.send("いないポケモン。何をしようとしているのですか。その行為に意味はありますか")
             return
         
         enemytype1 = worksheet.cell(cell.row,3).value
         enemytype2 = worksheet.cell(cell.row,4).value
         enemyatkbase = worksheet.cell(cell.row,6).value
         enemyspatkbase = worksheet.cell(cell.row,8).value
        
         myhpbase = int(myhpbase)
         mydefbase = int(mydefbase)
         myspdefbase = int(myspdefbase)
         enemyatkbase = int(enemyatkbase)
         enemyspatkbase = int(enemyspatkbase)
         
         enemyatkkyoku = int((enemyatkbase + 52)*1.1)
         enemyspatkkyoku = int((enemyspatkbase + 52)*1.1)
            
         mydefkyoku = int((mydefbase + 52)*1.1)
         myspdefkyoku = int((myspdefbase + 52)*1.1)
            
         mydefjun = int(mydefbase + 52)
         myspdefjun = int(myspdefbase + 52)
            
         mydefmu = int(mydefbase + 20)
         myspdefmu = int(myspdefbase + 20)
         
         ###わざについて###
         
         await message.channel.send("調整先のポケモンが使うわざ（耐えたいわざ）を送信してください。")
        
         try:
             m3 = await client.wait_for('message', timeout=60.0,check=None)
         except asyncio.TimeoutError:
             await message.channel.send("時間内にお答えいただきたかったですね。")
             return
              
         m3 = m3.content
    
         if m3 == "":
             await message.channel.send("何をしようとしているのですか。その行為に意味はありますか")
             return
         
         worksheet = workbook.get_worksheet(2)
         
         try:
             cell = worksheet.find(m3)
         except gspread.exceptions.CellNotFound:
             await message.channel.send("ないわざ。何をしようとしているのですか。その行為に意味はありますか")
             return
         
         wazaname = m3
         wazatype = worksheet.cell(cell.row,2).value
         wazapower = worksheet.cell(cell.row,3).value
         wazabunrui = worksheet.cell(cell.row,6).value
        
         wazapower = int(wazapower)
         
         if wazabunrui == "物理":
             attack = enemyatkkyoku
             defence = mydefkyoku
                
         if wazabunrui == "特殊":
             attack = enemyspatkkyoku
             defence = myspdefkyoku
                
         if wazabunrui == "変化":
             await message.channel.send('送信されたのは変化わざです。')
             return
            
         itti = 1.0
            
         if enemytype1 == wazatype:
             itti = 1.5
         
         if enemytype2 == wazatype:
             itti = 1.5
              
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
          
         if wazatype == "ノーマル":
             typebairitu = normal
         if wazatype == "ほのお":
             typebairitu = fire
         if wazatype == "みず":
             typebairitu = water
         if wazatype == "くさ":
             typebairitu = grass
         if wazatype == "でんき":
             typebairitu = electric
         if wazatype == "こおり":
             typebairitu = ice
         if wazatype == "かくとう":
             typebairitu = fighting
         if wazatype == "どく":
             typebairitu = poison
         if wazatype == "じめん":
             typebairitu = ground
         if wazatype == "ひこう":
             typebairitu = flying
         if wazatype == "エスパー":
             typebairitu = psychic
         if wazatype == "むし":
             typebairitu = bug
         if wazatype == "いわ":
             typebairitu = rock
         if wazatype == "ゴースト":
             typebairitu = ghost
         if wazatype == "ドラゴン":
             typebairitu = dragon
         if wazatype == "あく":
             typebairitu = dark
         if wazatype == "はがね":
             typebairitu = steel
         if wazatype == "フェアリー":
             typebairitu = fairy
        
         damageMIN = int(int(int(22 * wazapower * attack / defence) / 50 + 2)*0.85)
         damageMAX = int(int(22 * wazapower * attack / defence) / 50 + 2)
          
         damageMIN = int(damageMIN * itti * typebairitu)
         damageMAX = int(damageMAX * itti * typebairitu)
        
         message_send = (f"{wazabunrui}特化の{m2}が{wazaname}で性格補正あり特化の{m}に与える予想ダメージは{damageMIN}～{damageMAX}です。")
          
         if wazabunrui == "物理":
             attack = enemyatkkyoku
             defence = mydefjun
                
         if wazabunrui == "特殊":
             attack = enemyspatkkyoku
             defence = myspdefjun
          
         damageMIN = int(int(int(22 * wazapower * attack / defence) / 50 + 2)*0.85)
         damageMAX = int(int(22 * wazapower * attack / defence) / 50 + 2)
          
         damageMIN = int(damageMIN * itti * typebairitu)
         damageMAX = int(damageMAX * itti * typebairitu)
        
         message_send = message_send + "\n" + (f"{wazabunrui}特化の{m2}が{wazaname}で性格補正なし252振りの{m}に与える予想ダメージは{damageMIN}～{damageMAX}です。")
          
         if wazabunrui == "物理":
             attack = enemyatkkyoku
             defence = mydefmu
                
         if wazabunrui == "特殊":
             attack = enemyspatkkyoku
             defence = myspdefmu
          
         damageMIN = int(int(int(22 * wazapower * attack / defence) / 50 + 2)*0.85)
         damageMAX = int(int(22 * wazapower * attack / defence) / 50 + 2)
          
         damageMIN = int(damageMIN * itti * typebairitu)
         damageMAX = int(damageMAX * itti * typebairitu)
        
         message_send = message_send + "\n" + (f"{wazabunrui}特化の{m2}が{wazaname}で無振の{m}に与える予想ダメージは{damageMIN}～{damageMAX}です。")
          
         myhpkyoku = myhpbase + 107
         myhpmu = myhpbase + 75
          
         message_send = message_send + "\n" + (f"{m}のHPは252振りで{myhpkyoku}、無振りで{myhpmu}です。")
        
         await message.channel.send(message_send)
    

client.run(Token)
