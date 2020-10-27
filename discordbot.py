import discord
import os
import gspread

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
          
        await message.channel.send(message_send)
        
    

client.run(Token)
