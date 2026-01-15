<template>
    <view class="map-view">
        <text>路线地图</text>
        <map class="map-style" :id="appStore.messageList[index].mapId"
            :longitude="appStore.messageList[index].longitude" :latitude="appStore.messageList[index].latitude"
            :markers="appStore.messageList[index].markers" :polyline="appStore.messageList[index].polyline"
            :include-points="appStore.messageList[index].includePpoints" />

        <!-- 切换天数 -->
        <view class="item-day"
            v-if="appStore.messageList[index].locationData && appStore.messageList[index].locationData!.length > 0">
            <text v-for="(item, index1) in appStore.messageList[index].locationData" :key="index1"
                :class="{ 'select-day': index === selectIndex }" @click="changeDay(index, index1)">
                {{ item.day }}
            </text>
        </view>
    </view>
</template>

<script setup lang="ts">
import { useAppStore } from '@/store/index'
import { ref } from 'vue';
const appStore = useAppStore()
const selectIndex = ref(0)
// 父组件传递过来的对话index
defineProps<{
    index: number
}>()

const changeDay = (index: number, index1: number) => {
    const messageObj = appStore.messageList[index]
    messageObj.mapLoading = true
    appStore.changeDay(index, index1)
    messageObj.mapLoading = false
}
</script>

<style scoped lang="less">
.map-view {
    border-radius: 20rpx;

    .map-title {
        padding-bottom: 20rpx;
        font-size: 30rpx;
        font-weight: bold;
    }

    .map-style {
        width: 100%;
        height: 450rpx;
    }

    .item-day {
        display: flex;
        align-items: center;
        background-color: magenta;
        border-radius: 10rpx;
        margin-top: 20rpx;
        color: #fff;

        text {
            font-size: 27rpx;
            padding: 7rpx 15rpx;
            border-radius: 10rpx;
            margin: 10rpx;
            background: none;
        }
    }

    .select-day {
        background-color: #fff;
        color: black;
    }

}
</style>