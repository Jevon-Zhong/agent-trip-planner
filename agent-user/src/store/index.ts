import type { AIMessageType, ConversationListType, MessageListType, UserLoginResType, IncludePpointsType, ModelMapType, MapDataType, MarkersType, CardDataType, RecordStateType, TencentASRRealTimeResponse } from '@/types'
import xingzou from '@/static/xingzou.png'
import { defineStore } from 'pinia'
import { conversationDetailApi, baseWsUrl } from '@/api/request'
const baseUrl_ws = baseWsUrl
export const useAppStore = defineStore('app', {
    state: () => ({
        userInfo: null as UserLoginResType | null,
        conversationList: [] as ConversationListType,
        selectedThreadId: '',
        switchHistoryAndChat: false,
        messageList: [] as MessageListType[],//用户和模型的对话列表
        CardDataList: [] as CardDataType,//用户和模型的对话列表
        isConnected: false, //ws是否连接上
        loading: false, // 全局大loading
        cardSkeleton: false, // 快捷提问的骨架屏
        socket: null, //socket 对象
        disabledStatus: false, // 模型对话是否禁用
        isVoice: false, // 当前是否是语音输入
        recordState: {
            isRecording: false, // 是否正在录音
            isOutOfRange: false, // 触点是否超出按钮范围
            btnRect: { top: 0, left: 0, width: 0, height: 0 } // 按钮位置信息
        } as RecordStateType, // 录音状态
        // 临时存储工具列表
        toolList: [] as any,
        // 上一条是否是ai消息
        lastAssistantFlag: true,
        // 临时存储对话历史数据
        newSessionData: [] as MessageListType[],
        // 临时存储对话历史数据的工具
        historyToolList: [] as string[],
        //临时存储每一天的地图路线数据
        mapDataList: [] as MapDataType[],

        // 语音识别的socket
        socketTask: null as any,
        // 语音识别出的文字
        voiceResText: ''
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
                    // const aiMessageObj = this.messageList[this.messageList.length - 1]
                    // 如果是工具返回
                    if (modelObj.role == 'tool') {
                        // // 收到模型回复， 吧loading加载去掉
                        // aiMessageObj.toolThinking = false
                        // aiMessageObj.toolList?.push(modelObj.content)

                        // 上一条是ai消息，那就可以创建个新模板
                        if (this.lastAssistantFlag) {
                            this.messageList.push({
                                role: 'assistant',
                                content: '',
                                loading: true,
                                toolList: [],
                                toolThinking: true,
                            })
                        }
                        const aiMessageObj = this.messageList[this.messageList.length - 1]
                        // 把工具信息组装进去
                        aiMessageObj.toolList?.push(modelObj.content)
                        this.lastAssistantFlag = false
                    }
                    // 如果有工具结果返回
                    if (modelObj.role == "tool_result") {
                        const aiMessageObj = this.messageList[this.messageList.length - 1]
                        // 如果是地图数据
                        const objRes = JSON.parse(res.data);
                        console.log(objRes);
                        // jsonMap：大模型返回的值 {"points": pl, "type": "route_polyline", "day": day, "marker": markers}
                        let jsonMap: ModelMapType
                        if (typeof objRes.content.null === 'string') {
                            jsonMap = JSON.parse(objRes.content.null);
                        } else {
                            jsonMap = objRes.content.null; // 已是对象，直接使用
                        }
                        console.log('type1', typeof jsonMap === 'object')
                        console.log('type2', jsonMap)
                        console.log('type3', jsonMap.type)
                        if (jsonMap.type && jsonMap.type === "route_polyline") {
                            console.log('jsonMap', jsonMap)
                            const newMapItem = this.makeUpMap(jsonMap);
                            console.log('newMapItem', newMapItem)
                            console.log('Object.keys(newMapItem)', Object.keys(newMapItem))
                            console.log('Object.keys(newMapItem).length', Object.keys(newMapItem).length)
                            if (Object.keys(newMapItem).length > 0) {
                                if (aiMessageObj.mapDataList) {
                                    aiMessageObj.mapDataList?.push(newMapItem);
                                } else {
                                    aiMessageObj.mapDataList = [newMapItem]
                                }
                            }
                            console.log('innner_mapDataList', aiMessageObj.mapDataList)
                        }
                        console.log('mapDataList', aiMessageObj.mapDataList)
                    }
                    // 大模型返回消息
                    if (modelObj.role === 'assistant') {
                        const aiMessageObj = this.messageList[this.messageList.length - 1]
                        // // 上一条不是ai消息，并且messageList里没有插入空模板，消息列表需要新插入空消息模板
                        // if (!lastAssistantFlag && aiMessageObj.role != 'assistant') {
                        //     this.messageList.push({
                        //         role: 'assistant',
                        //         content: '',
                        //         loading: true,
                        //         toolList: [],
                        //         toolThinking: true,
                        //     })
                        //     // 把工具信息组装进去
                        //     if (this.toolList.length > 0) {
                        //         aiMessageObj.toolList = this.toolList
                        //         this.toolList = []
                        //     }
                        // }

                        // 收到模型回复， 吧loading加载去掉
                        aiMessageObj.toolThinking = false
                        aiMessageObj.loading = false
                        aiMessageObj.content += modelObj.content
                        this.lastAssistantFlag = true
                    }
                    // 如果大模型回复完毕或者出错
                    if (modelObj.role == 'end') {
                        const aiMessageObj = this.messageList[this.messageList.length - 1]
                        this.disabledStatus = false
                        // 判断状态
                        const status = modelObj.code
                        switch (status) {
                            case 200:
                                console.log('大模型回复完毕')
                                break;
                            case 401:
                                uni.navigateTo({ url: '/pages/login/index' })
                                // aiMessageObj.content = '登陆后我再回复你'
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
                        aiMessageObj.toolThinking = false
                        aiMessageObj.loading = false
                        aiMessageObj.modelSuccess = true
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


        // changeDay(parentIndex: number, childIndex: number) {
        //     const messageObj = this.messageList[parentIndex]
        //     const locationData = messageObj.locationData
        //     const points: IncludePpointsType = []
        //     // 默认展示第一天
        //     messageObj.longitude = locationData![0].location[0].longitude
        //     messageObj.latitude = locationData![0].location[0].latitude
        //     // 重制数据
        //     messageObj.markers = []
        //     messageObj.polyline = []
        //     // 地图赋值第n天数据
        //     locationData![childIndex].location.forEach((item, index) => {
        //         // includePpoints
        //         messageObj.includePpoints?.push({
        //             longitude: item.longitude,
        //             latitude: item.latitude
        //         })
        //         // 
        //         messageObj.markers?.push({
        //             id: Date.now() + index,
        //             longitude: item.longitude,
        //             latitude: item.latitude,
        //             iconPath: xingzou,
        //             width: 30,
        //             height: 30,
        //             callout: {
        //                 content: item.city,
        //                 color: '#fff',
        //                 borderRadius: 3,
        //                 borderColor: '#ff00bf',
        //                 bgColor: '#ff00bf',
        //                 padding: 3,
        //                 display: 'ALWAYS'
        //             }
        //         })
        //         points.push({
        //             longitude: item.longitude,
        //             latitude: item.latitude
        //         })
        //         messageObj.polyline = [
        //             {
        //                 points: points,
        //                 color: '#9F24D0',
        //                 width: 2
        //             }
        //         ]

        //     })

        // },

        // 根据大模型给的地图数据绘制地图
        makeUpMap(jsonMap: ModelMapType) {
            // 一天的地图数据
            let oneDayMapData: MapDataType = {}
            const points = jsonMap.points
            const markers = jsonMap.marker
            const day = jsonMap.day
            // 如果大模型没有返回坐标点就返回空对象
            if (points.length <= 0 || markers.length < 0) return {}
            // 遍历数据中的标记点组装成地图需要的结构   `   `       
            const markersData: MarkersType = []
            const includePoints: IncludePpointsType = [];
            markers.forEach(item => {
                markersData.push({
                    id: item.id,
                    longitude: item.longitude,
                    latitude: item.latitude,
                    iconPath: xingzou,
                    width: 30,
                    height: 30,
                    callout: {
                        content: item.content,
                        color: "#333",
                        fontSize: 17,
                        borderRadius: 8,
                        borderWidth: 2,
                        borderColor: "#ffffff",
                        bgColor: "#888FB6",
                        padding: 8,
                        display: 'ALWAYS'
                    }
                })
                includePoints.push({
                    longitude: item.longitude,
                    latitude: item.latitude
                })
            })
            oneDayMapData = {
                mapId: String(Date.now()),
                day: day,
                longitude: points[0].longitude,
                latitude: points[0].latitude,
                markers: markersData,
                // 途经坐标点连线
                polyline: [
                    {
                        points: points,
                        color: "#858FB9",
                        width: 6,
                        borderColor: "#2f693c",
                        borderWidth: 1,
                    },
                ],
                includePoints: includePoints
            }
            return oneDayMapData
        },

        async getContent(thread_id: string) {
            console.log('thread_id', thread_id)
            const res = await conversationDetailApi(thread_id)
            console.log(res)
            res.data.forEach((item) => {
                // 如果是用户的消息
                if (item.role === 'user') {
                    this.newSessionData.push(item)
                }
                // 如果是工具名称
                if (item.role === 'tool') {
                    this.historyToolList?.push(item.content)
                }
                // 如果是模型消息
                if (item.role === 'assistant') {
                    this.newSessionData.push(item)
                    // 处理工具名单
                    let lastObj
                    if (this.historyToolList.length > 0) {
                        lastObj = this.newSessionData[this.newSessionData.length - 1]
                        if (lastObj) {
                            lastObj.toolList = this.historyToolList
                        }
                        this.historyToolList = []
                    }
                    // 处理地图位置（与哪条消息合并）
                    if (this.mapDataList.length > 0) {
                        if (lastObj?.toolList?.includes('map_data')) {
                            lastObj.mapDataList = this.mapDataList
                        }
                    }
                }
                // 如果是工具返回结果
                if (item.role === 'tool_result') {
                    console.log('触发tool_result')
                    let jsonMap: ModelMapType
                    if (typeof item.content.null === 'string') {
                        jsonMap = JSON.parse(item.content.null);
                    } else {
                        jsonMap = item.content.null; // 已是对象，直接使用
                    }
                    // 将每一天的地图数据返回存储到mapDataList
                    if (jsonMap.type && jsonMap.type === "route_polyline") {
                        console.log('jsonMap', jsonMap)
                        const newMapItem = this.makeUpMap(jsonMap);
                        console.log('newMapItem', newMapItem)
                        console.log('Object.keys(newMapItem)', Object.keys(newMapItem))
                        console.log('Object.keys(newMapItem).length', Object.keys(newMapItem).length)
                        if (Object.keys(newMapItem).length > 0) {
                            this.mapDataList.push(newMapItem)
                            // const lastObj = newSessionData.value[newSessionData.value.length - 1]
                            // console.log('lastObj', lastObj)
                            // if (lastObj) {
                            //     if (lastObj.mapDataList) {
                            //         lastObj.mapDataList.push(newMapItem);
                            //     } else {
                            //         lastObj.mapDataList = [newMapItem]
                            //     }
                            //     console.log('lastObj.mapDataList', lastObj)
                            // }
                            // console.log('tool_result', lastObj)
                        }
                    }
                }
            })
            console.log('dddddd')
            console.log(this.newSessionData)
            console.log('dddddd')
            this.messageList = this.newSessionData
            this.selectedThreadId = thread_id
            this.historyToolList = []
            this.newSessionData = []
            this.switchHistoryAndChat = false
        },

        // 连接腾讯云语音api
        async connectASR(asrUrl: string) {
            const asrSegment: any = [] // 存放每一段文本
            this.socketTask = await wx.connectSocket({
                url: asrUrl,
                method: "GET"
            })

            // 监听收到消息
            this.socketTask.onMessage((res: any) => {
                const objRes: TencentASRRealTimeResponse = JSON.parse(res.data)
                // 握手成功
                if (objRes.code === 0) {
                    // 语音返回结果
                    if (objRes.result && objRes.result.voice_text_str) {
                        const index: number = objRes.result.index
                        const text: string = objRes.result.voice_text_str
                        const sliceType: number = objRes.result.slice_type

                        // 初始化该index段
                        if (!asrSegment[index]) {
                            asrSegment[index] = ""
                        }
                        // 段话开始识别。
                        if (sliceType === 0) {
                            asrSegment[index] = text
                        }
                        // 一段话识别中，voice_text_str 为非稳态结果（该段识别结果还可能变化）
                        if (sliceType === 1) {
                            asrSegment[index] = text;
                        }
                        // 一段话识别结束，voice_text_str 为稳态结果（该段识别结果不再变化）
                        if (sliceType === 2) {
                            asrSegment[index] = text
                        }
                        // 拼接完整语音
                        this.voiceResText = asrSegment.filter(Boolean).join("")
                        console.log('voiceResText', this.voiceResText)
                    }
                } else if (objRes.code === 4008) {
                    uni.showToast({
                        icon: "none",
                        title: "没有听到你说话",
                    });
                } else {

                    uni.showToast({
                        icon: "none",
                        title: "连接失败",
                    });
                }
            })

            // 连接成功
            this.socketTask.onOpen(() => {
                console.log("websocket连接上voice");
            })
            // 连接关闭
            this.socketTask.onClose(() => {
                console.log("连接关闭voice");
            });
            // 连接错误
            this.socketTask.onError((err: any) => {
                console.log("连接错误voice:", err);
            });
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