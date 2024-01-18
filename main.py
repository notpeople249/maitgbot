#!/usr/bin/python
# -*- coding: utf-8 -*-

import asyncio
import os
from datetime import datetime
from pytz import timezone
from dotenv import load_dotenv
from pyrogram import Client, idle
from src.plugins.public import set_command, declare_online

load_dotenv()

API_ID = os.getenv('APP_ID')
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BTOKEN')

Plugins = dict(
    root="src",
    include = [
        "plugins.maimaidx",
        "plugins.public"
    ]
)

app = Client("maitgbot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, system_version="Mai-TgBot", plugins=Plugins)

tz_SG = timezone('Asia/Shanghai')
SG_time = datetime.now(tz_SG)


app.start()
print('机器人已启动!\n时间于：' + SG_time.strftime('%Y-%m-%d_%H:%M:%S '))
loop = asyncio.get_event_loop()
loop.run_until_complete(set_command(app))
loop.run_until_complete(declare_online(app))
idle()
app.stop()
SG_time = datetime.now(tz_SG)
print('机器人已停止!\n时间于：' + SG_time.strftime('%Y-%m-%d_%H:%M:%S '))
