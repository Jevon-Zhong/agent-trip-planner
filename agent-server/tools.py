import os

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

load_dotenv()

# 读取环境变量
API_KEY = os.getenv("API_KEY")

client = MultiServerMCPClient(
    {
        # 联网搜索
        "web_search": {
            "url": "https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/sse",
            "headers": {"Authorization": f"Bearer {API_KEY}"},
            "transport": "sse"
        },
        # 高德地图
        "amap_maps": {
            "url": "https://dashscope.aliyuncs.com/api/v1/mcps/amap-maps/sse",
            "headers": {"Authorization": f"Bearer {API_KEY}"},
            "transport": "sse"
        },
        # 12306
        "china_railway": {
            "url": "https://dashscope.aliyuncs.com/api/v1/mcps/china-railway/sse",
            "headers": {"Authorization": f"Bearer {API_KEY}"},
            "transport": "sse"
        },
    }
)
