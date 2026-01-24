<template>
    <view class="card-outer">
        <view class="box" v-for="item in cardData" :key="item.title" @click="sendMessage(item.prompt)">
            <view class="head">
                <image :src="item.icon" mode="widthFix" />
                <text class="title">{{ item.title }}</text>
            </view>
            <text v-show="!appStore.cardSkeleton" class="prompt">{{ item.prompt }}</text>
            <view style="width: 100%;">
                <up-skeleton v-show="appStore.cardSkeleton" rows="2" :loading="true" :title="false">
                    <up-text>loading为false时，将会展示此处插槽内容</up-text>
                </up-skeleton>
            </view>

        </view>
    </view>
    <view class="reload">
        <up-icon @click="changeQuestion" :size="20" name="reload" label="换一换" :labelSize="14"></up-icon>
    </view>
</template>

<script setup lang="ts">
import { getQuickQuestionApi, sendMessageApi } from '@/api/request';
import type { CardDataType } from '@/types'
import { useAppStore } from '@/store/index'
const appStore = useAppStore()

// 2. 子组件定义Props（指定类型/默认值/校验）
const props = defineProps<{ cardData: CardDataType }>()

const sendMessage = (prompt: string) => {
    sendMessageApi(prompt)
}

const changeQuestion = async () => {
    appStore.cardSkeleton = true
    const res = await getQuickQuestionApi()
    appStore.CardDataList = res.data
    appStore.cardSkeleton = false
}
</script>

<style scoped lang="less">
.card-outer {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20rpx;
    margin: 0 20rpx;

    .box {
        height: 180rpx;
        display: flex;
        flex-direction: column;
        align-items: center;
        background-image: linear-gradient(135deg,
                rgba(200, 215, 255, 0.3),
                /* 极淡蓝紫（透明度降至0.4） */
                rgba(180, 195, 255, 0.1),
                /* 超浅蓝紫过渡（透明度降至0.3） */
                rgba(190, 175, 245, 0.2)
                /* 极淡紫蓝（透明度降至0.4） */
            );
        border-radius: 15rpx;
        border: 1rpx solid #fff;
        padding: 10rpx 20rpx 20rpx 20rpx;

        .head {
            width: 100%;
            display: flex;
            align-items: center;
            border-radius: 0;

            image {
                width: 40rpx;
                margin-right: 5rpx;
            }

            .title {
                color: rgb(99, 120, 223);
                padding: 15rpx 0;
                font-weight: bold;
                font-size: 25rpx;
            }
        }

        .prompt {
            font-size: 30rpx;
            color: #4a4848;
            font-weight: bold;
        }
    }
}

.reload {
    width: 100%;
    display: flex;
    justify-content: center;
    margin-top: 70rpx;
}

.card-outer :nth-child(1) {
    border-radius: 30rpx 30rpx 30rpx 0;
}

.card-outer :nth-child(2) {
    border-radius: 30rpx 30rpx 0 30rpx;
}

.card-outer :nth-child(3) {
    border-radius: 0 30rpx 30rpx 30rpx;
}

.card-outer :nth-child(4) {
    border-radius: 30rpx 0 30rpx 30rpx;
}
</style>