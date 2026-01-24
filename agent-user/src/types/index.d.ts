export type CardDataType = {
    icon: string,
    title: string,
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
    content: any
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
    mapDataList?: MapDataType[];
}

export type MapDataType = {
  day?: string; //第几天
  mapId?: string; //地图id
  longitude?: number; //经度
  latitude?: number; //纬度
  markers?: MarkersType; // 用于在地图上显示标记的位置
  polyline?: PolylineType; // 坐标点连线
  includePoints?: IncludePointsType; // 缩放视野以包含所有给定的坐标点
  mapLoading?: boolean; //地图数据是否请求成功
  locationData?: LocationDataType; // 存储地图路线经纬度数据
};

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
    borderColor: string
    borderWidth: number
    color: string
    width: number
}[]

type CalloutType = {
    content: string
    fontSize: number;
    borderWidth: number;
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

// 模型返回的地图数据结构
export type ModelMapType = {
  points: {
    latitude: number;
    longitude: number;
  }[];
  type: string;
  day: string;
  marker: {
    id: number; // id表示对应每个景点的id，随机数生成不重复，可使用时间戳，数字类型
    latitude: number;
    longitude: number;
    content: string; //景点名称
  }[];
};