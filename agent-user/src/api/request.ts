import type { AIMessageType, ApiResponse, CardDataType, ConversationListType, createConversationType, LocationDataType, TencentASRRealTimeResponse, UserLoginResType, UserLoginType } from "@/types"
import { useAppStore } from '@/store/index'
// 公共域名
const baseUrl = 'http://172.20.10.2:8000'

// 图片上传（头像）
export const uploadImageApi = (url: string) => {
    return new Promise((resolve, reject) => {
        uni.uploadFile({
            url: `${baseUrl}/user/upload_image`,
            filePath: url,
            name: 'file',
            success: (res) => {
                resolve(JSON.parse(res.data).data.upload_image_url)
            },
            fail: (err) => {
                reject(err)
            }
        })
    })
}

// 音频上传
export const uploadAudioApi = (url: string) => {
    return new Promise((resolve, reject) => {
        uni.uploadFile({
            url: `${baseUrl}/chat/single_audio_recognize`,
            filePath: url,
            name: 'audio_file',
            success: (res) => {
                resolve(res)
            },
            fail: (err) => {
                reject(err)
            }
        })
    })
}

// 公用网络请求
const request = <T>(url: string, method: 'GET' | 'POST' | 'DELETE', data?: any): Promise<T> => {
    const appStore = useAppStore()
    return new Promise((resolve, reject) => {
        uni.request({
            url: baseUrl + url,
            method,
            data,
            header: { Authorization: "Bearer " + appStore.userInfo?.access_token },
            success: (res) => {
                const status = res.statusCode
                switch (status) {
                    case 200:
                        resolve(res.data as T)
                        break
                    case 404:
                        console.error('404')
                        reject('404')
                        break
                    case 401:
                        console.error('401')
                        reject('401')
                        uni.navigateTo({ url: '/pages/login/index' })
                        break
                    case 400:
                    case 422:
                        console.error(res.data)
                        reject('400 | 422')
                        uni.showToast({
                            title: '参数不对',
                            icon: 'none'
                        })
                        break
                    case 500:
                    case 501:
                    case 502:
                    case 503:
                        console.error('服务器发生错误')
                        reject('服务器发生错误')
                        uni.showToast({
                            title: '服务器发生错误',
                            icon: 'none'
                        })
                        break

                }
            },
            fail: (err) => {
                uni.showToast({
                    title: '出现异常',
                    icon: 'none'
                })
            }
        })
    })
}

// websocket发送消息
export const sendMessageApi = async (userMessage: string) => {
    const appStore = useAppStore()
    if (userMessage.trim() === '') {
        uni.showToast({
            icon: 'none',
            title: '请输入内容'
        })
        return
    }
    appStore.disabledStatus = true
    // 会话id为空就创建会话id
    if (appStore.selectedThreadId === '') {
        const res = await createConversationApi()
        appStore.selectedThreadId = res.data.sessionId
        // 新对话插入对话列表最顶部（头部）
        appStore.conversationList.unshift({ title: userMessage.trim(), created_at: '', thread_id: appStore.selectedThreadId })
    }
    // 新增对话详情
    appStore.messageList.push(
        {
            role: 'user',
            content: userMessage.trim()
        },
        {
            role: 'assistant',
            content: '',
            loading: true,
            toolList: [],
            toolThinking: true,
        }
    )
    appStore.sendWebSocketMessage(appStore.selectedThreadId, userMessage.trim())
}

// 登陆接口
export const userLoginApi = (params: UserLoginType): Promise<ApiResponse<UserLoginResType>> => {
    return request('/user/login', 'POST', params)
}

// 获取对话列表数据
export const conversationListApi = (): Promise<ApiResponse<ConversationListType>> => {
    return request('/chat/all_conversation_list', 'GET')
}

// 获取对话详情数据
export const conversationDetailApi = (thread_id: string): Promise<ApiResponse<AIMessageType[]>> => {
    return request(`/chat/get_conversation_detail/${thread_id}`, 'GET')
}

// 创建会话id
export const createConversationApi = (): Promise<ApiResponse<createConversationType>> => {
    return request(`/chat/create_conversation`, 'GET')
}

// 获取经纬度数据
export const getLoacationDataApi = (params: { content: string }): Promise<ApiResponse<LocationDataType>> => {
    return request(`/chat/get_location_data`, 'POST', params)
}

// 删除会话
export const deleteConversationApi = (thread_id: string): Promise<ApiResponse<[]>> => {
    return request(`/chat/delete_conversation/${thread_id}`, 'DELETE')
}

// 获取快捷提问
export const getQuickQuestionApi = (): Promise<ApiResponse<CardDataType>> => {
    return request(`/chat/get_quick_question`, 'POST')
}

// 获取腾讯云语音URL
export const getAsrUrlApi = (): Promise<ApiResponse<string>> => {
    return request(`/chat/get_asr_ws_url`, 'GET')
}
