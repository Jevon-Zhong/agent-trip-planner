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

export type RecordStateType = {
    isRecording: boolean, // 是否正在录音
    isOutOfRange: boolean, // 触点是否超出按钮范围
    btnRect: { top: number, left: number, width: number, height: number } // 按钮位置信息
}

/**
 * 腾讯云实时语音识别 响应根类型（使用 type 定义）
 */
export type TencentASRRealTimeResponse = {
  /** 状态码：0 表示成功（其他值可参考腾讯云文档对应错误码） */
  code: number;
  /** 响应消息：success 表示成功，失败时返回具体错误信息 */
  message: string;
  /** 语音唯一标识 ID，用于追踪该段语音的识别流程 */
  voice_id: string;
  /** 消息唯一标识 ID，用于追踪单条识别结果的分片（格式通常为 语音ID_分片_索引） */
  message_id: string;
  /** 核心识别结果数据 */
  result: ASRRecognitionResult;
};

/**
 * 语音识别核心结果类型（使用 type 定义）
 */
export type ASRRecognitionResult = {
  /** 分片类型：0 通常表示普通识别分片（可参考腾讯云文档，不同值对应不同分片类型，如收尾分片、纠错分片等） */
  slice_type: number;
  /** 分片索引：标识当前识别结果在整体语音中的分片顺序，从 0 开始递增 */
  index: number;
  /** 该分片语音的开始时间（单位：毫秒），对应整体语音的时间轴 */
  start_time: number;
  /** 该分片语音的结束时间（单位：毫秒），对应整体语音的时间轴 */
  end_time: number;
  /** 核心识别文本结果：实时返回的语音转文字内容 */
  voice_text_str: string;
  /** 词语列表大小：当前分片识别出的词语数量（此处为 0 表示无详细词语拆分，仅返回整句文本） */
  word_size: number;
  /** 词语详情列表：包含每个词语的详细信息，当前为空数组表示未返回详细词语数据 */
  word_list: ASRWordItem[];
};

/**
 * 词语详情类型（若 word_size > 0 时，word_list 会返回该类型数据）
 */
export type ASRWordItem = {
  // 注：该类型字段可根据腾讯云返回的详细数据补充，以下为常见字段示例
  /** 词语内容 */
  word?: string;
  /** 词语置信度（0-100，数值越高识别准确率越高） */
  confidence?: number;
  /** 词语在分片内的开始时间（毫秒） */
  start_time?: number;
  /** 词语在分片内的结束时间（毫秒） */
  end_time?: number;
};