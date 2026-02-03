<template>
    <view class="outer">
        <image src="https://i.ibb.co/Rp8qBmqY/ggg.gif" mode="widthFix" />
        <!-- <up-avatar src="/static/ggg.gif" shape="circle" :size="180"></up-avatar> -->
        <text>Hi！我是你的AI旅行规划助手</text>
    </view>
</template>

<script setup lang="ts">
</script>

<style scoped lang="less">
.outer {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 200rpx 25rpx 0 25rpx;

    image {
        width: 340rpx;
        height: 340rpx;
        border-radius: 50%;
    }

    text {
        font-weight: bold;
        font-size: 40rpx;
        padding: 30rpx 0;
    }
}
</style>