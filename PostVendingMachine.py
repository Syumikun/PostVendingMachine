# -*- coding: utf-8 -*- #
# ProgramName: PostVendingMachine(PVM)
# FileVersion: 00.00.00.01(Beta0.01)
# Version:     0.0.1
# Create:      SyumikunProject


#<<<-- インポート -->>>#
import discord
import yaml
import json
import time
import sys
import os
import socket
import requests
from discord_slash import SlashCommand, SlashContext


#<<<-- 終了 -->>>#
def end():
    print('\n<<-- 10秒後にシステムを終了します。 -->>')
    time.sleep(10)
    sys.exit()


#<<<-- 初期変数 -->>>#
VERSION = '0.0.1'
FILE_VERSION = '00.00.00.01'


#<<<-- 起動処理 -->>>#
print('# -*- coding: utf-8 -*- #\nProgramName:PostVendingMachine(PVM)\nFileVersion:00.00.00.01(Beta0.01)\nVersion:0.0.1\nCreate:SyumikunProject\n')
print('[Info]システムファイル読み込み中')

# -- インターネット確認  -- #
ip = socket.gethostname()
ip = socket.gethostbyname(ip)
if ip == '127.0.0.1':
    print('[Error]インターネットに接続されていません。接続環境を再度ご確認の上再実行してみたください。')
    end()

# -- システムファイル読み込み -- #
# ファイル読み込み
if not os.path.isfile('setting.yml'):
    print('[Error]設定ファイル(setting.yml)がありません。\n作成します')
    setting_file_url='https://syumikun.github.io/pvm/setting.yml'
    setting_file_name='setting.yml'
    setting_file_data = requests.get(setting_file_url).content
    with open(setting_file_name ,mode='wb') as f:
        f.write(setting_file_data)
    print('[Info]設定ファイル(setting.yml)を作成しました。設定をお願いします。')
    end()
else:
    print('[Info]設定ファイルを認識しました。')
with open('setting.yml', 'r', encoding='utf-8') as yml:
    setting_file = yaml.full_load(yml)
    yml.close
# 利用規約確認
if setting_file['consent'] != 'RoadRoller':
    print('[Error]利用規約に同意していません。"setting.yml"の下の方を確認してください。')
    end()
else:
    print('[Info]利用規約の同意を確認。')
# オーナー認証
OWNER = setting_file['OWNER']
if OWNER == None or OWNER == 'DEFAULT':
    print('[Error]OWNERが正しく設定されていません。"setting.yml"をご確認ください。又分からない場合は公式Wikiをご利用ください。')
    end()
else:
    print('[Info]OWNERの認証に成功。')
# TOKEN取得
TOKEN = setting_file['TOKEN']
if TOKEN == None or TOKEN == 'DEFAULT':
    print('[Error]TOKENが正しく設定されていません。"setting.yml"をご確認ください。又分からない場合は公式Wikiをご利用ください。')
    end()
else:
    print('[Info]TOKENの認証に成功。')
# その他の設定確認
VERSIONUP = setting_file['VERSIONUP']
if VERSIONUP != True and VERSIONUP != False:
    print('[Error]VERSIONUPが正しく設定されていません。"setting.yml"をご確認ください。又分からない場合は公式Wikiをご利用ください。')
    end()
BOTSTART = setting_file['BOTSTART']
if BOTSTART != True and BOTSTART != False:
    print('[Error]BOTSTARTが正しく設定されていません。"setting.yml"をご確認ください。又分からない場合は公式Wikiをご利用ください。')
    end()
USEROLL = setting_file['USEROLL']
if USEROLL != True and USEROLL != False:
    print('[Error]USEROLLが正しく設定されていません。"setting.yml"をご確認ください。又分からない場合は公式Wikiをご利用ください。')
    end()
MODE = setting_file['MODE']
if MODE != 'ONL' and MODE != 'DW' and MODE != 'TL' and MODE != 'OF':
    print('[Error]MODEが正しく設定されていません。"setting.yml"をご確認ください。又分からない場合は公式Wikiをご利用ください。')
    end()
PLAY = setting_file['PLAY']
if PLAY == None or PLAY == 'DEFAULT':
    PLAY = '制作:SyumikunProject'
NAME = setting_file['NAME']
if NAME == None or NAME == 'DEFAULT':
    NAME = 'Copyright(C)2022 SyumikunProject'
ICON = setting_file['ICON']
if ICON == None or ICON == 'DEFAULT':
    ICON = 'https://syumikun.github.io/icon.png'
# ロール設定
print('[Info]ロール設定取得中')
roll_number = int(setting_file['data']['use'])
if roll_number == 0:
    print('[Error]付与するロールの設定が正しく設定されていません。"setting.yml"をご確認ください。又分からない場合は公式Wikiをご利用ください。')
roll_message_id = []
roll_stamp = []
roll_give_roll = []
while roll_number != 0:
    roll_message_id.append(setting_file['data'][roll_number]['message_id'])
    roll_stamp.append(setting_file['data'][roll_number]['message_stamp'])
    roll_give_roll.append(setting_file['data'][roll_number]['roll_id'])
    roll_number = roll_number - 1
roll_message_id_s = len(roll_message_id)
print('[Info]設定ファイルの読み込みに成功しました。')

# -- アップデート確認 -- #
# 最新バージョン取得
update_session = requests.Session()
update_version = update_session.get('https://syumikun.github.io/pvm/version.json')
UPDATE_VERSION = json.loads(update_version.text)['version']
coercion = json.loads(update_version.text)['coercion']
# バージョンの差を確認
version_ha = False
if VERSION != UPDATE_VERSION:
    print('[Info]アップデートがあります。')
    if VERSIONUP == True or coercion == True:
        version_ha = True

# -- Botスタート -- #
print('[Info]DiscordBotを起動します。\n')
# インターネット接続確認
ip = socket.gethostname()
ip = socket.gethostbyname(ip)
if ip == '127.0.0.1':
    print('[Warning]インターネットに接続されていません。接続環境を再度ご確認の上再実行してみたください。')
    end()
# Discordの変数
intents = discord.Intents.default()
intents.members = True
bot = discord.Client(intents=discord.Intents.all())
slash_client = SlashCommand(bot, sync_commands=True)
# 起動時
@bot.event
async def on_ready():
    BOTNAME = bot.user
    BOTID = bot.user.id
    # ステータスの設定
    if MODE == 'ONL':
        game = discord.Game(PLAY)
        await bot.change_presence(status=discord.Status.online, activity=game)
        print('[Info]オンラインモードで起動中')
    # 初期設定 
    elif MODE == 'DW':
        game = discord.Game(PLAY)
        await bot.change_presence(status=discord.Status.idle, activity=game)
        print('[Info]退席中モードで起動中')
    # 開発モード
    elif MODE == 'TL':
        game = discord.Game(PLAY)
        await bot.change_presence(status=discord.Status.dnd, activity=game)
        print('[Info]取り込み中モードで起動中')
    # オフライン
    elif MODE == 'OF':
        await bot.change_presence(status=discord.Status.offline)
        print('[Info]オフラインモードで起動中')
    # DM起動お知らせ
    if BOTSTART:
        user=bot.get_user(OWNER)
        embed = discord.Embed(title='< Bot起動通知 >',description=f'DiscordBot(PostVendingMachine)が起動したことをお知らせします。', color=0XFFFFE0)
        embed.add_field(name='起動したBOTの名前',value=f'```{BOTNAME}```')
        embed.add_field(name='起動したBOTのID',value=f'```{BOTID}```')
        embed.set_footer(text=NAME,icon_url=ICON)
        await user.send(embed=embed)
    # 新しいバージョンがあったら通知
    if version_ha:
        # 強制アプデか確認
        if coercion == True:
            # 強制アップデートの詳細取得
            UPDATE_TITLE = json.loads(update_version.text)['news']['title']
            UPDATE_EXPLANATION = json.loads(update_version.text)['news']['explanation']
            UPDATE_URL = json.loads(update_version.text)['news']['version_url']
            user=bot.get_user(OWNER)
            embed = discord.Embed(title='< 新しいバージョンが出ました >',description=f'このアップデートは強制アップデートです。詳しくは上のタイトルをクリックしてください。', url=UPDATE_URL, color=0XFFFFE0)
            embed.add_field(name='現在のバージョン',value=f'```{VERSION}```')
            embed.add_field(name='新しいバージョン',value=f'```{UPDATE_VERSION}```')
            embed.add_field(name='アップデートのタイトル',value=f'```{UPDATE_TITLE}```')
            embed.add_field(name='アップデートの詳細',value=f'```{UPDATE_EXPLANATION}```')
            embed.set_footer(text=NAME,icon_url=ICON)
            await user.send(embed=embed)
        else:
            # アップデートの詳細取得
            UPDATE_TITLE = json.loads(update_version.text)['news']['title']
            UPDATE_EXPLANATION = json.loads(update_version.text)['news']['explanation']
            UPDATE_URL = json.loads(update_version.text)['news']['version_url']
            user=bot.get_user(OWNER)
            embed = discord.Embed(title='< 新しいバージョンが出ました >',description=f'上のタイトルをクリックすると詳細ページへと飛びます。', url=UPDATE_URL, color=0XFFFFE0)
            embed.add_field(name='現在のバージョン',value=f'```{VERSION}```')
            embed.add_field(name='新しいバージョン',value=f'```{UPDATE_VERSION}```')
            embed.add_field(name='アップデートのタイトル',value=f'```{UPDATE_TITLE}```')
            embed.add_field(name='アップデートの詳細',value=f'```{UPDATE_EXPLANATION}```')
            embed.set_footer(text=NAME,icon_url=ICON)
            await user.send(embed=embed)

# 起動をお知らせ
print('\n<< -- BOT起動完了 -- >>\n')


#<<<-- ロール付与機能 -->>>#
# ロール付与
@bot.event
async def on_raw_reaction_add(data):
    roll_message_id_s2 = int(roll_message_id_s)
    while roll_message_id_s2 != 0:
        if data.message_id == int(roll_message_id[roll_message_id_s2-1]):
            guild_id = data.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)
            if data.emoji.name == roll_stamp[roll_message_id_s2-1]:
                role = guild.get_role(int(roll_give_roll[roll_message_id_s2-1]))
                await data.member.add_roles(role)
                # USEROLLがTrueだったら管理者に通知
                if USEROLL:
                    user=bot.get_user(OWNER)
                    embed = discord.Embed(title='< ロールを付与しました >',description=f'ユーザーにロールを付与した事をお知らせします。', color=0X90EE90)
                    embed.add_field(name='付与した人のName',value=f'```{data.member.name}```')
                    embed.add_field(name='付与した人のID',value=f'```{data.user_id}```')
                    embed.add_field(name='付与したロールID',value=f'```{str(roll_give_roll[roll_message_id_s2-1])}```')
                    embed.set_footer(text=NAME,icon_url=ICON)
                    await user.send(embed=embed)
        roll_message_id_s2 = roll_message_id_s2 - 1
# ロール削除
@bot.event
async def on_raw_reaction_remove(data):
    roll_message_id_s2 = int(roll_message_id_s)
    while roll_message_id_s2 != 0:
        if data.message_id == int(roll_message_id[roll_message_id_s2-1]):
            guild_id = data.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)
            if data.emoji.name == roll_stamp[roll_message_id_s2-1]:
                role = guild.get_role(int(roll_give_roll[roll_message_id_s2-1]))
                member = guild.get_member(data.user_id)
                await member.remove_roles(role)
                # USEROLLがTrueだったら管理者に通知
                if USEROLL:
                    user=bot.get_user(OWNER)
                    embed = discord.Embed(title='< ロールを解除しました >',description=f'ユーザーのロールを剥奪した事をお知らせします。', color=0XCBC0FF)
                    embed.add_field(name='剥奪した人のID',value=f'```{data.user_id}```')
                    embed.add_field(name='剥奪したロールID',value=f'```{str(roll_give_roll[roll_message_id_s2-1])}```')
                    embed.set_footer(text=NAME,icon_url=ICON)
                    await user.send(embed=embed)
        roll_message_id_s2 = roll_message_id_s2 - 1


#<<<-- 繰り返し処理 -->>>#
bot.run(TOKEN)


# Copyright (C) 2022 SyumikunProject / Syumikun. All Rights Reserved.