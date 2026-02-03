<template>
    <view class="outer">
        <view class="box">
            <textarea v-model="userMessage" placeholder="任何旅行相关问题都可以问我哦" fixed maxlength="500"
                :auto-height="isAutoHeight" confirm-type="next" show-confirm-bar="false"
                placeholder-class="textarea-placeholder" cursor-spacing="20" @linechange="lineChange"
                @confirm="sendMessage" />
            <button plain @click.self="voice">
                <image src="/static/yuyin.png" mode="widthFix" />
            </button>
        </view>
    </view>
</template>

<script setup lang="ts">
import { sendMessageApi } from '@/api/request';
import type { EventType } from '@/types';
import { useAppStore } from '@/store/index'
const appStore = useAppStore()
import { getCurrentInstance, onMounted, reactive, ref } from 'vue';
const userMessage = ref('')

const sendMessage = () => {
    if (appStore.disabledStatus) return;
    sendMessageApi(userMessage.value)
    userMessage.value = ''
}

//输入框是否自动增高
const isAutoHeight = ref(true)

// 输入框行数变化
const lineChange = (e: EventType) => {
    isAutoHeight.value = e.detail.lineCount >= 4 ? false : true
}

// 获取按钮位置信息
const getBtnRect = async () => {
    const instance = getCurrentInstance();
    const query = uni.createSelectorQuery().in(instance!.proxy);
    query
        .select(".outer")
        .boundingClientRect((data) => {
            console.log('rect', data);
            if (data) {
                Object.assign(appStore.recordState.btnRect, data);
            }
        })
        .exec();
};

const voice = () => {
    appStore.isVoice = !appStore.isVoice
    console.log(appStore.recordState)
}

onMounted(() => {
    getBtnRect();
});
</script>

<style scoped lang="less">
.outer {
    position: fixed;
    left: 0;
    right: 0;
    bottom: 0;
    padding: 20rpx 40rpx 70rpx 40rpx;
    z-index: 99;
    background-color: #fff;

    .box {
        height: 66rpx;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border: 1rpx solid;
        border-color: rgba(80, 120, 255, 0.7) rgba(140, 80, 220, 0.7) rgba(40, 180, 220, 0.7) rgba(100, 140, 255, 0.7);
        border-radius: 40rpx;
        padding: 20rpx;

        textarea {
            flex: 1;
        }

        button {
            align-items: flex-end;
            width: 63rpx;
            height: 63rpx;
            padding: 0;
            margin: 0;
            border: none;

            image {
                width: 63rpx;
                height: 63rpx;
            }
        }
    }
}
</style>