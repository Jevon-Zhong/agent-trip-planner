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