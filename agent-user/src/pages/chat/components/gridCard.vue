<template>
    <view class="card-outer">
        <view class="box" v-for="item in cardData" :key="item.title">
            <image :src="item.icon" mode="widthFix" />
            <text class="title">{{ item.title }}</text>
            <text class="subtitle">{{ item.subtitle }}</text>
        </view>
    </view>
</template>

<script setup lang="ts">
import type { CardDataType } from '@/types'

// 2. 子组件定义Props（指定类型/默认值/校验）
const props = defineProps<{ cardData: CardDataType }>()
</script>

<style scoped lang="less">
.card-outer {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20rpx;
    margin: 0 20rpx;

    .box {
        display: flex;
        flex-direction: column;
        align-items: center;
        background-image: linear-gradient(135deg,
                rgba(200, 215, 255, 0.3),
                /* 极淡蓝紫（透明度降至0.4） */
                rgba(180, 195, 255, 0.2),
                /* 超浅蓝紫过渡（透明度降至0.3） */
                rgba(190, 175, 245, 0.3)
                /* 极淡紫蓝（透明度降至0.4） */
            );
        border-radius: 15rpx;
        border: 1rpx solid #fff;
        padding: 25rpx 0;

        image {
            width: 60rpx;
        }

        .title {
            padding: 15rpx 0;
            font-weight: bold;
        }

        .subtitle {
            font-size: 26rpx;
            color: #8b949b;
        }
    }
}
</style>