# coding=utf-8

import itchat
from itchat.content import *
import time
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import os, shutil
import re
import random
import requests as rq
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# 文件临时存储文件夹
rec_tmp_dir = os.path.join(os.getcwd(), 'tmp/')

# 撤回文件存储文件夹
img_file = os.path.join(os.getcwd(), 'img/')

# 存储数据的字典
rec_msg_dict = {}  

# 怼狗次数
dog_num = 6

# 图灵API接口
api_url = 'http://openapi.tuling123.com/openapi/api/v2'

headers = {
    'Content-Type': 'application/json',
    'Host': 'openapi.tuling123.com',
    'User-Agent': 'Mozilla/5.0 (Wi`ndows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3486.0 '
    'Safari/537.36 '
}

# 怼狗话术
dog_Reply = {
    '1': '叫个J8你叫',
    '2': '你瞎bb什么',
    '3': '你叫尼🐎呢？',
    '4': '一个反身碎骨Q!跑你麻痹的东方明珠塔!',
    '5': '老子打烂你的香蕉船！',
    '6': '干尼玛折耳根香油',
    '7': '蒙多蒙多，棒皮棒皮',
    '8': '你叫他妈的象拔蚌',
    '9': '我这装备，现在一个R，简直是TM终极蛇怪铁蛋火车侠日尼玛威猛先生无敌风火轮上去就是一顿敲，打的你这个臭嗨香蕉船皮皮怪立马稀巴烂成一片太平洋',
    '10': '傻狗闭嘴！',
    '11': '你在bb老子一拳把黄浦江的水打飞',
    '12': '你是真的皮，我反手就是一个翻皮水',
    '13': '以为自己很帅?不存在的。',
    '14': '你骚任你骚，我补我的刀',
    '15': '我对着你的狗头就是一记重抓萧峰标葵花起跳马氏跑动杀接起立再一脚下盘不是很稳打出KO',
    '16': '铁头娃，愣头青！头铁得就没边了！你这个头就是平板锅做的，多铁啊',
    '17': '你是真皮沙发！',
    '18': '摆摆手~你知道吗?如果你不知道，你就没有灵性',
    '19': '你的头是真的铁，铁头娃。',
    '20': '你怕是石乐志'
}

# 讨论组信息监听
@itchat.msg_register([TEXT, PICTURE, RECORDING, ATTACHMENT, VIDEO, SHARING, SYSTEM, FRIENDS, NOTE], isGroupChat=True)
def information(msg):
    botName = itchat.get_friends(update=True)[0]['NickName']
    chat_rooms = itchat.get_chatrooms()
    if len(chat_rooms) > 0:
        msg_id = msg['MsgId']
        msg_from_user = msg['ActualNickName']
        msg_content = ''
        # 收到信息的时间
        msg_time_rec = time.strftime("%Y-%m-%d %H:%M%S", time.localtime())
        msg_create_time = msg['CreateTime']
        msg_type = msg['Type']

        if msg['Type'] == 'Text':
            msg_content = msg['Content']
        elif msg['Type'] == 'Picture' \
                or msg['Type'] == 'Recording' \
                or msg['Type'] == 'Video' \
                or msg['Type'] == 'Attachment':
            msg_content = r"" + msg['FileName']
            msg['Text'](rec_tmp_dir + msg['FileName'])

        rec_msg_dict.update({
            msg_id: {
                'msg_from_user': msg_from_user,
                'msg_time_rec': msg_time_rec,
                'msg_create_time': msg_create_time,
                'msg_type': msg_type,
                'msg_content': msg_content
            }
        })

        random_num = random.randint(0,20)

        Reply = '???'

        isCall = re.match(r'(.*)机器猫(.*)', str(msg_content))

        if msg_from_user == "王二狗" \
            or msg_from_user == "哈小奇难得":
            global dog_num
            if dog_num > 0:
                dog_num -= 1
                if msg_type == 'Sharing':
                    if random_num < 10:
                        Reply = '你分享个什么gouJb东西'
                    else:
                        Reply = '分享的什么玩意傻狗'
                else:
                    Reply = dog_Reply.get(str(random_num))

                itchat.send_msg('@' + msg_from_user + " " + Reply, msg['FromUserName'])
                if random_num <= 6:
                    itchat.send_image(img_file + 'dog.jpg', msg['FromUserName'])
        
        elif isCall:
            if isCall.group(2) == '':
                if msg_from_user == u'\uabed':
                    random_num2 = random.randint(0, 8)
                    if random_num2 < 6:
                        itchat.send_image(img_file + 'cat' + str(random_num2) + '.jpg', msg['FromUserName'])
                    else:
                        itchat.send_msg('喵喵喵~', msg['FromUserName'])
                else:
                    if random_num < 6:
                        Reply = '叫个J8你叫'
                    elif random_num >= 6 and random_num < 15:
                        Reply = '想我了?'
                    itchat.send_msg(Reply, msg['FromUserName'])  
            else:
                tulingBotReply(isCall.group(2), msg['FromUserName'])

        elif re.match(r'(.*)爆照(.*)', str(msg_content)):
            itchat.send_msg(str(msg_content), msg['FromUserName'])

        elif msg_content == "爆照" \
            or msg_content == "新人爆照" \
            or re.match(r'爆照(.*?)', str(msg_content)):
            tulingBotReply(str(msg_content)[9:], msg['FromUserName'])

        elif msg['isAt']:
            msg_content = str(msg_content[len(botName)+1:]).strip().replace(" ", "")
            if msg_content == '':
                if msg_from_user == u'\uabed':
                    random_num2 = random.randint(0, 6)
                    if random_num2 < 6:
                        itchat.send_image(img_file + 'cat' + str(random_num2) + '.jpg', msg['FromUserName'])
                    else:
                        itchat.send_msg('喵喵喵~', msg['FromUserName'])
                else:
                    if random_num < 6:
                        Reply = ' 叫个J8你叫'
                    elif random_num >= 6 and random_num < 15:
                        Reply = ' 想我了?'
                    else: 
                        Reply = ' 干嘛?'
                    itchat.send_msg(Reply, msg['FromUserName'])
            else:
                tulingBotReply(msg_content, msg['FromUserName'])


@itchat.msg_register([NOTE], isFriendChat=True, isGroupChat=True)
def revoke_msg(msg):
    nickName = itchat.get_friends(update=True)[1]['NickName']
    is_revoke = re.search(r'(.*)CDATA(.*)撤回了一条消息]]>', str(msg['Content']))
    if is_revoke is not None:
        old_msg_id = re.search(r'<msgid>(.*)</msgid>',
                               is_revoke.group(1)).group(1)
        old_msg = rec_msg_dict.get(old_msg_id, {})
        # 先发送一条文字信息
        type_obj = {
            'Text': "一条文字信息",
            'Picture': "一张图片",
            'Recording': "一段语音",
            'Video': "一个视频",
            'Attachment': "一个文件"
        }
        key = str(old_msg.get('msg_type'))
        revoke_file_type = type_obj.get(key, '一条文字信息')
        if old_msg.get('msg_from_user') != u'\uabed':
            itchat.send_msg(str("@" + nickName + " " + old_msg.get('msg_from_user') + "撤回了") + revoke_file_type, msg['FromUserName'])
            itchat.send_msg(str(old_msg.get('msg_from_user') + "撤回了" + revoke_file_type + ": " + old_msg.get('msg_content')), toUserName="filehelper")

        # 判断文msg_content是否存在，不存在说明可能是
            if os.path.exists(os.path.join(rec_tmp_dir, old_msg.get('msg_content'))):
                if old_msg.get('msg_type') == 'Picture':
                    itchat.send_image(os.path.join(rec_tmp_dir, old_msg.get('msg_content')),
                                    toUserName="filehelper")
                elif old_msg.get('msg_type') == 'Video':
                    itchat.send_video(os.path.join(rec_tmp_dir, old_msg.get('msg_content')),
                                    toUserName="filehelper")
                elif old_msg.get('msg_type') == 'Attachment' \
                        or old_msg.get('msg_type') == 'Recording':
                    itchat.send_file(os.path.join(rec_tmp_dir, old_msg.get('msg_content')),
                                    toUserName="filehelper")


#图灵机器人自动回复
def tulingBotReply(msg, user):
    data = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": msg
            }
        },
        "userInfo": {
            "apiKey": "efbe8935873f4f7a9b4074b741a3e804",
            "userId": "123"
        }
    }
    result = rq.post(api_url, headers=headers, json=data).json()
    itchat.send_msg(result['results'][0]['values']['text'], user)

# 定时问候任务
def morning():
    for i in itchat.get_chatrooms():
        itchat.send_msg('小哥哥小姐姐们，古德摸宁！', i['UserName'])

# 定时问候任务
def afternoon():
    for i in itchat.get_chatrooms():
        itchat.send_msg('小哥哥小姐姐们，你们特么的下午好啊！', i['UserName'])

def evening():
    for i in itchat.get_chatrooms():
        itchat.send_msg('小哥哥小姐姐们，你们特么的晚上好啊！', i['UserName'])

# 每隔五种分钟执行一次清理任务
def clear_cache():
    global rec_msg_dict
    global dog_num
    dog_num = 6
    rec_msg_dict = {}
    for root, dirs, files in os.walk(rec_tmp_dir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))

# 开始轮询任务
def start_schedule():
    sched.add_job(clear_cache, 'interval', minutes=5)
    sched.add_job(morning, 'cron', hour=8)
    sched.add_job(afternoon, 'cron', hour=13)
    sched.add_job(evening, 'cron', hour=20)
    sched.start()

# 退出停止所有任务并清空缓存文件夹
def after_logout():
    sched.shutdown()
    shutil.rmtree(rec_tmp_dir)

if __name__ == '__main__':
    sched = BlockingScheduler()
    if not os.path.exists(rec_tmp_dir):
        os.mkdir(rec_tmp_dir)
    itchat.auto_login(hotReload=True, enableCmdQR=2)
    itchat.run(blockThread=False)
    start_schedule()