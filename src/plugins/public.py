
from pyrogram import Client, filters
from pyrogram.types import BotCommand


@Client.on_message(filters.command('help')
                    & filters.text)
async def help(Client, Message):
    help_str = '''可用命令如下：
<pre>...maimai...什么</pre> 随机一首歌
<pre>随个[dx/标准][绿黄红紫白](难度)</pre> 随机一首指定条件的乐曲
<pre>查歌 (乐曲标题的一部分)</pre> 查询符合条件的乐曲
<pre>[绿黄红紫白]id(歌曲编号)</pre> 查询乐曲信息或谱面信息
/inner_level (定数) 查询定数对应的乐曲
/inner_level (定数下限) (定数上限)
/today_mai 查看今天的舞萌运势
/pointer (难度+歌曲id) (分数线) 详情请输入“/pointer 帮助”查看
/b40 (查询账号的用户名) 根据查分器数据生成你的Best 40数据图
/b50 (查询账号的用户名) 根据查分器数据生成你的Best 50数据图
/help 显示此说明
/author 发现问题？请加入群向作者反馈'''
    await Message.reply(help_str)


@Client.on_message(filters.command('start')
                    & filters.text)
async def start(Client, Message):
    user = Message.from_user
    me = await Client.get_users("me")
    text = "你好 " + user.first_name + " 欢迎使用 " + me.first_name + '\n请发送 /help 以获取我的完整指令集\n使用 b40/b50 功能前请先前往<a href="https://www.diving-fish.com/maimaidx/prober/">舞萌DX查分器</a>绑定账号'
    await Message.reply(text, disable_web_page_preview=True)


@Client.on_message(filters.command('version')
                    & filters.text)
async def version(Client, Message):
    Version_Code = 'v1.2'
    text = 'MaiMai DX - Diving Fish Checker Bot\n' + Version_Code + '\n<a href="https://github.com/Diving-Fish/mai-bot">Original QQ bot Repo</a>\n<a href="https://github.com/notpeople249/maitgbot">Telegram bot Repo</a>'
    await Message.reply(text, quote=True, disable_web_page_preview=True)


async def set_command(Client):
    set_com = [BotCommand("today_mai", "查看今天的舞萌运势"),
            BotCommand("inner_level", "(定数) / [(定数下限) (定数上限)] 查询定数对应的乐曲"),
            BotCommand("pointer", "(难度+歌曲id) (分数线) 详情请输入“/pointer 帮助”查看"),
            BotCommand("b40", "(查询账号的用户名) 生成你的Best 40数据图"),
            BotCommand("b50", "(查询账号的用户名) 生成你的Best 50数据图"),
            BotCommand("help", "显示完整的指令说明")]
    await Client.set_bot_commands(set_com)


@Client.on_message(filters.command('author')
                    & filters.text)
async def author(Client, Message):
    text = '如有发现错误，请联系开发者进行校对与修改\n<a href="https://t.me/xiaopoqun">@xiaopoqun</a>'
    await Message.reply(text, quote=True, disable_web_page_preview=True)
