# -*- coding: utf-8 -*-
import time
import requests
import json
from datetime import datetime, timedelta

# from http import HTTPStatus
# import dashscope

import os
from openai import OpenAI

# 重新定义 use_ask 内容，
# use_ask = "总结以下充电桩企业五天内的新闻：特锐德，国电南瑞，​许继集团，易事特，星星充电，科士达，超翔科技，奥特迅，南方电网，比亚迪，​​阳光电源，盛弘股份，中恒电气，和顺电气，​通合科技，英可瑞，动力源，​科陆电子，万马新能源，​泰坦科技，依威能源，华为数字能源，普天新能源，​京能新能源，驴充充，正泰电器，德力西电气，天合光能，宁德时代，汇川技术，麦格米特，思源电气，中能电气，​科大智能，长园集团，置信电气，平高电气，国轩高科，亿纬锂能，正泰安能，绿能慧充​。"
# use_ask = "分析近期充电桩产业动态信息,尤其关注以下企业：特锐德，国电南瑞，​许继集团，易事特，星星充电，科士达，超翔科技，奥特迅，南方电网，比亚迪，​​阳光电源，盛弘股份，中恒电气，和顺电气，​通合科技，英可瑞，动力源，​科陆电子，万马新能源，​泰坦科技，依威能源，华为数字能源，普天新能源，​京能新能源，驴充充，正泰电器，德力西电气，天合光能，宁德时代，汇川技术，麦格米特，思源电气，中能电气，​科大智能，长园集团，置信电气，平高电气，国轩高科，亿纬锂能，正泰安能，绿能慧充​。"
# use_ask = "总结最近期全球重大新闻。"
use_ask = "现在时间，和最近一周内充电桩企业动态，关注以下企业：特锐德，国电南瑞，​许继集团，易事特，星星充电，科士达，奥特迅，南方电网，比亚迪，​​阳光电源，盛弘股份，中恒电气，和顺电气，​通合科技，英可瑞，​科陆电子，泰坦科技，华为数字能源，​正泰电器，宁德时代，麦格米特，中能电气，​长园集团，绿能慧充"
# use_ask = "汇总最近十天内充电桩的行业动态详细信息，重点关注下：星星充电，科士达，比亚迪，​​阳光电源，盛弘股份，中恒电气，和顺电气，​通合科技，英可瑞，​科陆电子，​泰坦科技，华为数字能源，正泰电器，宁德时代，麦格米特，​科大智能，长园集团，绿能慧充​。"

# 定义腾讯TX的 API 密钥和基础 URL
AI_MODEL = "hunyuan-turbos-latest" 
# AI_MODEL = "hunyuan-t1-latest"    # -web-search
API_KEY = "sk-CSq5yl2g1WLxYxYmvfPn5ISabgyLjTAij9ktDkiBy6drdQjP"
BASE_URL = "https://api.hunyuan.cloud.tencent.com/v1"

# 定义阿里ALI的 API 密钥和基础 URL
AI_MODEL_ALI = "qwen-plus"
API_KEY_ALI = "sk-9c28c47c313146aa93f6918cb02fd376"
BASE_URL_ALI = "https://dashscope.aliyuncs.com/compatible-mode/v1"

# 微信机器人的 webhook 地址
WEBHOOK_URL = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=2f80fbaf-74d7-42b1-97bd-96269a381f74'
# 全局定义 description
DESCRIPTION = ""

# 构造 client
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

# 企业微信机器人的发送消息-定义 markdown 内容
markdown_content = ""

# 封装调用 OpenAI 发送消息的函数
def get_openai_response(content):
    try:
        completion = client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": content
                }
            ],
            extra_body={
                "enable_enhancement": True,  # <- 自定义参数
                "EnableEnhancement": True,
                # "enable_deep_search": True,  # <- 自定义参数
                "EnableDeepSearch": True,  # <- 自定义参数
                # "enable_multimedia": True,  # <- 自定义参数
                "EnableDeepReading": True  # <- 自定义参数
            },
        )
        print(completion.choices[0].message.content)
        return completion.choices[0].message.content
    except Exception as e:
        print(f"调用 OpenAI 失败: {e}")
        return ""
def qywxRobot_Send_Message():
    markdown_content = get_openai_response(use_ask)
    # 简单转换为 Markdown 格式，添加换行符
    markdown_contents = markdown_content.replace('- ', '>- ')
    print(markdown_contents)

    # 要发送的消息内容，这里以文本消息为例
    message = {
        "msgtype": "markdown",
        "markdown": {
            "content": markdown_contents
        }
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        # 发送 POST 请求
        response = requests.post(WEBHOOK_URL, data=json.dumps(message), headers=headers)
        response.raise_for_status()
        print("消息发送成功")
    except requests.RequestException as e:
        print(f"消息发送失败: {e}")

def get_next_run_time():
    now = datetime.now()
    next_run = now.replace(hour=9, minute=24, second=0, microsecond=0)
    if now >= next_run:
        next_run += timedelta(days=1)
    return (next_run - now).total_seconds()

while True:
    wait_seconds = get_next_run_time()
    # time.sleep(wait_seconds)
    # qywxRobot_Send_Message()

    
    markdown_content = get_openai_response(use_ask)
    time.sleep(60)