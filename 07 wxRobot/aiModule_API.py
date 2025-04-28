import os
from openai import OpenAI

# 构造 client
client = OpenAI(
    # api_key=os.environ.get("HUNYUAN_API_KEY"),  # 混元 APIKey
    api_key="sk-CSq5yl2g1WLxYxYmvfPn5ISabgyLjTAij9ktDkiBy6drdQjP",  # 混元 APIKey
    base_url="https://api.hunyuan.cloud.tencent.com/v1",  # 混元 endpoint
)

# 重新定义 content 内容
content = "总结最近三天国内外关于新能源充电机的行业动态信息。"

completion = client.chat.completions.create(
    model="hunyuan-turbos-latest",
    messages=[
        {
            "role": "user",
            "content": content
        }
    ],
    extra_body={
        "enable_enhancement": True,  # <- 自定义参数
        # "enable_deep_search": True,  # <- 自定义参数
        # "enable_multimedia": True,  # <- 自定义参数
    },
)
print(completion.choices[0].message.content)