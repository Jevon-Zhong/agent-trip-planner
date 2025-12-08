<template>
    <!-- 顶部侧边栏按钮 -->
    <view class="menu-outer">
        <view class="button-top"></view>
        <view class="menu-style">
            <image src="/static/chat-list.png" mode="widthFix" />
        </view>
    </view>
    <!-- 欢迎界面 -->
    <!-- <Welcome /> -->
    <!-- 快速卡片 -->
    <!-- <GridCard :cardData="cardData" /> -->
    <!-- 输入框 -->
    <ChatInput />
    <!-- 对话窗口 -->
    <Window />
    <!-- 历史对话记录 -->
    <History />
</template>

<script setup lang="ts">
import { ref } from 'vue'
const { height, top, bottom } = uni.getStorageSync("buttonPosition")
import type { CardDataType } from '@/types'
import Welcome from './components/welcome.vue'
import GridCard from "./components/gridCard.vue"
import ChatInput from "./components/chatInput.vue"
import Window from "./components/window.vue"
import History from "./components/history.vue"

import iconA from "@/static/icon-a.png"
import iconB from "@/static/icon-b.png"
import iconC from "@/static/icon-c.png"
import iconD from "@/static/icon-d.png"

const cardData = ref<CardDataType>([
    {
        icon: iconA,
        title: '为我发现目的地',
        subtitle: '寒假人少景美目的地',
        prompt: '为我推荐几个适合寒假旅游人少景美的国内目的地'
    },
    {
        icon: iconB,
        title: '为我找便宜高铁票',
        subtitle: '高铁优惠购票指南',
        prompt: '帮我查询近期从大理到丽江的高铁票，并推荐最便宜的方案'
    },
    {
        icon: iconC,
        title: '为我规划行程',
        subtitle: '智能个性化行程推荐',
        prompt: '昆明到丽江，两日游，为我规划一个行程'
    },
    {
        icon: iconD,
        title: '为我查询目的地天气',
        subtitle: '实时天气出行参考',
        prompt: '帮我查询下近期成都的天气，并告诉我是否适合出行'
    }

])
</script>

<style scoped lang="less">
.menu-outer {
    height: v-bind('height + "px"');
    background-color: linear-gradient(#e7ebff, #dedfff);
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 999;

    .button-top {
        height: v-bind('top + "px"');
    }

    .menu-style {
        display: flex;
        align-items: center;
        height: v-bind('height + "px"');
        padding-left: 20rpx;

        image {
            width: 40rpx;
        }
    }
}
</style>