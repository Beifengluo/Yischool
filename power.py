import requests
import json

# 定义文件名
json_file = "surplus_value.json"

# 尝试读取 JSON 文件，如果文件不存在，则创建一个初始的 JSON 文件
try:
    with open(json_file, "r") as f:
        data = json.load(f)
except FileNotFoundError:
    data = {"previous_surplus_value": None}

url = 'https://application.xiaofubao.com/app/electric/queryISIMSRoomSurplus'
headers = {
    'Cookie': '',   #自行抓包"application.xiaofubao.com"域名下的请求头
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.38(0x1800262c) NetType/4G Language/zh_CN',
}

request_data = {		#以下参数自行抓包"application.xiaofubao.com"域名下的请求体
    'areaId': '',
    'buildingCode': '',
    'floorCode': '',
    'roomCode': '',
}

response = requests.post(url, headers=headers, data=request_data)
response_data = json.loads(response.text)

# 提取 "surplus" 值
surplus_value = response_data['data']['surplusList'][0]['surplus']
print("电量剩余:", surplus_value, "度")

# 计算两次运行之间的差值
previous_surplus_value = data["previous_surplus_value"]
if previous_surplus_value is not None:
    difference = previous_surplus_value - surplus_value
        # 使用 round() 函数保留两位小数
    difference = round(difference, 2)
    print("与上次运行相比，电量差值:", difference, "度")

    # 合并两条消息为一个字符串
    message = f"电量剩余{surplus_value}度，与上次运行相比，电量差值:{difference}度"
else:
    # 如果是第一次运行，只推送电量剩余
    message = f"电量剩余{surplus_value}度"

# 更新 JSON 文件中的数据
data["previous_surplus_value"] = surplus_value
with open(json_file, "w") as f:
    json.dump(data, f)

# 定义WXPusher的API URL和消息数据
wxpusher_api_url = 'https://wxpusher.zjiecode.com/api/send/message'
app_token = ''  # 替换为您的应用密钥
uid = ''  # 替换为您的用户ID

# 发送推送消息到 wxpusher
try:
    message_data = {
        "appToken": app_token,
        "content": message,
        "contentType": 1,  # 文本类型
        "topicIds": [],
        "uids": [uid],
    }
    response = requests.post(wxpusher_api_url, json=message_data)
    response_data = response.json()
    if response_data.get('code') == 1000:
        print('消息发送成功')
    else:
        print('消息发送失败，错误信息:', response_data.get('msg'))
except Exception as e:
    print('发送消息时出现异常:', str(e))
