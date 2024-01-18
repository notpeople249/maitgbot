import os
import traceback
from pyrogram import Client, filters
from pyrogram.types import BotCommand
from pyrogram.enums.parse_mode import ParseMode
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
Record_ID = os.getenv('Record_Channel_ID')

async def fullname(user):  # get user's fullname
    if user.last_name != None: # if user have last name
        u_fullname = ' '.join((user.first_name, user.last_name))
        return u_fullname
    elif user.last_name == None: # if user don't have last name
        u_fullname = user.first_name
        return u_fullname
    else:
        return user.first_name # accept first name first


@Client.on_message(filters.command('help')
                    & filters.text)
async def help(Client, Message):
    try:
        help_str = '''<b>可用命令如下：</b>
<code>...maimai...什么</code> 随机一首歌
<code>随个[dx/标准][绿黄红紫白](难度)</code> 随机一首指定条件的乐曲
<code>查歌 (乐曲标题的一部分)</code> 查询符合条件的乐曲
<code>[绿黄红紫白]id(歌曲编号)</code> 查询乐曲信息或谱面信息
/inner_level (定数) 查询定数对应的乐曲
/inner_level (定数下限) (定数上限)
/today_mai 查看今天的舞萌运势
/pointer (难度+歌曲id) (分数线) 详情请输入“<code>/pointer 帮助</code>”查看
/b40 (查询账号的用户名) 根据查分器数据生成你的Best 40数据图
/b50 (查询账号的用户名) 根据查分器数据生成你的Best 50数据图

(<b>使用b40和b50功能需要先前往 <a href="https://www.diving-fish.com/maimaidx/prober/">舞萌DX查分器</a> 绑定账号</b>)
(机器人貌似会随机无反应，可通知开发者重启bot尝试解决。若急需查看个人数据也可前往 <a href="https://www.diving-fish.com/maimaidx/prober/">舞萌DX查分器</a> 官网查看。)
/help 显示此说明
/author 发现问题？请加入群向作者反馈
/update 机器人更新记录'''
        await Message.reply(help_str, quote=True, disable_web_page_preview=True, parse_mode=ParseMode.HTML)
    except:
        error = traceback.format_exc(limit=15)
        record = 'An error occurred when processing message:\n<code>' + Message.text + '</code>\nBy user: ' + await fullname(Message.from_user) + ' ( tg://user?id=' + str(Message.from_user.id) + ' )\nThe error des:\n' + str(error)
        await Client.send_message(int(Record_ID), record)
        await Message.reply('错误触发，请重新发送指令。若多次触发错误请发送 /author 通知作者。')


@Client.on_message(filters.command('start')
                    & filters.text)
async def start(Client, Message):
    try:
        user = Message.from_user
        me = await Client.get_users("me")
        text = "你好 " + user.first_name + " 欢迎使用 " + me.first_name + '\n请发送 /help 以获取我的完整指令集\n使用 b40/b50 功能前先请前往<a href="https://www.diving-fish.com/maimaidx/prober/">舞萌DX查分器</a>绑定账号'
        await Message.reply(text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    except:
        error = traceback.format_exc(limit=15)
        record = 'An error occurred when processing message:\n<code>' + Message.text + '</code>\nBy user: ' + await fullname(Message.from_user) + ' ( tg://user?id=' + str(Message.from_user.id) + ' )\nThe error des:\n' + str(error)
        await Client.send_message(int(Record_ID), record)
        await Message.reply('错误触发，请重新发送指令。若多次触发错误请发送 /author 通知作者。')


@Client.on_message(filters.command('version')
                    & filters.text)
async def version(Client, Message):
    try:
        Version_Code = 'v1.4.2'
        Last_Update = '18/1/2024'
        text = 'MaiMai DX - Diving Fish Checker Telegram Bot\n' + Version_Code + '\nLast update: ' + Last_Update + '\n<a href="https://github.com/Diving-Fish/mai-bot">Original QQ bot Repo</a>\n<a href="https://github.com/notpeople249/maitgbot">Telegram bot Repo</a>'
        await Message.reply(text, quote=True, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    except:
        error = traceback.format_exc(limit=15)
        record = 'An error occurred when processing message:\n<code>' + Message.text + '</code>\nBy user: ' + await fullname(Message.from_user) + ' ( tg://user?id=' + str(Message.from_user.id) + ' )\nThe error des:\n' + str(error)
        await Client.send_message(int(Record_ID), record)
        await Message.reply('错误触发，请重新发送指令。若多次触发错误请发送 /author 通知作者。')


@Client.on_message(filters.command('update')
                    & filters.text)
async def update(Client, Message):
    try:
        Version_Code = 'v1.4.2'
        text = 'Bot Current Version: ' + Version_Code + "\n28 Aug 2022 - Stable update\n01 Sep 2023 - Cover picture link update\n22 Oct 2023 - Unknown responding problem spotted, pls wait for update\n04 Jan 2024 - Verifying unresponsive problem, update error notifier, update to pyrogram 2.0.106\n06 Jan 2024 - Fix minor typo error and 'pointer' indicator, improve 'inner_level'"
        await Message.reply(text, quote=True)
    except:
        error = traceback.format_exc(limit=15)
        record = 'An error occurred when processing message:\n<code>' + Message.text + '</code>\nBy user: ' + await fullname(Message.from_user) + ' ( tg://user?id=' + str(Message.from_user.id) + ' )\nThe error des:\n' + str(error)
        await Client.send_message(int(Record_ID), record)
        await Message.reply('错误触发，请重新发送指令。若多次触发错误请发送 /author 通知作者。')

async def set_command(Client):
    try:
        set_com = [BotCommand("help", "显示完整的指令说明"),
                BotCommand("today_mai", "查看今天的舞萌运势"),
                BotCommand("inner_level", "(定数) / [(定数下限) (定数上限)] 查询定数对应的乐曲"),
                BotCommand("pointer", "(难度+歌曲id) (分数线) 详情请输入“/pointer 帮助”查看"),
                BotCommand("b40", "(查询账号的用户名) 生成你的Best 40数据图"),
                BotCommand("b50", "(查询账号的用户名) 生成你的Best 50数据图"),
                BotCommand("update", "机器人更新记录"),
                BotCommand("author", "联系开发者")]
        await Client.set_bot_commands(set_com)
    except:
        error = traceback.format_exc(limit=15)
        record = 'An error occurred when setting command during init\nThe error des:\n' + str(error)
        await Client.send_message(int(Record_ID), record)

async def declare_online(Client):
    me = await Client.get_me()
    text = "我苏醒了！@" + me.username
    await Client.send_message(int(Record_ID), text)


@Client.on_message(filters.command('author')
                    & filters.text)
async def author(Client, Message):
    try:
        text = '如有发现错误，请联系开发者进行校对与修改\n<a href="https://t.me/xiaopoqun">@xiaopoqun</a>'
        await Message.reply(text, quote=True, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    except:
        error = traceback.format_exc(limit=15)
        record = 'An error occurred when processing message:\n<code>' + Message.text + '</code>\nBy user: ' + await fullname(Message.from_user) + ' ( tg://user?id=' + str(Message.from_user.id) + ' )\nThe error des:\n' + str(error)
        await Client.send_message(int(Record_ID), record)
        await Message.reply('错误触发，请重新发送指令。若多次触发错误请发送 /author 通知作者。\nhttps://t.me/xiaopoqun')
