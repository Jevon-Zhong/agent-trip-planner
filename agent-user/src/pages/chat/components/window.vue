<template>
    <view class="outer">
        <!-- 用户消息 -->
        <view class="user-message">
            <text>用户发送的消息</text>
        </view>
        <!-- 工具回复的消息 -->
        <view class="tool-message">
            <text>分析思考中</text>
            <ToolSteps :tool-list="['第一个', '第二个']" />
        </view>
        <!-- 模型回复的消息 -->
        <view class="ai-message">模型回复的消息模型回复的消息模型回复的消息模型回复的消息模型回复的消息模型回复的消息</view>
        <!-- 地图数据 -->
    </view>
</template>

<script setup lang="ts">
import ToolSteps from './toolSteps.vue';
const { top, bottom, right } = uni.getStorageSync("buttonPosition")
</script>

<style scoped lang="less">
.outer {
    padding-top: v-bind('bottom + 10 + "px"');
    display: flex;
    flex-direction: column;
    margin: 0 15rpx;

    .user-message {
        margin-top: 30rpx;
        max-width: 70%;
        align-self: flex-end;

        text {
            line-height: 1.5;
            background-color: #3a71e8;
            border-radius: 10rpx;
            color: #fff;
            padding: 10rpx;
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
}
</style>