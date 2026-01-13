<template>
    <up-popup class="my-popup" :show="appStore.switchHistoryAndChat" @close="close" closeOnClickOverlay
        :customStyle="{ marginTop: `${bottom + 10}px`, width: '600rpx' }"
        :overlayStyle="{ marginTop: `${bottom + 10}px` }" mode="left" zIndex="99">
        <view>
            <view class="user-info">
                <image :src="appStore.userInfo?.avatar" mode="aspectFill" />
                <text>{{ appStore.userInfo?.nickname }}</text>
            </view>
        </view>
        <up-button :customStyle="{ width: '94%' }" text="新建对话" @click="newChat"></up-button>
        <view class="history-title">历史对话</view>
        <up-list height="500">
            <up-list-item v-for="(item, index) in appStore.conversationList" :key="item.thread_id">
                <view class="hostory-item" @click="getContent(item.thread_id)"
                    :class="{ hostoryItemSelected: appStore.selectedThreadId && item.thread_id === appStore.selectedThreadId }">
                    <text>{{ item.title }}</text>
                </view>
            </up-list-item>
        </up-list>
    </up-popup>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAppStore } from '@/store/index'
const appStore = useAppStore()
import { onLoad } from '@dcloudio/uni-app';
import { conversationDetailApi } from '@/api/request';
import type { MessageListType } from '@/types';
const { top, bottom, right } = uni.getStorageSync("buttonPosition")
const close = () => {
    // 关闭逻辑，设置 show 为 false  
    appStore.switchHistoryAndChat = false
}
//对话历史数据
const newSessionData = ref<MessageListType[]>([])
//临时存储工具名称列表
const toolList = ref<string[]>([])
const getContent = async (thread_id: string) => {
    const res = await conversationDetailApi(thread_id)
    console.log(res)
    res.data.forEach((item) => {
        // 如果是用户的消息
        if (item.role === 'user') {
            newSessionData.value.push(item)
        }
        // 如果是工具名称
        if (item.role === 'tool') {
            toolList.value?.push(item.content)
        }
        // 如果是模型消息
        if (item.role === 'assistant') {
            newSessionData.value.push(item)
            if (toolList.value?.length > 0) {
                const lastObj = newSessionData.value[newSessionData.value.length - 1]
                if (lastObj) {
                    lastObj.toolList = toolList.value
                }
                toolList.value = []
            }
        }
    })
    console.log('dddddd')
    console.log(newSessionData.value)
    console.log('dddddd')
    appStore.messageList = newSessionData.value
    appStore.selectedThreadId = thread_id
    toolList.value = []
    newSessionData.value = []
    appStore.switchHistoryAndChat = false
}

const newChat = () => {
    appStore.switchHistoryAndChat = false
    appStore.messageList = []
    appStore.selectedThreadId = ''
}
</script>

<style scoped lang="less">
.user-info {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 30rpx 0;

    image {
        width: 90rpx;
        height: 90rpx;
        border-radius: 50%;
    }

    text {
        font-size: 35rpx;
        font-weight: bold;
        padding-top: 10rpx;
    }
}

.history-title {
    font-size: 32rpx;
    margin: 20rpx 20rpx 10rpx 20rpx;
    font-weight: bold;
    color: purple;
}

.hostory-item {
    background-color: #fff;
    border-radius: 20rpx;
    margin: 0 20rpx 20rpx 20rpx;
    padding: 20rpx;

    text {
        display: -webkit-box;
        overflow: hidden;
        -webkit-box-orient: vertical;
        -webkit-line-clamp: 1;
    }
}

.hostoryItemSelected {
    background-color: #5a66fc;
    color: #fff;
    border-radius: 20rpx;
    margin: 0 20rpx 20rpx 20rpx;
    padding: 20rpx;
}
</style>