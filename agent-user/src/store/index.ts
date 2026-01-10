import type { ConversationListType, MessageListType, UserLoginResType } from '@/types'
import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', {
    state: () => ({
        userInfo: null as UserLoginResType | null,
        conversationList:[] as ConversationListType,
        selectedThreadId: '',
        switchHistoryAndChat: false,
        messageList:[] as MessageListType[],//用户和模型的对话列表
    }),
    getters: {

    },
    actions: {
        userLogin(userInfo: UserLoginResType) {
            this.userInfo = userInfo
        },
    },
    persist: {
        key: 'app_store',
        // 2. 自定义存储方式（UniApp 推荐用 uniStorage，兼容多端）
        storage: {
            // 读取数据
            getItem: (key) => uni.getStorageSync(key),
            // 存储数据
            setItem: (key, value) => uni.setStorageSync(key, value)
        },
        pick: ['userInfo', 'conversationList', 'selectedThreadId', 'messageList']
    }
})