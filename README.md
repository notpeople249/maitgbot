# mai tg bot 使用指南

此bot由 Diving-Fish/mai-bot 的源码修改而成，使用了python的pyrogram与Telegram的服务器交流。

此 README 提供了最低程度的 maitgbot 教程与支持。

**建议您至少拥有一定的编程基础之后再尝试使用本工具。**

**此源码编写于Windows 11， Python 3 版本 > 3.9，并测试于 Ubuntu 20.02 与 Debian 10。如有遇到其它问题，到Issue里提。**

## Step 1. 安装 Python 3

请自行前往 https://www.python.org/ 下载 Python 3 版本（> 3.7）并将其添加到环境变量（在安装过程中勾选 Add Python to system PATH）。对大多数用户来说，您应该下载 Windows installer (64-bit)。

在 Linux 系统上，需要依照其他安装步骤，请自行查找。

## Step 2. 安装 Python 3 Pip

Python 3 PIP 为 python 安装依赖包的应用，属于必要程序。以下方法为 Windows 版教程， **Linux 下执行 `apt-get install python3-pip` 即可**。

首先打开 cmd.exe ，然后 选择一个目录后下载 get-pip.py 的文件：
```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
```

过后在同一个目录下执行以下指令
```
python get-pip.py
```

最后使用此指令确保pip能显示当前已安装的版本
```
pip --version
```

## Step 3. 获取机器人的环境设置内容

因为 Telegram 的限制，因此使用 Pyrogram 登录机器人需要准备三样东西，都必须得有 Telegram 账号才可获得。三样东西分别为 Api ID， Api Hash，和 Bot Token。

打开 https://my.telegram.org/auth 网站，然后登录个人 Telegram 账号。然后选择 `API development tools` ，之后在`App title:`输入 `MaiMai DF bot` ，`Short name:`输入 `MaiTGBot` 和`URL:`输入 此项目的链接。（或其他任何内容皆可，但尽量真实避免导致封禁你的个人账号）
至于`Platform：`可以随选，之后点击 `Create application` 即可获取 `Api ID` 和 `Api Hash` 。

接下来打开 Telegram ，寻找 [@BotFather](https://t.me/BotFather) 创建一个机器人（发送`/newbot`->设置bot的名字->设置bot的用户名->机器人创建完毕），然后就能获得bot的token了。接下来就是准备运行项目。

## Step 4. 运行项目

您可以直接在本界面下载代码的压缩包进行运行。也可以安装完成 Git 后使用 cmd.exe 执行指令然后下载代码到指定的文件夹。
```
git clone https://github.com/notpeople249/maitgbot '下载保存的路径'
```

**在运行代码之前，您需要从 [此链接](https://www.diving-fish.com/maibot/static.zip) 下载资源文件并解压到`src`文件夹中。

在运行代码之前，您需要从 [此链接](https://www.diving-fish.com/maibot/static.zip) 下载资源文件并解压到`src`文件夹中。

在运行代码之前，您需要从 [此链接](https://www.diving-fish.com/maibot/static.zip) 下载资源文件并解压到`src`文件夹中。**

> 资源文件仅供学习交流使用，请自觉在下载 24 小时内删除资源文件。

在此之后，**您需要打开控制台，并切换到该项目所在的目录。**
在 Windows 10 系统上，您可以直接在项目的根目录（即 bot.py）文件所在的位置按下 Shift + 右键，点击【在此处打开 PowerShell 窗口】。
如果您使用的是更旧的操作系统（比如 Windows 7），请自行查找关于`Command Prompt`，`Powershell`以及`cd`命令的教程。

之后，在打开的控制台中输入
```
python --version
```
控制台应该会打印出 Python 的版本。如果提示找不到 `python` 命令，请检查环境变量或干脆重装 Python，**并务必勾选 Add Python to system PATH**。

之后，输入
```
pip install -r requirements.txt
```
安装依赖完成后，打开`.env`文件填写上一步骤中获取的 `Api ID` ， `Api Hash` 和 `Bot Token` （如果没有请查看回上一步骤获取），以及 `Record_Channel_ID` (此为记录频道的id，可新建频道并把机器人添加为频道管理员。)
例子（仅供参考，无法使用）：
```
API_ID = '35846523'
API_HASH = '65s1vrd68vs4r5v1e89dv4s6d4v5ef14b520tbf'
BTOKEN = '123456789:D54FGA556RFG4AF-46WE5FVADS!4FG98'
Record_Channel_ID = '-1005478811271'
```
最后运行即可。（Linux 下把 `python` 更换为 `python3` ）
```
python main.py
```
运行项目。如果输出如下所示的内容，代表运行成功：
```
机器人已启动!
时间于：（当前时间） 
```
**运行成功后请勿关闭此窗口。**

## Step 5. 后台运行

**此步骤为 Linux 系统专用， Windows 运行的请自行查找方式。**

上一步骤运行成功后，键盘中敲击
```
Ctrl + C
```

退出运行后，复制粘贴此段：
```
cat <<'TEXT' > /etc/systemd/system/maitgbot.service
[Unit]
Description=MaiMai's Checker Telegram Bot
After=network.target

[Install]
WantedBy=multi-user.target

[Service]
Type=simple
WorkingDirectory=/root/maitgbot
ExecStart=python3 main.py
Restart=always
TEXT
```

然后就可以使用以下指令控制在后台的程序
```
systemctl enable maitgbot  （开启开机自动启动）
systemctl disable maitgbot （关闭开机自动启动）
systemctl start maitgbot   （启动程序）
systemctl stop maitgbot    （停止程序）
```

## FAQ

想要关闭电脑 / 程序但保持项目运行，可以吗？
>建议请把项目运行于服务器上， Windows 或 Linux（Ubuntu/Debian/CentOS/AlmaLinux/Rocky Linux/等等等）皆可，然后长期运行。 <br> Linux 上建议搭配 screen 或 tmux 等类似的程序一起使用。

机器人对b40和b50指令无反应，如何解决？
>目前发现问题为无法连接上舞萌DX查分器的api，貌似因为网页修改导致的异常。现观察为已修复。

有问题想询问？（仅限于 Telegram 版，如想询问 QQ 版请移步到原项目询问。）
>可在 Telegram 群组 [@xiaopoqun](https://t.me/xiaopoqun) 说明，看见后会回复。(入群需要通过入群验证，失败需等待数分钟后重新入群完成验证。)

## 说明

本 bot 提供了如下功能：

命令 | 功能
--- | ---
/help | 查看帮助文档
/today_mai | 查看今天的舞萌运势
/update | 查看机器人更新记录
/author | 发现问题？请加入群向作者反馈
...maimai...什么 | 随机一首歌
随个[dx/标准][绿黄红紫白]<难度> | 随机一首指定条件的乐曲
查歌<乐曲标题的一部分> | 查询符合条件的乐曲
[绿黄红紫白]id<歌曲编号> | 查询乐曲信息或谱面信息
/inner_level <定数> <br> /inner_level <定数下限> <定数上限> |  查询定数对应的乐曲
/pointer <难度+歌曲id> <分数线> | 展示歌曲的分数线
/b40 (查询账号的用户名) | 根据查分器数据生成你的Best 40数据图
/b50 (查询账号的用户名) | 根据查分器数据生成你的Best 50数据图

## License

MIT

您可以自由使用本项目的代码用于商业或非商业的用途，但必须附带 MIT 授权协议。
