<template>
    <view class="outer">
        <image src="/static/lvxing-logo.png" mode="widthFix" />
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
    }

    text {
        font-weight: bold;
        font-size: 40rpx;
        padding: 30rpx 0;
    }
}
</style>