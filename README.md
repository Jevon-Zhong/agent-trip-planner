# ✈️ AI智能旅行规划助手
这是一个前端基于Uniapp、Vue3、TS、Pinia、uview-plus、Websocket，后端基于Python、FastAPI、PostgreSQL等框架及语言并结合LangGraph、LangChain大模型框架以及阿里云百炼MCP、腾讯地图、腾讯云语音识别等技术实现的AI智能旅行规划助手。

能根据用户的关于旅行规划方面的提问（例如旅行攻略、天气预报、高铁车票等）进行阿里百炼MCP工具调用最后结合大模型的总结能力为用户提供一份详细周全的攻略和回答。若用户提问的是某地的旅游攻略，智能助手还会自动生成腾讯地图路线规划，同时智能助手引入了腾讯云语音识别能力，用户可切换语音输入方式来对智能助手进行提问，从而获得更便捷的使用体验。



## ✨ 主要功能

### 🔐 登陆退出

- 登陆/点击头像退出账号
- 新用户自动注册
- 保留和区分每个账号的对话记录

<div align="center">
    <img src="https://github.com/Jevon-Zhong/agent-trip-planner/blob/main/images/%E7%99%BB%E9%99%86.png?raw=true" width="250"/>
    <img src="https://github.com/Jevon-Zhong/agent-trip-planner/blob/main/images/%E9%80%80%E5%87%BA.png?raw=true" width="250"/>
</div>



### 💬 流式输出回复

- 基于Websocket流式输出回复问题
- MD格式展示
- 模板式输出，图文并茂，内容详尽
- 工具调用列表展示
- 自动生成腾讯地图路线规划
- 骨架屏优化体验
- 发送消息自动滚动到底部

<div align="center">  <img src="https://github.com/Jevon-Zhong/agent-trip-planner/blob/main/images/%E5%9B%BE%E6%96%87%E5%B9%B6%E8%8C%82.png?raw=true" width="250"/>
  	<img src="https://github.com/Jevon-Zhong/agent-trip-planner/blob/main/images/%E5%9C%B0%E5%9B%BE.png?raw=true" width="250"/>
    <img src="https://github.com/Jevon-Zhong/agent-trip-planner/blob/main/images/%E6%B5%81%E5%BC%8F%E8%BE%93%E5%87%BA.gif?raw=true" width="250"/></div>

### 🗂️ 历史对话管理

- 点击对话item显示历史对话内容

- 点击按钮创建新对话
- 左滑item点击删除对话

<img src="https://github.com/Jevon-Zhong/agent-trip-planner/blob/main/images/%E5%8E%86%E5%8F%B2%E5%AF%B9%E8%AF%9D%E7%AE%A1%E7%90%86.png?raw=true" alt="历史对话管理" style="zoom: 50%;" />



### 🌈 新对话页面提问推荐卡片

- 新建对话页面根据历史提问生成用户可能感兴趣的提问
- 点击"换一换"调用大模型生成新的推荐提问
- 点击提问推荐卡片，快速问答

<div align="center">
    <img src="https://github.com/Jevon-Zhong/agent-trip-planner/blob/main/images/%E6%96%B0%E5%AF%B9%E8%AF%9D.png?raw=true" width="250"/>
    <img src="https://github.com/Jevon-Zhong/agent-trip-planner/blob/main/images/%E6%96%B0%E5%AF%B9%E8%AF%9D.gif?raw=true" width="250"/>
  	<img src="https://github.com/Jevon-Zhong/agent-trip-planner/blob/main/images/%E5%BF%AB%E9%80%9F%E6%8F%90%E9%97%AE.gif?raw=true" width="250"/>
</div>



### 🎤 实时语音识别

- 点击输入框右侧语音/键盘按钮切换语音/键盘输入
- 长按进行语音输入+松手发送消息
- 长按+移出按钮范围+松手取消本次语音

<div align="center">
    <img src="https://github.com/Jevon-Zhong/agent-trip-planner/blob/main/images/%E8%AF%AD%E9%9F%B3.png?raw=true" width="250"/>
    <img src="https://github.com/Jevon-Zhong/agent-trip-planner/blob/main/images/%E6%9D%BE%E6%89%8B%E5%8F%96%E6%B6%88.png?raw=true" width="250"/>
  	<img src="https://github.com/Jevon-Zhong/agent-trip-planner/blob/main/images/%E8%AF%AD%E9%9F%B3.gif?raw=true" width="250"/>
</div>



## 🛠️ 技术架构

- **前端**：Uniapp、Vue3、TS、Pinia、uview-plus、Websocket
- **后端**：Python + FastAPI
- **数据库**：PostgreSQL
- **大模型开发框架**：LangGraph、L angChain
- **MCP服务来源**：阿里云百炼MCP广场
- **大模型**：通义千问系列，本系统使用qwen3-max



## 🕹️ 运行环境

- **Node.Js**：v20.18.0
- **Python**：3.12.12
- **PostgreSQL**：14.18
- **UV**：0.9.18 



## 🚀 项目运行

### 目录介绍

- **agent-user**：项目前端（uniapp微信小程序）
- **agent-server**：项目后端



### 使用的IDE

- **前端**：微信开发者工具、VSCode
- **后端**：PyCharm
- **数据库**：pgAdmin 4



### 项目运行准备

- 安装uv
- 安装PostgreSQL
- 安装pnpm
- 注册微信开发者，获取自己的小程序ID和小程序密钥
- 获取自己的自己的通义千问api key并开通相应的大模型使用权限，本系统使用的qwen3-max
- 获取自己的腾讯地图key并开通驾车路线规划服务
- 获取自己的腾讯云APPID、SECRET_ID、SECRET_KEY，并开通实时语音识别服务



### 运行项目

1. **克隆项目**

   ```bash
   git clone https://github.com/Jevon-Zhong/agent-trip-planner.git
   cd agent-trip-planner
   ```

   

2. **运行agent-server**

   在agent-server根目录创建.env文件，然后粘贴以下代码块内容，并修改以下字段

   1. **DB_USER**：安装的PostgreSQL用户名称
   2. **DB_PASSWORD**：安装的PostgreSQL用户密码
   3. **APPID**：微信开放平台查看自己的APPID https://mp.weixin.qq.com/wxamp/devprofile/get_profile
   4. **SECRET**：微信开放平台查看自己的小程序密钥,链接同上
   5. **API_KEY**：自己的通义千问api key
   6. **QQ_MAP_KEY**：自己的腾讯地图key https://lbs.qq.com/dev/console/application/mine
   7. **DB_URI**：需要填充其中的数据库用户名称，同上面的DB_USER
   8. **TENCENT_APPID**：自己的腾讯云APPID https://console.cloud.tencent.com/cam/capi
   9. **TENCENT_SECRET_ID**：自己的腾讯云SECRET_ID
   10. **TENCENT_SECRET_KEY**：自己的腾讯云SECRET_KEY

   ```bash
   # 数据库账号密钥
   DB_USER=安装的PostgreSQL用户名称
   DB_PASSWORD=安装的PostgreSQL用户密码
   DB_HOST=127.0.0.1
   DB_PORT=5432
   DB_NAME=agent
   
   # 小程序账号密钥
   APPID=自己的小程序ID
   SECRET=自己的小程序密钥
   
   # 身份认证jwt
   SECRET_KEY=agent123
   # 加密算法
   ALGORITHM=HS256
   # 过期时间
   TOKEN_EXPIRE=120
   
   # 通义千问api key
   API_KEY=自己的通义千问api key
   
   # 腾讯地图key，获取链接：https://lbs.qq.com/dev/console/application/mine
   QQ_MAP_KEY=自己的腾讯地图key
   
   # langgraph的数据库连接
   DB_URI = "postgresql://数据库用户名称:root@localhost:5432/agent?sslmode=disable"
   
   # mcp提供的appcode服务器密钥，固定是这个不变
   APPCODE=sk-fhfytuudhgryomk9098
   
   # 腾讯云appid，密钥，获取链接：https://console.cloud.tencent.com/cam/capi
   TENCENT_APPID=自己的腾讯云APPID
   TENCENT_SECRET_ID=自己的腾讯云SECRET_ID
   TENCENT_SECRET_KEY=自己的腾讯云SECRET_KEY
   
   HOST=127.0.0.1
   PORT=8000
   
   MODEL=qwen3-max
   ```

   接着安装虚拟环境和相关依赖来启动项目

   ```bash
   cd agent-server
   uv sync
   uv run main.py
   ```

   此时后端启动成功

   

3. **运行agent-user**

   安装前端依赖

   ```
   cd agent-user
   pnpm i
   ```

   替换小程序ID，src/manifest.json 下

   ```json
   /* 小程序特有相关 */
       "mp-weixin" : {
           "appid" : "写自己的APPID",
           "setting" : {
               "urlCheck" : false
           },
           "usingComponents" : true,
           "mergeVirtualHostAttributes" : true
       },
   ```

   运行前端

   ```bash
   pnpm run dev:mp-weixin
   ```

   将运行后的dist/dev/mp-weixin 这层目录在微信开发者工具中导入创建即可在微信开发者工具中运行和预览

​		

### 注意事项

- 可修改后端.env文件的HOST为本机IP或者WIFI的IP地址同时设置前端request.ts文件的baseUrl和baseWsUrl为后端修改的IP后即可通过预览或者真机模拟来在手机上运行测试本项目
- 后端.env文件的MODEL可修改为其他大模型，但是个人测试还是觉得qwen3-max最好用，它的处理文本和工具调用能力比较不容易出错



## 🔑 **License**

本项目采用 [MIT License](https://github.com/JustForSO/Sentra-Agent/blob/main/LICENSE) 开源协议。

你可以自由地使用、修改、分发本项目，但是禁止商业化。



## 📩 联系我

- **QQ**：1035684305









