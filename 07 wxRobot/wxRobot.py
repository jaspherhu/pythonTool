# -*- coding: utf-8 -*-
import time
import random
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import urllib.parse 

import os
from openai import OpenAI

# 重新定义 use_ask 内容，
# use_ask = "总结以下充电桩企业五天内的新闻：特锐德，国电南瑞，​许继集团，易事特，星星充电，科士达，超翔科技，奥特迅，南方电网，比亚迪，​​阳光电源，盛弘股份，中恒电气，和顺电气，​通合科技，英可瑞，动力源，​科陆电子，万马新能源，​泰坦科技，依威能源，华为数字能源，普天新能源，​京能新能源，驴充充，正泰电器，德力西电气，天合光能，宁德时代，汇川技术，麦格米特，思源电气，中能电气，​科大智能，长园集团，置信电气，平高电气，国轩高科，亿纬锂能，正泰安能，绿能慧充​。"
# use_ask = "分析近期充电桩产业动态信息,尤其关注以下企业：特锐德，国电南瑞，​许继集团，易事特，星星充电，科士达，超翔科技，奥特迅，南方电网，比亚迪，​​阳光电源，盛弘股份，中恒电气，和顺电气，​通合科技，英可瑞，动力源，​科陆电子，万马新能源，​泰坦科技，依威能源，华为数字能源，普天新能源，​京能新能源，驴充充，正泰电器，德力西电气，天合光能，宁德时代，汇川技术，麦格米特，思源电气，中能电气，​科大智能，长园集团，置信电气，平高电气，国轩高科，亿纬锂能，正泰安能，绿能慧充​。"
# use_ask = "总结最近期全球重大新闻。"
use_ask = ["盛弘电气", "绿能慧充", "科华", "科士达"]
# use_ask = "现在时间，最近一周内充电桩企业动态，关注以下企业：特锐德，国电南瑞，​许继集团，易事特，星星充电，科士达，奥特迅，南方电网，比亚迪，​​阳光电源，盛弘股份，中恒电气，和顺电气，​通合科技，英可瑞，​科陆电子，泰坦科技，华为数字能源，​正泰电器，宁德时代，麦格米特，中能电气，​长园集团，绿能慧充"
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
# DESCRIPTION = ""

# 构造 client
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

# 基本参数配置
apiUrl = 'http://v.juhe.cn/toutiao/index'  # 接口请求URL
apiKey = '1e5bc79f211a18215b226e3cbbdbf5c5'  # 在个人中心->我的数据,接口名称上方查看
# 企业微信机器人的发送消息-定义 markdown 内容
markdown_content = ""

def juhe_search():
    # 接口请求入参配置
    requestParams = {
        'key': apiKey,
        'type': 'top',
        'page': '20',
        'page_size': '',
        'is_filter': '',
    }
    # 发起接口网络请求
    response = requests.get(apiUrl, params=requestParams)

    # 解析响应结果
    if response.status_code == 200:
        responseResult = response.json()
        # 网络请求成功。可依据业务逻辑和接口文档说明自行处理。
        print(responseResult)
    else:
        # 网络异常等因素，解析结果异常。可依据业务逻辑自行处理。
        print('请求异常')
    return responseResult


from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
# 新增导入语句
from selenium import webdriver
# 新增导入语句
from selenium.webdriver.common.by import By

def selenium_baidu_search(keywords):
    # 配置 Edge 选项
    edge_options = EdgeOptions()
    edge_options.add_argument('--headless')  # 无头模式，不显示浏览器窗口
    # 禁用浏览器日志输出
    edge_options.add_argument('--log-level=3')
    # 忽略证书验证
    edge_options.add_argument('--ignore-certificate-errors')
    # 请根据实际情况修改 ChromeDriver 的路径
    service = EdgeService('C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedgedriver.exe')
    driver = webdriver.Edge(service=service, options=edge_options)

    max_retries = 3
    for retry in range(max_retries):
        try:
            # 生成 Markdown 格式的结果
            markdown_result = ""

            for keyword in keywords:
                # 构建百度搜索 URL
                encoded_keyword = urllib.parse.quote_plus(keyword)
                # url = f"https://news.qq.com/search?query={encoded_keyword}&page=1"
                url = f"https://www.baidu.com/s?tn=news&rtt=1&bsst=1&wd={encoded_keyword}&cl=2"
                
                # 打开搜索页面
                driver.get(url)
                time.sleep(2)

                from selenium.webdriver.support.ui import WebDriverWait
                from selenium.webdriver.support import expected_conditions as EC
                # 使用显式等待确保页面加载完成
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".result-op.c-container.xpath-log.new-pmd"))
                    )
                except Exception as e:
                    print(f"等待搜索结果加载失败: {e}")

                # 提取搜索结果，使用百度新闻搜索结果的常见选择器
                cards = driver.find_elements(By.CSS_SELECTOR, ".result-op.c-container.xpath-log.new-pmd")

                if not cards:
                    print(f"未找到关键词 {keyword} 的搜索结果，请检查选择器或网络连接。")

                # 存储结果的列表
                results = []

                for card in cards:
                    # 提取标题
                    try:
                        title_element = card.find_element(By.CSS_SELECTOR, "h3.news-title_1YtI1 a")
                        title = title_element.text
                    except Exception as e:
                        title = "未知标题"
                        print(f"提取标题失败: {e}")

                    # 提取描述
                    try:
                        description_element = card.find_element(By.CSS_SELECTOR, "div.c-span12 span.c-font-normal.c-color-text")
                        description = description_element.text
                    except Exception as e:
                        description = "未知描述"
                        print(f"提取描述失败: {e}")

                    # 提取链接
                    try:
                        link_element = card.find_element(By.CSS_SELECTOR, "h3.news-title_1YtI1 a")
                        link = link_element.get_attribute('href')
                    except Exception as e:
                        link = "未知链接"
                        print(f"提取链接失败: {e}")

                    # 提取作者
                    try:
                        author_element = card.find_element(By.CSS_SELECTOR, "div.news-source_Xj4Dv a.source-link_Ft1ov span.c-color-gray")
                        author = author_element.text
                    except Exception as e:
                        author = "未知作者"
                        print(f"提取作者失败: {e}")

                    # 提取时间
                    try:
                        time_element = card.find_element(By.CSS_SELECTOR, "span.c-color-gray2.c-font-normal.c-gap-right-xsmall")
                        time_str = time_element.text
                    except Exception as e:
                        time_str = "未知时间"
                        print(f"提取时间失败: {e}")

                    # 将结果存入字典
                    result = {
                        "title": title,
                        "description": description,
                        "link": link,
                        "author": author,
                        "time": time_str
                    }

                    results.append(result)

                for result in results:
                    markdown_result += f"# {result['title']}\n"
                    markdown_result += f"## 作者: {result['author']}\n"
                    markdown_result += f"## 时间: {result['time']}\n"
                    markdown_result += f"## 描述: {result['description']}\n"
                    markdown_result += f"## 链接: [{result['link']}]({result['link']})\n\n"

                # print(f"关键词 {keyword} 的搜索结果已保存。",results)
                
            print("搜索结果已保存。",markdown_result)
            return markdown_result

        except Exception as e:
            import traceback
            if retry < max_retries - 1:
                print(f"第 {retry + 1} 次尝试失败，将在 5 秒后重试: {e}")
                print(traceback.format_exc())
                time.sleep(5)
            else:
                print(f"所有尝试均失败: {e}")
                print(traceback.format_exc())

    # 确保 finally 语句和 try 语句正确配对
    try:
        pass  # 这里可以添加需要执行的代码，如果没有可以留空
    finally:
        driver.quit()
    return ""

# 代理 IP 地址列表 - https://www.docip.net/free
proxy_list = [
    "31.14.122.28:443"
    # "43.129.201.43:443"
    # "112.86.55.130:81",
    # "59.53.80.122:10024"
]

# 随机选择一个代理并转换为字典格式
selected_proxy = random.choice(proxy_list)
proxies = {
    "https": f"https://{selected_proxy}",
    "http": f"http://{selected_proxy}"
}

def baidu_search(keyword):
    # 对关键词进行 URL 编码
    encoded_keyword = urllib.parse.quote_plus(keyword)
    url = f"https://www.baidu.com/s?tn=news&rtt=1&bsst=1&wd={encoded_keyword}&cl=2"
    # url = f"https://cn.bing.com/search?q={use_ask}"
    # url = f"https://news.qq.com/search?query={use_ask}&page=1"
    # url = f"https://www.fy5.org/vod_search.html?wd={use_ask_test}"

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "MAWEBCUID=web_iqcUckJnVzsSEGTNIJKshQiJsGfGlCsMTgrsBrsUgTpcrEnfdL; BAIDUID=CD95B21A56CF0324402ADD9037E67859:FG=1; BD_UPN=12314753; PSTM=1742999209; BIDUPSID=CD95B21A56CF0324402ADD9037E67859; MCITY=-%3A; H_WISE_SIDS_BFESS=60273_61027_62325_62344_62484_62637_62869_62877_62881_62892_62926_62969_62966_63018_63040_63044_63039; BDUSS=3BpWXg1RlFvUEczbDZJbnpYTlk1U1BkbVRnY0hwZnMzb1NSTzVLRUM3enJnelpvSVFBQUFBJCQAAAAAAAAAAAEAAAC8UYcXamFzcGVyc3VkbwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOv2Dmjr9g5oS; BDUSS_BFESS=3BpWXg1RlFvUEczbDZJbnpYTlk1U1BkbVRnY0hwZnMzb1NSTzVLRUM3enJnelpvSVFBQUFBJCQAAAAAAAAAAAEAAAC8UYcXamFzcGVyc3VkbwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOv2Dmjr9g5oS; bce-sessionid=00192aa49415a4143dabb6415bc6c6a42f1; H_PS_PSSID=60273_61027_62325_62344_62484_62869_62877_62892_62926_62969_63018_63040_63044_63129; H_WISE_SIDS=60273_61027_62325_62344_62484_62869_62877_62892_62926_62969_63018_63040_63044_63129; ispeed_lsm=2; BA_HECTOR=2h210k8g20ag052g0hagak2l24d3be1k119gs22; BAIDUID_BFESS=CD95B21A56CF0324402ADD9037E67859:FG=1; delPer=0; BD_CK_SAM=1; PSINO=7; ZFY=OPy:A42JBJ7nrG4Ky6xly7ofOwhXDc7Zgg2j8UryfxpI:C; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; sugstore=1; BDRCVFR[C0p6oIjvx-c]=mk3SLVN4HKm; arialoadData=false; BDSVRTM=388",
        "Host": "www.baidu.com",
        "Sec-Ch-Ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Microsoft Edge\";v=\"122\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
    }

    try:
        # 发送请求--使用代理yong  proxy
        response = requests.get(url, headers=headers)
        # rresponse = requests.get(url, proxies=proxies)
        response.raise_for_status()
        # 手动指定编码
        response.encoding = response.apparent_encoding
        # 打印搜索返回状态
        # print(f"百度搜索请求状态码: {response.status_code}")
        # 打印搜索返回内容
        print(f"搜索返回内容: {response.text}")
        # 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        # 提取搜索结果的文本信息
        search_text = ""
        # 尝试多种类名匹配
        class_names = ['result c-container new-pmd', 'c-container']
        for class_name in class_names:
            results = soup.find_all('div', class_=class_name)
            for result in results:
                title = result.find('h3')
                if title:
                    search_text += title.get_text() + "\n"
                abstract = result.find('div', class_='c-abstract')
                if not abstract:
                    abstract = result.find('div', class_='c-span-last')
                if abstract:
                    search_text += abstract.get_text() + "\n\n"
        
        print(f"回复文本: {search_text}")
        return search_text
    except requests.RequestException as e:
        print(f"请求搜索失败: {e}")
        return ""

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

        return completion.choices[0].message.content
    except Exception as e:
        print(f"调用 OpenAI 失败: {e}")
        return ""


def qywxRobot_Send_Message():

    if 1:
        # search_result = baidu_search(use_ask)
        search_result = selenium_baidu_search(use_ask)
        # print("answer:", final_answer)
        final_answer = get_openai_response(f"根据搜索结果：{search_result}，请总结要点。")
    else:
        final_answer = get_openai_response(use_ask)

    # 简单转换为 Markdown 格式，添加换行符
    markdown_contents = final_answer.replace('- ', '>- ')
    # markdown_contents = final_answer
    print("ai_answer",markdown_contents)

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
    next_run = now.replace(hour=0, minute=31, second=50, microsecond=0)
    if now >= next_run:
        next_run += timedelta(days=1)
    return (next_run - now).total_seconds()

while True:
    wait_seconds = get_next_run_time()

    if 0:
        time.sleep(wait_seconds)
        qywxRobot_Send_Message()
    else:
        search_result = selenium_baidu_search(use_ask)
        print(search_result)
        time.sleep(60) 
    