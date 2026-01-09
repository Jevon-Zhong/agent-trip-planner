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
export type ApiResponse<T>={
    code:number
    msg:string
    data:T
}

// 登陆接口返回的结果数据类型
export type UserLoginResType = {
    avatar: string
    nickname: string
    usertoken: string
}