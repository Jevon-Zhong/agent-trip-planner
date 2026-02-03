<template>
    <view class="record-container">
        <!-- 录音状态提示 -->
        <view class="status-text" :class="{ cancelStatus: statusText === '松手取消' }">{{ statusText }}</view>
        <!-- 长方形录音按键 -->
        <view class="record-btn" id="record-btn-id" :style="{ backgroundColor: btnColor, borderColor: btnBorderColor }"
            @touchstart="handleTouchStart" @touchmove="handleTouchMove" @touchend="handleTouchEnd"
            @touchcancel="handleTouchCancel" ref="recordBtnRef">
            <text v-show="!appStore.recordState.isRecording" class="btn-text">长按开始录音</text>
            <button v-show="!appStore.recordState.isRecording" plain @touchstart.stop
                @touchend="appStore.isVoice = !appStore.isVoice" @longpress.prevent.stop>
                <image src="/static/jianpan.png" mode="widthFix" />
            </button>
            <view class="gapline" v-if="appStore.recordState.isRecording">
                <view class="item" v-for="item in 30" :key="item" />
            </view>
        </view>

        <!-- <view class="audio-actions" v-if="recordFilePath">
            <button class="audio-btn play-btn" @click="togglePlayAudio">
                {{ isPlaying ? '暂停播放' : '播放录音' }}
            </button>
            <button class="audio-btn delete-btn" @click="deleteAudio">
                删除录音
            </button>
        </view> -->
    </view>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted, getCurrentInstance, nextTick } from 'vue';
import { useAppStore } from '@/store/index'
import { getAsrUrlApi, sendMessageApi, uploadAudioApi } from '@/api/request';
const appStore = useAppStore()
// 按钮DOM引用
const recordBtnRef = ref<HTMLElement>();
// 按钮颜色
const btnColor = ref('#fff'); // 默认灰色
// 边框颜色
const btnBorderColor = ref('rgba(80, 120, 255, 0.7) rgba(140, 80, 220, 0.7) rgba(40, 180, 220, 0.7) rgba(100, 140, 255, 0.7)'); // 默认灰色
// 状态提示
const statusText = ref('');

// 新增：音频播放相关状态
const recordFilePath = ref(''); // 保存录音文件路径
// const isPlaying = ref(false); // 是否正在播放音频
let audioContext: UniApp.InnerAudioContext | null = null; // 音频播放上下文

// 录音管理器（使用uniapp统一API）
let recorderManager: UniApp.RecorderManager | null = null;
// 录音状态
// const recordState = reactive({
//     isRecording: false, // 是否正在录音
//     isOutOfRange: false, // 触点是否超出按钮范围
//     btnRect: { top: 0, left: 0, width: 0, height: 0 } // 按钮位置信息
// });
onMounted(() => {
    // getBtnRect();
    // 新增：初始化音频播放上下文
    // initAudioContext();
});

// 新增：初始化音频播放上下文
// const initAudioContext = () => {
//     // 创建音频播放实例
//     audioContext = uni.createInnerAudioContext();

//     // 监听播放错误
//     audioContext.onError((err) => {
//         console.error('音频播放错误：', err);
//         statusText.value = '播放失败：' + err.errMsg;
//         resetPlayState();
//     });

//     // 监听播放完成
//     audioContext.onEnded(() => {
//         statusText.value = '播放完成';
//         resetPlayState();
//     });

//     // 监听暂停事件
//     audioContext.onPause(() => {
//         isPlaying.value = false;
//     });
// };

// 获取按钮位置信息
// const getBtnRect = async () => {
//     const instance = getCurrentInstance();
//     const query = uni.createSelectorQuery().in(instance!.proxy);
//     query
//         .select("#record-btn-id")
//         .boundingClientRect((data) => {
//             console.log('rect', data);
//             if (data) {
//                 Object.assign(appStore.recordState.btnRect, data);
//             }
//         })
//         .exec();
// };

// 判断触点是否在按钮范围内
const isPointInBtn = (clientX: number, clientY: number): boolean => {
    const { left, top, width, height } = appStore.recordState.btnRect;
    return (
        clientX >= left &&
        clientX <= left + width &&
        clientY >= top &&
        clientY <= top + height
    );
};

// 初始化录音管理器（核心：使用uniapp的API）
recorderManager = uni.getRecorderManager();

// 录音成功回调
recorderManager.onStart(() => {
    appStore.recordState.isRecording = true;
    btnColor.value = '#007aff'; // 蓝色
    btnBorderColor.value = btnColor.value
    statusText.value = '松手发送，上移取消';
});

// 已录制完指定帧大小的文件，会回调录音分片结果数据。如果设置了 frameSize ，则会回调此事件
recorderManager.onFrameRecorded((res) => {
    // 将ArrayBuffer 转成可方便切片操作的 8位数组
    const buffer = new Uint8Array(res.frameBuffer)
    // 16k 采样率1280字节，即每一块都需要尽量为1280字节，可以在最后一块小于1280字节
    const CHUNK_SIZE = 1280
    //将buffer切块
    let offset = 0
    while (offset < buffer.length) {
        const slice = buffer.slice(offset, offset + CHUNK_SIZE)
        offset += CHUNK_SIZE
        appStore.socketTask.send({
            data: slice.buffer,
        });
    }
})

// 录音结束回调
recorderManager.onStop((res) => {
    appStore.recordState.isRecording = false;
    btnColor.value = '#fff'; // 恢复默认色
    btnBorderColor.value = 'rgba(80, 120, 255, 0.7) rgba(140, 80, 220, 0.7) rgba(40, 180, 220, 0.7) rgba(100, 140, 255, 0.7)'

    if (appStore.recordState.isOutOfRange) {
        statusText.value = '';
        recordFilePath.value = ''; // 取消录音则清空路径
    } else {
        // 新增：保存录音文件路径
        recordFilePath.value = res.tempFilePath;
        statusText.value = '录音完成，可播放或删除录音';
        console.log('录音文件：', res);
        // 录音停止后，延迟上传（确保临时文件生成完成）
        // setTimeout(() => {
        //     uploadAudioToBackend()
        // }, 200)
        // 通知腾讯云识别结束
        appStore.socketTask.send({
            data: JSON.stringify({ type: "end" }),
        });
    }
});

// 录音错误回调
recorderManager.onError((err) => {
    console.error('录音错误：', err);
    statusText.value = '录音失败：' + err.errMsg;
    recordFilePath.value = ''; // 录音失败清空路径
    // resetRecordState();
});

// 触摸开始（长按开始）
const handleTouchStart = async (e: TouchEvent) => {
    recordFilePath.value = ''; // 开始录音清空路径
    // 防止重复录音
    if (appStore.recordState.isRecording) return;

    // 重置录音状态
    // resetRecordState();
    // 获取ast url
    const res = await getAsrUrlApi()
    await appStore.connectASR(res.data)
    // 开始录音（uniapp统一配置）
    recorderManager.start({
        duration: 60000, // 最长录音时间60秒
        sampleRate: 16000,
        numberOfChannels: 1,
        encodeBitRate: 96000,
        format: "PCM",
        frameSize: 1,
    });
};

// 触摸移动
const handleTouchMove = (e: TouchEvent) => {
    if (!appStore.recordState.isRecording) return;

    // 获取触摸坐标
    const touch = e.changedTouches[0];
    const inRange = isPointInBtn(touch.clientX, touch.clientY);

    if (!inRange) {
        // 移出范围 - 红色
        appStore.recordState.isOutOfRange = true;
        btnColor.value = '#ff3b30';
        btnBorderColor.value = btnColor.value
        statusText.value = '松手取消';
    } else {
        // 移回范围 - 蓝色
        appStore.recordState.isOutOfRange = false;
        btnColor.value = '#007aff';
        btnBorderColor.value = btnColor.value
        statusText.value = '松手发送，上移取消';
    }
};

// 触摸结束（松开）
const handleTouchEnd = () => {
    stopRecord();
};

// 触摸被打断（如来电、弹窗）
const handleTouchCancel = () => {
    stopRecord(true);
    appStore.voiceResText = ''
};

// 停止录音
const stopRecord = (isCancel = false) => {
    if (recorderManager && appStore.recordState.isRecording) {
        // 如果是主动取消或超出范围，标记状态
        if (isCancel || appStore.recordState.isOutOfRange) {
            appStore.recordState.isOutOfRange = true;
            appStore.voiceResText = ''
        }
        if (appStore.voiceResText.trim() !== '') {
            sendMessageApi(appStore.voiceResText)
            appStore.voiceResText = ''
        }
        recorderManager.stop();
    }
};

// 重置录音状态
// const resetRecordState = () => {
//     appStore.recordState.isRecording = false;
//     appStore.recordState.isOutOfRange = false;
//     btnColor.value = '#fff';
// };

// 新增：播放/暂停音频切换
// const togglePlayAudio = () => {
//     if (!recordFilePath.value) {
//         statusText.value = '暂无录音文件可播放';
//         return;
//     }

//     if (isPlaying.value) {
//         // 暂停播放
//         audioContext?.pause();
//         isPlaying.value = false;
//         statusText.value = '已暂停播放';
//     } else {
//         // 开始播放
//         audioContext!.src = recordFilePath.value;
//         audioContext!.play();
//         isPlaying.value = true;
//         statusText.value = '正在播放录音...';
//     }
// };

// 新增：重置播放状态
// const resetPlayState = () => {
//     isPlaying.value = false;
//     audioContext?.pause();
// };

// 新增：删除音频
// const deleteAudio = () => {
//     // 先停止播放
//     resetPlayState();
//     // 清空录音路径
//     recordFilePath.value = '';
//     // statusText.value = '已删除录音文件';
//     statusText.value = '';
// };

// 页面卸载时清理资源
onUnmounted(() => {
    // 停止录音
    if (recorderManager && appStore.recordState.isRecording) {
        recorderManager.stop();
    }

    // 新增：销毁音频播放上下文
    // if (audioContext) {
    //     audioContext.stop();
    //     audioContext.destroy();
    //     audioContext = null;
    // }

    // resetRecordState();
    // resetPlayState();
});

// 上传音频文件到 FastAPI 后端
// const uploadAudioToBackend = async () => {
//     if (!recordFilePath.value) {
//         uni.showToast({ title: '无有效音频文件', icon: 'none' })
//         return
//     }

//     // 上传音频
//     const audioRes: any = await uploadAudioApi(recordFilePath.value)
//     console.log(audioRes)
// }




</script>

<style scoped lang="less">
.record-container {
    position: fixed;
    left: 0;
    right: 0;
    bottom: 0;
    padding: 20rpx 40rpx 70rpx 40rpx;
    z-index: 99;
    background-color: #fff;
}

.record-btn {
    width: auto;
    height: 66rpx;
    padding: 20rpx;
    display: flex;
    align-items: center;
    justify-content: space-between;
    touch-action: none;
    /* 禁用浏览器默认触摸行为 */
    user-select: none;
    /* 禁止文字选中 */
    border: 1rpx solid;
    border-color: rgba(80, 120, 255, 0.7) rgba(140, 80, 220, 0.7) rgba(40, 180, 220, 0.7) rgba(100, 140, 255, 0.7);
    border-radius: 40rpx;

    text {
        text-align: center;
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

    .gapline {
        width: 100%;
        display: flex;
        justify-content: center;

        .item {
            width: 8rpx;
            height: 20rpx;
            background-color: #fff;
            border-radius: 30rpx;
            margin: 0 4rpx;
        }
    }
}

.btn-text {
    font-weight: bold;
    font-size: 32rpx;
    color: #333;
}

.status-text {
    width: 100%;
    text-align: center;
    margin-bottom: 30rpx;
    font-size: 28rpx;
    color: #666;
}

.cancelStatus {
    color: red !important;
}

/* 新增：音频操作按钮样式 */
.audio-actions {
    display: flex;
    gap: 30rpx;
    margin-top: 40rpx;
}

.audio-btn {
    padding: 20rpx 40rpx;
    border-radius: 10rpx;
    border: none;
    font-size: 28rpx;
    color: #fff;
}

.play-btn {
    background-color: #007aff;
}

.delete-btn {
    background-color: #ff3b30;
}
</style>