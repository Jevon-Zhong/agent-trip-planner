import type { UserLoginResType } from '@/types'
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
    state: () => ({
        userInfo: null as UserLoginResType | null,
    }),
    getters: {

    },
    actions: {
        userLogin(userInfo: UserLoginResType) {
            this.userInfo = userInfo
        },
    },
    persist: {
        key: 'user_store',
        // 2. 自定义存储方式（UniApp 推荐用 uniStorage，兼容多端）
        storage: {
            // 读取数据
            getItem: (key) => uni.getStorageSync(key),
            // 存储数据
            setItem: (key, value) => uni.setStorageSync(key, value)
        },
        pick: ['userInfo']
    }
})