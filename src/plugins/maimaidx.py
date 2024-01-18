
import traceback
from pyrogram import Client, filters
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.errors import MessageTooLong
import re
from io import BytesIO

from src.libraries.tool import hash
from src.libraries.maimaidx_music import *
from src.libraries.image import text_to_image
from src.libraries.maimai_best_40 import generate
from src.libraries.maimai_best_50 import generate50
from src.plugins.public import Record_ID, fullname

def song_txt(music:Music):
    photo_id = get_cover_len5_id(music.id)
    id = music.id
    title = music.title
    level = '/ '.join(music.level)
    photo = "https://www.diving-fish.com/covers/" + photo_id + ".png"
    caption= id+". "+title + "\n" + level
    return photo, caption

def inner_level_q(ds1, ds2=None):
    result_set = []
    diff_label = ['Bas', 'Adv', 'Exp', 'Mst', 'ReM']
    if ds2 is not None:
        music_data = total_list.filter(ds=(ds1, ds2))
    else:
        music_data = total_list.filter(ds=(ds1))
    for music in sorted(music_data, key = lambda i: int(i['id'])):
        for i in music.diff:
            result_set.append((music['id'], music['title'],  music['ds'][i], diff_label[i], music['level'][i]))
    return result_set

wm_list = ['拼机', '推分', '越级', '下埋', '夜勤', '练底力', '练手法', '打旧框', '干饭', '抓绝赞', '收歌']


@Client.on_message(filters.command('inner_level')
                    & filters.text)
async def inner_level(Client, Message):
    try:
        argv = str(Message.text).strip().split(" ")
        if len(argv) > 3 or len(argv) == 1:
            await Message.reply("命令格式为\n/inner_level <定数>\n/inner_level <定数下限> <定数上限>")
            return
        if len(argv) == 2:
            result_set = inner_level_q(float(argv[1]))
        else:
            result_set = inner_level_q(float(argv[1]), float(argv[2]))
            if len(result_set) > 151:
                await Message.reply(f"结果过多（{len(result_set)} 条），请缩小搜索范围至150条以下。")
                return
        s = ""
        for elem in result_set:
            s += f"{elem[0]}.  {elem[1]} {elem[3]} {elem[4]}({elem[2]})\n"
        if len(s) > 4000:
            index = s[:4000].rfind('\n')
            s1 = s[:index]
            s2 = s[index+1:]
            await Message.reply("您所求定数的" + str(len(result_set)) + "首歌曲来啦～\n" + s1)
            await Message.reply(s2)
            return
        await Message.reply("您所求定数的" + str(len(result_set)) + "首歌曲来啦～\n" + s)
    except MessageTooLong as e:
        await Message.reply('结果过多，请缩小搜索范围。')
        record = 'An error occurred when processing message:\n<code>' + Message.text + '</code>\nBy user: ' + await fullname(Message.from_user) + ' ( tg://user?id=' + str(Message.from_user.id) + ' )\nThe error des:\n' + str(e)
        await Client.send_message(int(Record_ID), record)
    except:
        error = traceback.format_exc(limit=15)
        record = 'An error occurred when processing message:\n<code>' + Message.text + '</code>\nBy user: ' + await fullname(Message.from_user) + ' ( tg://user?id=' + str(Message.from_user.id) + ' )\nThe error des:\n' + str(error)
        await Client.send_message(int(Record_ID), record)
        await Message.reply('错误触发，请重新发送指令。若多次触发错误请发送 /author 通知作者。')


@Client.on_message(filters.regex(r"^随个(?:dx|sd|标准)?[绿黄红紫白]?[0-9]+\+?")
                    &filters.text)
async def spec_rand(Client, Message):
    try:
        regex = "随个((?:dx|sd|标准))?([绿黄红紫白]?)([0-9]+\+?)"
        res = re.match(regex, str(Message.text).lower())
        try:
            if res.groups()[0] == "dx":
                tp = ["DX"]
            elif res.groups()[0] == "sd" or res.groups()[0] == "标准":
                tp = ["SD"]
            else:
                tp = ["SD", "DX"]
            level = res.groups()[2]
            if res.groups()[1] == "":
                music_data = total_list.filter(level=level, type=tp)
            else:
                music_data = total_list.filter(level=level, diff=['绿黄红紫白'.index(res.groups()[1])], type=tp)
            if len(music_data) == 0:
                rand_result = "没有这样的乐曲哦。"
                await Message.reply(rand_result)
            else:
                photo, caption = song_txt(music_data.random())
                await Message.reply_photo(photo=photo, caption=caption)
        except Exception:
            await Message.reply("随机命令错误，请检查语法")
    except:
        error = traceback.format_exc(limit=15)
        record = 'An error occurred when processing message:\n<code>' + Message.text + '</code>\nBy user: ' + await fullname(Message.from_user) + ' ( tg://user?id=' + str(Message.from_user.id) + ' )\nThe error des:\n' + str(error)
        await Client.send_message(int(Record_ID), record)
        await Message.reply('错误触发，请重新发送指令。若多次触发错误请发送 /author 通知作者。')


@Client.on_message(filters.regex(r".*maimai.*什么")
                    & filters.text)
async def mw(Client, Message):
    try:
        photo, caption = song_txt(total_list.random())
        await Message.reply_photo(photo=photo, caption=caption)
    except:
        error = traceback.format_exc(limit=15)
        record = 'An error occurred when processing message:\n<code>' + Message.text + '</code>\nBy user: ' + await fullname(Message.from_user) + ' ( tg://user?id=' + str(Message.from_user.id) + ' )\nThe error des:\n' + str(error)
        await Client.send_message(int(Record_ID), record)
        await Message.reply('错误触发，请重新发送指令。若多次触发错误请发送 /author 通知作者。')


@Client.on_message(filters.regex(r"^查歌.+")
                    &filters.text)
async def search(Client, Message):
    try:
        regex = "查歌(.+)"
        name = re.match(regex, str(Message.text)).groups()[0].strip()
        if name == "":
            await Message.reply("请输入曲子名字。")
            return
        res = total_list.filter(title_search=name)
        if len(res) == 0:
            await Message.reply("抱歉，没有找到这样的乐曲。")
        elif len(res) < 151:
            search_result = ""
            for music in sorted(res, key = lambda i: int(i['id'])):
                search_result += f"{music['id']}. {music['title']}\n"
            await Message.reply(search_result)
        else:
            await Message.reply(f"结果过多（{len(res)} 条），请缩小查询范围至150条以下。")
    except:
        error = traceback.format_exc(limit=15)
        record = 'An error occurred when processing message:\n<code>' + Message.text + '</code>\nBy user: ' + await fullname(Message.from_user) + ' ( tg://user?id=' + str(Message.from_user.id) + ' )\nThe error des:\n' + str(error)
        await Client.send_message(int(Record_ID), record)
        await Message.reply('错误触发，请重新发送指令。若多次触发错误请发送 /author 通知作者。')

@Client.on_message(filters.regex(r"^([绿黄红紫白]?)id([0-9]+)")
                    &filters.text)
async def query(Client, Message):
    try:
        regex = "([绿黄红紫白]?)id([0-9]+)"
        groups = re.match(regex, str(Message.text)).groups()
        level_labels = ['绿', '黄', '红', '紫', '白']
        if groups[0] != "":
            try:
                level_index = level_labels.index(groups[0])
                level_name = ['Basic', 'Advanced', 'Expert', 'Master',  'Re: MASTER']
                name = groups[1]
                music = total_list.by_id(name)
                chart = music['charts'][level_index]
                ds = music['ds'][level_index]
                level = music['level'][level_index]
                file = f"https://www.diving-fish.com/covers/{get_cover_len5_id(music['id'])}.png"
                if len(chart['notes']) == 4:
                    msg = f'''{level_name[level_index]} {level}({ds})
TAP: {chart['notes'][0]}
HOLD: {chart['notes'][1]}
SLIDE: {chart['notes'][2]}
BREAK: {chart['notes'][3]}
谱师: {chart['charter']}'''
                else:
                    msg = f'''{level_name[level_index]} {level}({ds})
TAP: {chart['notes'][0]}
HOLD: {chart['notes'][1]}
SLIDE: {chart['notes'][2]}
TOUCH: {chart['notes'][3]}
BREAK: {chart['notes'][4]}
谱师: {chart['charter']}'''
                r_text = f"{music['id']}. {music['title']}\n" + msg
                await Message.reply_photo(photo=file, caption=r_text)
            except Exception:
                await Message.reply("未找到该谱面")
        else:
            name = groups[1]
            music = total_list.by_id(name)
            try:
                file =f"https://www.diving-fish.com/covers/{get_cover_len5_id(music['id'])}.png"
                r_text = f"{music['id']}. {music['title']}\n" + f"艺术家: {music['basic_info']['artist']}\n分类: {music['basic_info']['genre']}\nBPM: {music['basic_info']['bpm']}\n版本: {music['basic_info']['from']}\n难度: {'/'.join(music['level'])}"
                await Message.reply_photo(photo=file, caption=r_text)
            except Exception:
                await Message.reply("未找到该乐曲")
    except:
        error = traceback.format_exc(limit=15)
        record = 'An error occurred when processing message:\n<code>' + Message.text + '</code>\nBy user: ' + await fullname(Message.from_user) + ' ( tg://user?id=' + str(Message.from_user.id) + ' )\nThe error des:\n' + str(error)
        await Client.send_message(int(Record_ID), record)
        await Message.reply('错误触发，请重新发送指令。若多次触发错误请发送 /author 通知作者。')

@Client.on_message(filters.command('today_mai')
                    & filters.text)
async def jrwm(Client, Message):
    try:
        user_id = int(Message.from_user.id)
        h = hash(user_id)
        rp = h % 100
        wm_value = []
        for i in range(11):
            wm_value.append(h & 3)
            h >>= 2
        s = f"今日人品值：{rp}\n"
        for i in range(11):
            if wm_value[i] == 3:
                s += f'宜 {wm_list[i]}\n'
            elif wm_value[i] == 0:
                s += f'忌 {wm_list[i]}\n'
        me = await Client.get_users("me")
        s += me.first_name + " 提醒您：打机时不要大力拍打或滑动哦\n今日推荐歌曲："
        music = total_list[h % len(total_list)]
        photo, caption = song_txt(music)
        await Message.reply(s)
        await Message.reply_photo(photo=photo, caption=caption)
    except:
        error = traceback.format_exc(limit=15)
        record = 'An error occurred when processing message:\n<code>' + Message.text + '</code>\nBy user: ' + await fullname(Message.from_user) + ' ( tg://user?id=' + str(Message.from_user.id) + ' )\nThe error des:\n' + str(error)
        await Client.send_message(int(Record_ID), record)
        await Message.reply('错误触发，请重新发送指令。若多次触发错误请发送 /author 通知作者。')  


@Client.on_message(filters.command('pointer')
                    & filters.text)
async def score(Client, Message):
    try:
        r = "([绿黄红紫白])(id)?([0-9]+)"
        argv = str(Message.text).strip().split(" ")
        if len(argv) == 2 and argv[1] == '帮助':
            s = '''此功能为查找某首歌分数线设计。
命令格式：/pointer <难度+歌曲id> <分数线>
难度为5种，绿 黄 红 紫 白
例如：/pointer 紫799 100
命令将返回分数线允许的 TAP GREAT 容错以及 BREAK 50落等价的 TAP GREAT 数。
以下为 TAP GREAT 的对应表：
GREAT/GOOD/MISS
TAP     1/2.5/5
HOLD    2/5/10
SLIDE   3/7.5/15
TOUCH   1/2.5/5
BREAK   5/12.5/25(外加200落)'''
            img = text_to_image(s)
            output = BytesIO()
            img.save(output, format="PNG")
            await Message.reply_photo(photo=output)
        elif len(argv) == 3:
            try:
                grp = re.match(r, argv[1]).groups()
                level_labels = ['绿', '黄', '红', '紫', '白']
                level_labels2 = ['Basic', 'Advanced', 'Expert', 'Master', 'Re:MASTER']
                level_index = level_labels.index(grp[0])
                chart_id = grp[2]
                line = float(argv[2])
                music = total_list.by_id(chart_id)
                chart: Dict[Any] = music['charts'][level_index]
                tap = int(chart['notes'][0])
                slide = int(chart['notes'][2])
                hold = int(chart['notes'][1])
                touch = int(chart['notes'][3]) if len(chart['notes']) == 5 else 0
                brk = int(chart['notes'][-1])
                total_score = 500 * tap + slide * 1500 + hold * 1000 + touch * 500 + brk * 2500
                break_bonus = 0.01 / brk
                break_50_reduce = total_score * break_bonus / 4
                reduce = 101 - line
                if reduce <= 0 or reduce >= 101:
                    raise ValueError
                await Message.reply(f'''{music['title']} {level_labels2[level_index]}
分数线 {line}% 允许的最多 TAP GREAT 数量为 {(total_score * reduce / 10000):.2f}(每个-{10000 / total_score:.4f}%),
BREAK 50落(一共{brk}个)等价于 {(break_50_reduce / 100):.3f} 个 TAP GREAT(-{break_50_reduce / total_score * 100:.4f}%)''')
            except Exception as e:
                await Message.reply("数据错误，请重新输入数值。\n输入 <code>/pointer 帮助</code> 以查看帮助信息")
        else:
            await Message.reply("信息输入错误，输入 <code>/pointer 帮助</code> 以查看帮助信息")
    except:
        error = traceback.format_exc(limit=15)
        record = 'An error occurred when processing message:\n<code>' + Message.text + '</code>\nBy user: ' + await fullname(Message.from_user) + ' ( tg://user?id=' + str(Message.from_user.id) + ' )\nThe error des:\n' + str(error)
        await Client.send_message(int(Record_ID), record)
        await Message.reply('错误触发，请重新发送指令。若多次触发错误请发送 /author 通知作者。')


@Client.on_message(filters.command('b40')
                    & filters.text)
async def b40(Client, Message):
    try:
        argv = str(Message.text).strip().split(" ")
        if len(argv) > 2 or len(argv) == 1:
            await Message.reply('命令格式为\n/b40 (查询账号的用户名)\n使用此功能请确保已前往 <a href="https://www.diving-fish.com/maimaidx/prober/">舞萌DX查分器</a> 绑定账号', disable_web_page_preview=True, parse_mode=ParseMode.HTML)
            return
        if len(argv) == 2:
            Wait_M = await Message.reply("获取用户信息中。。。")
            payload = {'username': argv[1]}
            img, success = await generate(payload)
        if success == 400:
            await Wait_M.edit_text('未找到此玩家，请确保此玩家的用户名和查分器中的用户名相同。\n使用此功能请确保已前往 <a href="https://www.diving-fish.com/maimaidx/prober/">舞萌DX查分器</a> 绑定账号', disable_web_page_preview=True, parse_mode=ParseMode.HTML)
            return
        elif success == 403:
            await Wait_M.edit_text('该用户已设置禁止了其他人获取数据。可前往 <a href="https://www.diving-fish.com/maimaidx/prober/">舞萌DX查分器</a> 官网登录账号，然后点击右上角 <i>"编辑个人资料"</i> 修改', disable_web_page_preview=True, parse_mode=ParseMode.HTML)
            return
        else:
            output = BytesIO()
            img.save(output, format="PNG")
            await Wait_M.delete()
            await Message.reply_photo(photo=output)
    except:
        error = traceback.format_exc(limit=15)
        record = 'An error occurred when processing message:\n<code>' + Message.text + '</code>\nBy user: ' + await fullname(Message.from_user) + ' ( tg://user?id=' + str(Message.from_user.id) + ' )\nThe error des:\n' + str(error)
        await Client.send_message(int(Record_ID), record)
        await Message.reply('错误触发，请重新发送指令。若多次触发错误请发送 /author 通知作者。')


@Client.on_message(filters.command('b50')
                    & filters.text)
async def b50(Client, Message):
    try:
        argv = str(Message.text).strip().split(" ")
        if len(argv) > 2 or len(argv) == 1:
            await Message.reply('命令格式为\n/b50 (查询账号的用户名)\n使用此功能请确保已前往 <a href="https://www.diving-fish.com/maimaidx/prober/">舞萌DX查分器</a> 绑定账号', disable_web_page_preview=True, parse_mode=ParseMode.HTML)
            return
        if len(argv) == 2:
            Wait_M = await Message.reply("获取用户信息中。。。")
            payload = {'username': argv[1], 'b50': True}
            img, success = await generate50(payload)
        if success == 400:
            await Wait_M.edit_text('未找到此玩家，请确保此玩家的用户名和查分器中的用户名相同。\n使用此功能请确保已前往 <a href="https://www.diving-fish.com/maimaidx/prober/">舞萌DX查分器</a> 绑定账号', disable_web_page_preview=True, parse_mode=ParseMode.HTML)
            return
        elif success == 403:
            await Wait_M.edit_text('该用户已设置禁止了其他人获取数据。可前往 <a href="https://www.diving-fish.com/maimaidx/prober/">舞萌DX查分器</a> 官网登录账号，然后点击右上角 <i>"编辑个人资料"</i> 修改', disable_web_page_preview=True, parse_mode=ParseMode.HTML)
            return
        else:
            output = BytesIO()
            img.save(output, format="PNG")
            await Wait_M.delete()
            await Message.reply_photo(photo=output)
    except:
        error = traceback.format_exc(limit=15)
        record = 'An error occurred when processing message:\n<code>' + Message.text + '</code>\nBy user: ' + await fullname(Message.from_user) + ' ( tg://user?id=' + str(Message.from_user.id) + ' )\nThe error des:\n' + str(error)
        await Client.send_message(int(Record_ID), record)
        await Message.reply('错误触发，请重新发送指令。若多次触发错误请发送 /author 通知作者。')
