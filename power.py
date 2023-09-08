import requests
import json

url = 'https://application.xiaofubao.com/app/electric/queryISIMSRoomSurplus'
headers = {
    'Cookie': '',   #自行抓包"application.xiaofubao.com"域名下的请求头
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.38(0x1800262c) NetType/4G Language/zh_CN',
}

data = {
    'areaId': '',   #以下参数自行抓包"application.xiaofubao.com"域名下的请求体
    'buildingCode': '',
    'floorCode': '',
    'roomCode': '',
}

response = requests.post(url, headers=headers, data=data)
response_data = json.loads(response.text)

# 提取 "surplus" 值
surplus_value = response_data['data']['surplusList'][0]['surplus']
print("电量剩余:", surplus_value,"度")

#对接WXPUSHER
# 定义WXPusher的API URL和消息数据
wxpusher_api_url = 'https://wxpusher.zjiecode.com/api/send/message'
app_token = ''  # 替换为您的应用密钥
uid = ''  # 替换为您的用户ID
content = f'电费剩余{surplus_value}度'

# 创建消息数据
message_data = {
    "appToken": app_token,
    "content": content,
    "contentType": 1,  # 文本消息
    "topicIds": [],
    "uids": [uid],
}

# 发送消息到WXPusher
try:
    response = requests.post(wxpusher_api_url, json=message_data)
    response_data = response.json()
    if response_data.get('code') == 1000:
        print('消息发送成功')
    else:
        print('消息发送失败，错误信息:', response_data.get('msg'))
except Exception as e:
    print('发送消息时出现异常:', str(e))