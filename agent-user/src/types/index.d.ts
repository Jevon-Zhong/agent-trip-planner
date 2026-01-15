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
    title: string
    created_at: string
    thread_id: string
}[]

// 获取会话详情接口数据类型
export type AIMessageType = {
    role: 'user' | 'tool' | 'tool_result' | 'assistant' | 'end',
    content: string
    code?: number
}

// 用户和模型的对话数据类型
export type MessageListType = {
    role: 'user' | 'tool' | 'tool_result' | 'assistant' | 'end',
    content: string
    loading?: boolean //发送时等待模型回复的loading
    toolThinking?: boolean //工具返回思考开始/结束
    modelSuccess?: boolean // 模型是否回复成功（用于地图展示）
    toolList?: string[] // 返回的工具列表
    //地图展示
    mapId?: string //地图id
    longitude?: number //经度
    latitude?: number //维度
    markers?: MarkersType //标记点
    polyline?: PolylineType //坐标点连线
    includePpoints?: IncludePpointsType //缩放视野以包含所有给定的坐标点
    mapLoading?: boolean //地图数据是否请求成功
    locationData?: LocationDataType //存储地图路线经纬度数据
}

// markers 类型
export type MarkersType = {
    id: number
    longitude: number
    latitude: number
    iconPath: string
    width: number
    height: number
    callout: CalloutType
}[]

// polyline类型
export type PolylineType = {
    points: { latitude: number, longitude: number }[]
    color: string
    width: number
}[]

type CalloutType = {
    content: string
    color: string
    borderRadius: number
    borderColor: string
    bgColor: string
    padding: number
    display: string
}

type IncludePpointsType = {
    latitude: number
    longitude: number
}[]

// 存储地图路线经纬度数据
export type LocationDataType = {
    day: string
    location: {
        city: string
        latitude: number
        longitude: number
    }[]
}[]


// 获取会话详情接口数据类型
export type createConversationType = {
    sessionId: string
}