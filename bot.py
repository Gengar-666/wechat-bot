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

import logging
logging.basicConfig()

# 文件临时存储文件夹
rec_tmp_dir = os.path.join(os.getcwd(), 'tmp/')

# 回复图片
img_file = os.path.join(os.getcwd(), 'img/')

# 存储数据的字典
rec_msg_dict = {}  

# 关闭的讨论组集合
closeArr = []

# 怼狗次数
dog_num = 1

# 图灵API接口
api_url = 'http://openapi.tuling123.com/openapi/api/v2'

# 请求头
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
    '7': '撤回！',
    '8': '你叫他妈的象拔蚌',
    '9': '我这装备，现在一个R，简直是TM终极蛇怪铁蛋火车侠日尼玛威猛先生无敌风火轮上去就是一顿敲，打的你这个臭嗨香蕉船皮皮怪立马稀巴烂成一片太平洋',
    '10': '傻狗闭嘴！',
    '11': '你在bb老子一拳把黄浦江的水打飞',
    '12': '大吉大利，今晚吃鸡',
    '13': '以为自己很帅?不存在的。',
    '14': '你骚任你骚，我补我的刀',
    '15': '我对着你的狗头就是一记重抓萧峰标葵花起跳马氏跑动杀接起立再一脚下盘不是很稳打出KO',
    '16': '你这个头就是平板锅做的，多铁啊',
    '17': '你是真皮沙发！',
    '18': '真香警告',
    '19': '你怕是石乐志',
    '20': 'CNMua~',
    '21': '再bb把你抓去和袋鼠打拳击',
    '22': '再bb把你发配到南极捡企鹅屎',
    '23': '5fuck缩',
    '24': 'funny🐎的pee',
    '25': '该死，我的老伙计你真是坏极了，就像发了霉的烂橘子',
    '26': '2B不只是铅笔，还有你',
    '27': '你不会是不知火舞的弟弟不知好歹吧',
    '28': '看在你丑的份上,就当你说的是对的吧',
    '29': '吔屎啦你',
    '30': '你吹咩',
    '31': '躝开',
    '32': '讲甘多托膝咩，吔个包先拉',
    '33': '雷猴啊，索嗨',
    '34': '你快d行柒开',
    '35': '你今日唔记得带个脑出街咩？',
    '36': '你叫咩，我都劈你只扑街',
    '37': '我冇👀睇你，扑街',
    '38': '睇到你个样我就想报警',
    '39': '收声啦，锁嗨',
    '40': '傻仔 都话咗你个死人白痴仔 讲野唔仑得正',
    '41': '叼你啊死捞头,信悟信我起你天灵盖度疴督屎啊',
    '42': '想升你两巴掌',
    '43': '我顶你的肺，我戳你个咀',
    '44': '人之初，口多多！！手指指，食鸡屎！！',
    '45': '丢',
    '46': '你信唔信我收你皮！',
    '47': '你睇下你，整个麻甩佬甘样，不好行埋黎啊',
    '48': '有种你唔好走等我call友',
    '49': '有种你讲多次',
    '50': '叼你卤味！',
    '51': '你条粉肠',
    '52': '信唔信我一巴hum到你阿妈都唔认得',
    '53': '傻狗，退下',
    '54': '叫爸爸',
    '55': '你再bb一句试试',
    '56': '侬脑子瓦特了',
    '57': '傻狗！',
    '58': '？？？',
    '59': '哪来的傻狗',
    '60': '叫爸爸'
}

# 好友信息监听
@itchat.msg_register([TEXT, PICTURE, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True)
def handle_friend_msg(msg):
    if msg['Content'] == '更新次数':
        global dog_num
        dog_num = 1


# 讨论组信息监听
@itchat.msg_register([TEXT, PICTURE, MAP, CARD, RECORDING, ATTACHMENT, VIDEO, SHARING], isGroupChat=True)
def information(msg):
    global closeArr
    # 机器人昵称
    botName = str(itchat.get_friends(update=True)[0]['NickName'])
    # 讨论组集合
    chat_rooms = itchat.get_chatrooms()
    # 当前讨论组名称
    room_name = str(msg['User']['NickName']).decode()
    # 消息id
    msg_id = str(msg['MsgId']).decode()
    # 发消息人昵称
    msg_from_user = str(msg['ActualNickName'])
    # 消息内容
    msg_content = ''
    # 收到信息的时间
    msg_time_rec = time.strftime("%Y-%m-%d %H:%M%S", time.localtime())
    msg_create_time = msg['CreateTime']
    # 消息类型
    msg_type = msg['Type']

    if msg['Type'] == 'Text' \
        or msg['Type'] == 'Sharing':
            msg_content = str(msg['Content']).replace("\n", "").replace("\t","")
    elif msg['Type'] == 'Picture' \
        or msg['Type'] == 'Recording' \
        or msg['Type'] == 'Video' \
        or msg['Type'] == 'Attachment':
        msg_content = r"" + msg['FileName']
        msg['Text'](rec_tmp_dir + msg['FileName'])
    elif msg['Type'] == 'Card':
        msg_content = msg['RecommendInfo']['NickName'] + r" 的名片"
    elif msg['Type'] == 'Map':
        x, y, location = re.search(
            "<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*", msg['OriContent']).group(1, 2, 3)
        if location is None:
            msg_content = r"纬度->" + x.__str__() + " 经度->" + y.__str__()
        else:
            msg_content = r"" + location

    rec_msg_dict.update({
        msg_id: {
            'msg_from_user': msg_from_user,
            'msg_time_rec': msg_time_rec,
            'msg_create_time': msg_create_time,
            'msg_type': msg_type,
            'msg_content': msg_content
        }
    })

    isCall = re.match(r'(.*)机器猫(.*)', str(msg_content))

    if len(chat_rooms) > 0 and not room_name in closeArr:
        if re.findall(r"王二狗", msg_from_user) \
            or re.findall(r"哈小奇难得", msg_from_user):
            random_num = random.randint(1,60)
            Reply = ''
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
                if random.randint(0, 5) <= 2:
                    itchat.send_image(img_file + str(random.randint(1, 5)) + '.jpg', msg['FromUserName'])
        
        elif isCall and not msg['IsAt']:
            if isCall.group(2) == '':
                img_random = random.randint(1, 23)
                if img_random < 20:
                    itchat.send_image(img_file + 'cat' + str(img_random) + '.jpg', msg['FromUserName'])
                else:
                    itchat.send_msg('喵喵喵~', msg['FromUserName'])
            else:
                if isCall.group(2).strip() == '关闭' and msg_from_user == u'\uabed':
                    closeArr.append(room_name)
                    itchat.send_msg('机器猫已关闭', msg['FromUserName'])
                elif not choose_song(isCall.group(2), msg['FromUserName']):
                    tulingBotReply(isCall.group(2), msg['FromUserName'])

        elif re.match(r'(.*)爆照(.*)', str(msg_content)):
            itchat.send_msg(str(msg_content), msg['FromUserName'])

        elif msg['isAt']:
            msg_content = str(msg_content[len(botName)+1:]).strip().replace(" ", "")
            if msg_content == '':
                img_random = random.randint(1, 23)
                if img_random < 20:
                    itchat.send_image(img_file + 'cat' + str(img_random) + '.jpg', msg['FromUserName'])
                else:
                    itchat.send_msg('喵喵喵~', msg['FromUserName'])
            else:
                if msg_content.strip() == '关闭' and msg_from_user == u'\uabed':
                    closeArr.append(room_name)
                    itchat.send_msg('机器猫已关闭', msg['FromUserName'])
                elif not choose_song(isCall.group(2), msg['FromUserName']):
                    tulingBotReply(isCall.group(2), msg['FromUserName'])

    elif len(chat_rooms) > 0 and room_name in closeArr: 
        if re.match(r'(.*)开启(.*)', str(msg['Content'])) and msg_from_user == u'\uabed':
            closeArr.remove(room_name)
            itchat.send_msg('机器猫已开启', msg['FromUserName'])

@itchat.msg_register([NOTE], isFriendChat=True, isGroupChat=True)
def revoke_msg(msg):
    nickName = str(itchat.get_friends(update=True)[1]['NickName'])
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
            'Attachment': "一个文件",
            'Sharing': "一个分享",
            'Map': "一个位置信息",
            'Card': "一个名片分享",
        }
        key = str(old_msg.get('msg_type'))
        revoke_file_type = type_obj.get(key, '一条文字信息')
        if str(old_msg.get('msg_type')) == 'Sharing':
            sharing_appid = re.match(r'(.*)appid="(.*)" sdkver', str(old_msg.get('msg_content'))).group(2)
            if not sharing_appid:
                revoke_file_type = '一个小程序'
                old_msg['msg_content'] = re.match(r'(.*)<sourcedisplayname>(.*)</sourcedisplayname>', str(old_msg.get('msg_content'))).group(2) + "，" + '\r\n描述：' + re.findall(r"<title>(.+?)</title>", str(old_msg.get('msg_content')))[0]
            else:
                sharing_from = re.match(r'(.*)<appname>(.*)</appname></appinfo>', str(old_msg.get('msg_content'))).group(2)
                sharing_content = re.findall(r"<title>(.+?)</title>", str(old_msg.get('msg_content')))[0]
                sharing_url = re.match(r'(.*)<url>(.*)</url><lowurl', str(old_msg.get('msg_content'))).group(2)
                old_msg['msg_content'] = sharing_content + '\r\n链接：' + sharing_url + '\r\n来源：' + sharing_from
        if old_msg.get('msg_from_user') != u'\uabed':
            if str(old_msg.get('msg_type')) == 'Sharing' \
                or str(old_msg.get('msg_type')) == 'Map' \
                or str(old_msg.get('msg_type')) == 'Card':
                itchat.send_msg(str(old_msg.get('msg_from_user')) + "撤回了" + str(revoke_file_type) + ": " + str(old_msg.get('msg_content')), msg['FromUserName'])
                itchat.send_msg(str(old_msg.get('msg_from_user')) + "撤回了" + str(revoke_file_type) + ": " + str(old_msg.get('msg_content')), toUserName="filehelper")
            else:
                itchat.send_msg(str(old_msg.get('msg_from_user')) + "撤回了" + str(revoke_file_type), msg['FromUserName'])
                itchat.send_msg(str(old_msg.get('msg_from_user')) + "撤回了" + str(revoke_file_type) + ": " + str(old_msg.get('msg_content')), toUserName="filehelper")

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

#点歌
def choose_song(msg, user):
    msg_content = re.match(r'(.*)点歌(.*)', msg) or re.match(r'(.*)首(.*)', msg)
    if msg_content:
        m_name = msg_content.group(2).strip()
        result = rq.get('http://47.99.180.56:3000/search?keywords=' + m_name + '&limit=1').json()['result']
        play_id = result['songs'][0]['id']
        music_name = result['songs'][0]['name']
        singer = result['songs'][0]['artists'][0]['name']
        send_msg = '【' + music_name + ' - ' + singer + '】，请快点击试听吧：' + 'https://music.163.com/m/song?id=' + str(play_id)
        itchat.send_msg(send_msg, user)
        return True
    else:
        return False

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

# 每隔五种分钟执行一次清理任务
def clear_cache():
    global rec_msg_dict
    # 当前时间
    cur_time = time.time()
    # 遍历字典，如果有创建时间超过2分钟(120s)的记录，删除，非文本的话，连文件也删除
    for key in list(rec_msg_dict.keys()):
        if int(cur_time) - int(rec_msg_dict.get(key).get('msg_create_time')) > 120:
            if not rec_msg_dict.get(key).get('msg_type') == 'Text' \
                and not rec_msg_dict.get(key).get('msg_type') == 'Sharing' \
                and not rec_msg_dict.get(key).get('msg_type') == 'Card' \
                and not rec_msg_dict.get(key).get('msg_type') == 'Map':
                file_path = os.path.join(rec_tmp_dir, rec_msg_dict.get(key).get('msg_content'))
                if os.path.exists(file_path):
                    os.remove(file_path)
            rec_msg_dict.pop(key)

def init_dog_num():
    global dog_num
    dog_num = 1

# 开始轮询任务
def start_schedule():
    sched.add_job(clear_cache, 'interval', minutes=2)
    sched.add_job(init_dog_num, 'interval', minutes=30)
    sched.add_job(morning, 'cron', hour=8)
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