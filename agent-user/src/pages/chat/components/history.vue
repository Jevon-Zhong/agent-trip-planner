<template>
    <up-popup class="my-popup" :show="appStore.switchHistoryAndChat" @close="close" closeOnClickOverlay
        :customStyle="{ marginTop: `${bottom + 10}px`, width: '600rpx' }"
        :overlayStyle="{ marginTop: `${bottom + 10}px` }" mode="left" zIndex="99">
        <view>
            <view class="user-info" @click="show = true">
                <up-avatar :src="appStore.userInfo?.avatar" shape="circle"></up-avatar>
                <!-- <image :src="appStore.userInfo?.avatar" mode="aspectFill" /> -->
                <text>{{ appStore.userInfo?.nickname }}</text>
            </view>
        </view>
        <up-button :customStyle="{ width: '94%' }" text="新建对话" @click="newChat"></up-button>
        <view class="history-title">历史对话</view>
        <up-list height="500">
            <up-list-item v-for="(item, index) in appStore.conversationList" :key="item.thread_id">
                <!-- <view class="hostory-item" @click="appStore.getContent(item.thread_id)"
                    :class="{ hostoryItemSelected: appStore.selectedThreadId && item.thread_id === appStore.selectedThreadId }">
                    <text>{{ item.title }}</text>
                </view> -->
                <up-swipe-action :autoClose="true">
                    <up-swipe-action-item :options="options1" @click="deleteSession(item.thread_id)">
                        <view class="swipe-action"
                            :class="{ hostoryItemSelected: appStore.selectedThreadId && item.thread_id === appStore.selectedThreadId }">
                            <!-- class="hostory-item" -->
                            <view class="swipe-action__content" @click="appStore.getContent(item.thread_id)">
                                <text
                                    :class="{ hostoryItemSelectedtext: appStore.selectedThreadId && item.thread_id === appStore.selectedThreadId }"
                                    class="swipe-action__content__text">{{ item.title }}</text>
                            </view>
                        </view>
                    </up-swipe-action-item>
                </up-swipe-action>
            </up-list-item>
        </up-list>
    </up-popup>
    <up-loading-page style="z-index: 99999999;" bg-color="#0000002e" :loading="appStore.loading"></up-loading-page>
    <up-notify message="删除失败" ref="uNotifyRef" type="error"></up-notify>
    <up-toast ref="uToastRef"></up-toast>
    <up-action-sheet :show="show" @select="selectClick" @close="show = false" :actions="actions"
        cancelText="取消"></up-action-sheet>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue';
import { useAppStore } from '@/store/index'
const appStore = useAppStore()
import { onLoad } from '@dcloudio/uni-app';
import { conversationDetailApi, conversationListApi, deleteConversationApi, getQuickQuestionApi } from '@/api/request';
import type { MapDataType, MessageListType, ModelMapType } from '@/types';
const { top, bottom, right } = uni.getStorageSync("buttonPosition")
const close = () => {
    // 关闭逻辑，设置 show 为 false  
    appStore.switchHistoryAndChat = false
}
//对话历史数据
// const newSessionData = ref<MessageListType[]>([])
//临时存储工具名称列表
// const toolList = ref<string[]>([])
//临时存储每一天的地图路线数据
// const mapDataList = ref<MapDataType[]>([])
// const getContent = async (thread_id: string) => {
//     console.log('thread_id', thread_id)
//     const res = await conversationDetailApi(thread_id)
//     console.log(res)
//     res.data.forEach((item) => {
//         // 如果是用户的消息
//         if (item.role === 'user') {
//             newSessionData.value.push(item)
//         }
//         // 如果是工具名称
//         if (item.role === 'tool') {
//             toolList.value?.push(item.content)
//         }
//         // 如果是模型消息
//         if (item.role === 'assistant') {
//             newSessionData.value.push(item)
//             // 处理工具名单
//             let lastObj
//             if (toolList.value.length > 0) {
//                 lastObj = newSessionData.value[newSessionData.value.length - 1]
//                 if (lastObj) {
//                     lastObj.toolList = toolList.value
//                 }
//                 toolList.value = []
//             }
//             // 处理地图位置（与哪条消息合并）
//             if (mapDataList.value.length > 0) {
//                 if (lastObj?.toolList?.includes('map_data')) {
//                     lastObj.mapDataList = mapDataList.value
//                 }
//             }
//         }
//         // 如果是工具返回结果
//         if (item.role === 'tool_result') {
//             console.log('触发tool_result')
//             let jsonMap: ModelMapType
//             if (typeof item.content.null === 'string') {
//                 jsonMap = JSON.parse(item.content.null);
//             } else {
//                 jsonMap = item.content.null; // 已是对象，直接使用
//             }
//             // 将每一天的地图数据返回存储到mapDataList
//             if (jsonMap.type && jsonMap.type === "route_polyline") {
//                 console.log('jsonMap', jsonMap)
//                 const newMapItem = appStore.makeUpMap(jsonMap);
//                 console.log('newMapItem', newMapItem)
//                 console.log('Object.keys(newMapItem)', Object.keys(newMapItem))
//                 console.log('Object.keys(newMapItem).length', Object.keys(newMapItem).length)
//                 if (Object.keys(newMapItem).length > 0) {
//                     mapDataList.value.push(newMapItem)
//                     // const lastObj = newSessionData.value[newSessionData.value.length - 1]
//                     // console.log('lastObj', lastObj)
//                     // if (lastObj) {
//                     //     if (lastObj.mapDataList) {
//                     //         lastObj.mapDataList.push(newMapItem);
//                     //     } else {
//                     //         lastObj.mapDataList = [newMapItem]
//                     //     }
//                     //     console.log('lastObj.mapDataList', lastObj)
//                     // }
//                     // console.log('tool_result', lastObj)
//                 }
//             }
//         }
//     })
//     console.log('dddddd')
//     console.log(newSessionData.value)
//     console.log('dddddd')
//     appStore.messageList = newSessionData.value
//     appStore.selectedThreadId = thread_id
//     toolList.value = []
//     newSessionData.value = []
//     appStore.switchHistoryAndChat = false
// }

const newChat = async () => {
    appStore.switchHistoryAndChat = false
    appStore.messageList = []
    appStore.selectedThreadId = ''
    appStore.cardSkeleton = true
    const res = await getQuickQuestionApi()
    appStore.CardDataList = res.data
    appStore.cardSkeleton = false
}

// 使用 reactive 创建响应式对象  
const options1 = reactive([{
    text: '删除',
    style: {
        backgroundColor: 'red',
        marginBottom: '20rpx',
        borderColor: 'yellow'
    }
}]);

const uToastRef = ref()

// 删除会话
const deleteSession = async (sessionId: string) => {
    appStore.loading = true
    const res = await deleteConversationApi(sessionId)
    if (res.code === 200) {
        // 获取对话列表数据
        const res = await conversationListApi()
        appStore.conversationList = res.data
        // 如果当前对话是要被删除的那个对话
        if (sessionId === appStore.selectedThreadId) {
            appStore.getContent(appStore.conversationList[0].thread_id)
        }
        appStore.switchHistoryAndChat = false
        appStore.loading = false
    } else {
        uToastRef.value.show({
            type: 'error',
            message: '删除失败'
        });
    }

}

const show = ref(false)

const actions = ref([{
    name: '退出登陆',
},
])

const selectClick = (index: { name: string }) => {
    if (index.name = '退出登陆') {
        appStore.userInfo = null
        uni.navigateTo({ url: '/pages/login/index' })
    }
};  
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
    background-color: #5a66fc !important;
}

.hostoryItemSelectedtext {
    color: #fff !important;
}


.swipe-action {
    background-color: #fff;
    border-radius: 20rpx;
    margin: 0 20rpx 20rpx 20rpx;
    padding: 20rpx;

    &__content {

        &__text {
            font-size: 15px;
            color: #000;
            display: -webkit-box;
            overflow: hidden;
            -webkit-box-orient: vertical;
            -webkit-line-clamp: 1;
        }
    }
}
</style>