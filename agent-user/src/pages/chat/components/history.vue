<template>
    <up-popup :show="show" @close="close" closeOnClickOverlay
        :customStyle="{ marginTop: `${bottom + 10}px`, width: '600rpx' }"
        :overlayStyle="{ marginTop: `${bottom + 10}px` }" mode="left">
        <view>
            <view class="user-info">
                <image src="/static/logo.png" mode="aspectFill" />
                <text>用户昵称</text>
            </view>
        </view>
        <up-button :customStyle="{ width: '94%'}" text="新建对话"></up-button>
        <view class="history-title">历史对话</view>
        <up-list>
            <up-list-item v-for="(item, index) in 6" :key="index">
                <view class="hostory-item">
                    <text>{{ `列表长度-${index + 1}` }}</text>
                </view>
            </up-list-item>
        </up-list>
    </up-popup>
</template>

<script setup lang="ts">
import { ref } from 'vue';
const { top, bottom, right } = uni.getStorageSync("buttonPosition")
const show = ref(true)
const close = () => {
    // 关闭逻辑，设置 show 为 false  
    show.value = false;
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
    margin: 20rpx 20rpx 0rpx 20rpx;
    font-weight: bold;
    color: purple;
}

.hostory-item {
    background-color: #fff;
    border-radius: 20rpx;
    margin: 20rpx;
    padding: 20rpx;
}
</style>