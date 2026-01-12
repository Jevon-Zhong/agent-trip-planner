export type CardDataType = {
    icon: string,
    title: string,
    subtitle: string,
    prompt: string
}[]

export type EventType = {
    detail: {
        lineCount: number
    }
}

export type LoginEventType = { detail: { value: { nickname: string } } }

export type AvatarEventType = { detail: { avatarUrl: string } }

export type UserLoginType = {
    code: string
    avatar: string
    nickname: string
}

// 所有http接口返回的数据类型
export type ApiResponse<T> = {
    code: number
    msg: string
    data: T
}

// 登陆接口返回的结果数据类型
export type UserLoginResType = {
    avatar: string
    nickname: string
    access_token: string
}

// 请求对话列表数据返回的数据类型
export type ConversationListType = {
    title: string,
    created_at: string,
    thread_id: string
}[]

// 获取会话详情接口数据类型
export type AIMessageType = {
    role: 'user' | 'tool' | 'tool_result' | 'assistant' | 'end',
    content: string,
    code?: number
}

// 用户和模型的对话数据类型
export type MessageListType = {
    role: 'user' | 'tool' | 'tool_result' | 'assistant' | 'end',
    content: string,
    loading?:boolean, //发送时等待模型回复的loading
    toolThinking?:boolean, //工具返回思考开始/结束
    modelSuccess?: boolean, // 模型是否回复成功
    toolList?:string[], // 返回的工具列表
}

// 获取会话详情接口数据类型
export type createConversationType = {
    sessionId: string
}