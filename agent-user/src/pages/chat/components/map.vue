<template>
    <view class="map-view">
        <view style="margin-bottom: 10rpx; color: #404564;">路线地图</view>
        <map class="map-style" :id="mapDataList[selectIndex].mapId"
            :longitude="mapDataList[selectIndex].longitude" :latitude="mapDataList[selectIndex].latitude"
            :markers="mapDataList[selectIndex].markers" :polyline="mapDataList[selectIndex].polyline"
            :include-points="mapDataList[selectIndex].includePoints" />

        <!-- 切换天数 -->
        <view class="item-day">
            <text v-for="(item, index) in mapDataList" :class="{ 'select-day': index === selectIndex }" @click="changeDay(index)">
                {{ item.day }}
            </text>
        </view>
    </view>
</template>

<script setup lang="ts">
import { useAppStore } from '@/store/index'
import type { MapDataType } from '@/types';
import { ref } from 'vue';
const appStore = useAppStore()
const selectIndex = ref(0)
// 父级下标
const prop = defineProps<{
    mapDataList: MapDataType[];
}>();

const changeDay = (index: number) => {
    selectIndex.value = index
}
</script>

<style scoped lang="less">
.map-view {
    border-radius: 20rpx;
    // box-shadow:4px 4px 15px #cbcbcb;
    border: 1rpx solid #cbcbcb;
    padding: 20rpx;
    box-sizing: border-box;

    .map-title {
        padding-bottom: 20rpx;
        font-size: 30rpx;
        font-weight: bold;
    }

    .map-style {
        width: 100%;
        height: 480rpx;
    }

    .item-day {
        display: flex;
        align-items: center;
        border-radius: 10rpx;
        margin: 15rpx 0;

        text {
            color: #333;
            font-size: 27rpx;
            padding: 7rpx 15rpx;
            border: 1rpx solid #eeee;
            border-radius: 10rpx;
            box-sizing: border-box;
            margin-right: 10rpx;
        }
    }

    .select-day {
        background-color: #888fb6;
        color: #ffffff;
    }

}
</style>