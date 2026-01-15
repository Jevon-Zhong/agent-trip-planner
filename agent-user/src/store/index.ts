import type { AIMessageType, ConversationListType, MessageListType, UserLoginResType, IncludePpointsType } from '@/types'
import xingzou from '@/static/xingzou.png'
import { defineStore } from 'pinia'
const baseUrl_ws = 'ws://127.0.0.1:8000'
export const useAppStore = defineStore('app', {
    state: () => ({
        userInfo: null as UserLoginResType | null,
        conversationList: [] as ConversationListType,
        selectedThreadId: '',
        switchHistoryAndChat: false,
        messageList: [] as MessageListType[],//用户和模型的对话列表
        isConnected: false, //ws是否连接上
        socket: null, //socket 对象
        disabledStatus: false, // 模型对话是否禁用
    }),
    getters: {

    },
    actions: {
        userLogin(userInfo: UserLoginResType) {
            this.userInfo = userInfo
        },
        // 连接WebSocket服务器  
        async connectWebSocket() {
            if (!this.isConnected) {
                this.socket = await uni.connectSocket({
                    url: `${baseUrl_ws}/chat/send_message`, // 替换为你的WebSocket服务器URL  
                    header: {
                        "content-type": "application/json",
                        "Authorization": this.userInfo?.access_token
                    },
                });

                uni.onSocketOpen(res => {
                    console.log('WebSocket连接已打开！');
                    this.isConnected = true;
                });

                uni.onSocketMessage(res => {
                    console.log('收到WebSocket服务器消息：', res.data);
                    const modelObj = JSON.parse(res.data) as AIMessageType
                    //取对话最后一项,即之前预填的ai信息
                    const aiMessageObj = this.messageList[this.messageList.length - 1]
                    // 如果是工具返回
                    if (modelObj.role == 'tool') {
                        // 收到模型回复， 吧loading加载去掉
                        aiMessageObj.toolThinking = false
                        aiMessageObj.toolList?.push(modelObj.content)
                    }
                    // 大模型返回消息
                    if (modelObj.role === 'assistant') {
                        // 收到模型回复， 吧loading加载去掉
                        aiMessageObj.toolThinking = false
                        aiMessageObj.loading = false
                        aiMessageObj.content += modelObj.content
                    }
                    // 如果大模型回复完毕或者出错
                    if (modelObj.role == 'end') {
                        aiMessageObj.toolThinking = false
                        aiMessageObj.loading = false
                        aiMessageObj.modelSuccess = true
                        this.disabledStatus = false
                        // 判断状态
                        const status = modelObj.code
                        switch (status) {
                            case 200:
                                console.log('大模型回复完毕')
                                break;
                            case 401:
                                uni.navigateTo({ url: '/pages/login/index' })
                                aiMessageObj.content = '登陆后我再回复你'
                                break;
                            case 422:
                                uni.showToast({ icon: 'none', title: '请求参数不对' })
                                aiMessageObj.content = '请求参数不对'
                                break;
                            case 500:
                                uni.showToast({ icon: 'none', title: '服务器异常' })
                                aiMessageObj.content = '服务器异常'
                                break;
                        }
                    }
                });

                uni.onSocketClose(res => {
                    console.log('WebSocket连接已关闭！');
                    this.isConnected = false;
                });

                uni.onSocketError(err => {
                    console.error('WebSocket连接打开失败，请检查：', err);
                });
            }
        },

        // 发送WebSocket消息  
        sendWebSocketMessage(sessionId: string, content: string) {
            if (this.socket && this.isConnected) {
                uni.sendSocketMessage({
                    data: JSON.stringify({
                        sessionId: sessionId,
                        content: content
                    }),
                    success: () => {
                        console.log('发送成功')
                    },
                    fail: (err: any) => {
                        console.log('发送失败' + err)
                    }
                });
            } else {
                console.error('WebSocket未连接或未打开，请先连接WebSocket！');
            }
        },

        // parentIndex: 父组件传过来的index
        // childIndex: 第几天对应的数据
        // 切换第几天
        changeDay(parentIndex: number, childIndex: number) {
            const messageObj = this.messageList[parentIndex]
            const locationData = messageObj.locationData
            const points: IncludePpointsType = []
            // 默认展示第一天
            messageObj.longitude = locationData![0].location[0].longitude
            messageObj.latitude = locationData![0].location[0].latitude
            // 重制数据
            messageObj.markers = []
            messageObj.polyline = []
            // 地图赋值第n天数据
            locationData![childIndex].location.forEach((item, index) => {
                // includePpoints
                messageObj.includePpoints?.push({
                    longitude: item.longitude,
                    latitude: item.latitude
                })
                // 
                messageObj.markers?.push({
                    id: Date.now() + index,
                    longitude: item.longitude,
                    latitude: item.latitude,
                    iconPath: xingzou,
                    width: 30,
                    height: 30,
                    callout: {
                        content: item.city,
                        color: '#fff',
                        borderRadius: 3,
                        borderColor: '#ff00bf',
                        bgColor: '#ff00bf',
                        padding: 3,
                        display: 'ALWAYS'
                    }
                })
                points.push({
                    longitude: item.longitude,
                    latitude: item.latitude
                })
                messageObj.polyline = [
                    {
                        points: points,
                        color: '#9F24D0',
                        width: 2
                    }
                ]

            })

        }
    },
    persist: {
        key: 'app_store',
        // 2. 自定义存储方式（UniApp 推荐用 uniStorage，兼容多端）
        storage: {
            // 读取数据
            getItem: (key: string) => uni.getStorageSync(key),
            // 存储数据
            setItem: (key: string, value: string) => uni.setStorageSync(key, value)
        },
        pick: ['userInfo', 'conversationList', 'selectedThreadId', 'messageList']
    }
}
)