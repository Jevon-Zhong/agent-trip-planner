<template>
    <view class="outer">
        <template v-for="(item, index) in appStore.messageList" :key="index">
            <!-- 用户消息 -->
            <view class="user-message" v-if="item.role === 'user'">
                <text>{{ item.content }}</text>
            </view>
            <!-- 工具回复的消息 -->
            <view class="tool-message" v-if="item.role === 'assistant' && item.toolList && item.toolList.length">
                <text>{{ item.toolThinking ? '分析思考中...' : '分析思考完毕' }}</text>
                <ToolSteps :tool-list="item.toolList" />
            </view>
            <!-- 模型回复的消息 -->
            <view class="ai-message" v-if="item.role === 'assistant' && item.content != ''">
                <up-markdown :content="item.content" />
            </view>
            <up-skeleton v-if="item.loading" style="margin-top: 30rpx;" rows="4" :loading="true" :title="false">
                <up-text>loading为false时，将会展示此处插槽内容</up-text>
            </up-skeleton>
            <!-- 地图数据 -->
            <view class="view-map" v-if="item.role == 'assistant' && item.content && item.modelSuccess">
                <Map style="width: 100%;height: auto;" :index="index" v-if="item.locationData && item.locationData.length > 0" />
                <view class="map-seek" @click="getLoacationData(item.content, index)" v-if="!item.locationData && !item.mapLoading">
                    <text>查看地图规划</text>
                    <text class="map-seek-text">点击查看</text>
                </view>
                <up-skeleton v-if="item.mapLoading" style="margin-top: 30rpx;" rows="4" :loading="true" :title="false">
                    <up-text>loading为false时，将会展示此处插槽内容</up-text>
                </up-skeleton>
            </view>
        </template>
    </view>
</template>

<script setup lang="ts">
import ToolSteps from './toolSteps.vue';
const { top, bottom, right } = uni.getStorageSync("buttonPosition")
import Map from '../components/map.vue'
import { useAppStore } from '@/store/index'
import { getLoacationDataApi } from '@/api/request';
const appStore = useAppStore()



// 请求地图数据
const getLoacationData = async (content: string, index: number) => {
    const messageObj = appStore.messageList[index]
    messageObj.mapLoading = true
    const res = await getLoacationDataApi({ content })
    const mapId = String(Date.now() + index)
    messageObj.mapId = mapId
    messageObj.locationData = res.data
    // 更新地图, 默认展示第一天数据
    appStore.changeDay(index, 0)
    messageObj.mapLoading = false
}
</script>

<style scoped lang="less">
.outer {
    padding-top: v-bind('bottom + 10 + "px"');
    display: flex;
    flex-direction: column;
    margin: 0 15rpx;
    padding-bottom: 250rpx;

    .user-message {
        margin-top: 30rpx;
        max-width: 70%;
        align-self: flex-end;
        background-color: #3a71e8;
        padding: 10rpx;
        color: #fff;
        border-radius: 10rpx;

        text {
            line-height: 1.5;
            font-size: 30rpx;
        }
    }

    .tool-message {
        margin-top: 30rpx;
        background-color: #eee;
        padding: 10rpx;
        border-radius: 10rpx;
        font-size: 30rpx;

        text {
            font-weight: bold;
            color: darkmagenta;
            padding-bottom: 6rpx;
        }
    }

    .ai-message {
        margin-top: 30rpx;
        background-color: #fff;
        padding: 10rpx;
        border-radius: 10rpx;
    }

    .view-map {
        background-color: #8bffff;
        border-radius: 15rpx;
        padding: 20rpx;
        margin: 40rpx 0;
        font-size: 30rpx;
        color: #5ea5f5;

        .map-seek {
            display: flex;
            justify-content: space-between;
        }

        .map-seek-text {
            font-size: 25rpx;
        }
    }
}
</style>