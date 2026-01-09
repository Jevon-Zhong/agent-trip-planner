<template>
    <image class="login-image" src="/static/login-new.jpg" mode="widthFix" />
    <text class="login-tip">登陆开启你的AI行程</text>
    <view class="login-view">
        <button open-type="chooseAvatar" @chooseavatar="chooseavatar">
            <image :src="userInfo.avatar ? userInfo.avatar : '/static/touxiang.png'" />
        </button>
    </view>
    <form class="form-submit" @submit="login">
        <input type="nickname" placeholder="请输入昵称" name="nickname">
        <button form-type="submit" :loading="loading" :disabled="loading">登陆</button>
    </form>
</template>

<script setup lang="ts">
import { uploadImageApi, userLoginApi } from '@/api/request';
import type { AvatarEventType, LoginEventType } from '@/types';
import { reactive, ref } from 'vue';
import {useUserStore} from '@/store/index'
const userStore = useUserStore()

const login = async (event: LoginEventType) => {
    userInfo.nickname = event.detail.value.nickname
    //校验
    if (!userInfo.nickname || !userInfo.avatar) {
        uni.showToast({
            icon: 'none',
            title: '请填写头像和昵称'
        })
        return
    }
    loading.value = true
    console.log('登陆')
    // 上传头像
    const avatarRes = await uploadImageApi(userInfo.avatar)
    console.log(avatarRes)
    // 获取code
    const code = await getCode()
    // 登陆api
    const loginRes = await userLoginApi({avatar: userInfo.avatar, nickname: userInfo.nickname, code})
    console.log(loginRes)
    // 存储本地缓存
    userStore.userLogin(loginRes.data)

}

//获取code
const getCode = (): Promise<string> => {
    return new Promise((resolve, reject) => {
        uni.login({
            success: (res) => {
                resolve(res.code)
            },
            fail: (err) => {
                reject(err)
            }
        });
    })
}

const userInfo = reactive({
    avatar: '',
    nickname: ''
})

const loading = ref(false)

const chooseavatar = (event: AvatarEventType) => {
    console.log(event)
    userInfo.avatar = event.detail.avatarUrl
}
</script>

<style scoped lang="less">
page {
    background-color: #fafafa;

    .login-image {
        width: 100%;
        padding-top: 110px;
    }

    .login-tip {
        font-weight: bold;
        padding: 40rpx 20rpx;
    }

    .login-view {
        display: flex;
        flex-direction: column;
        align-items: center;

        button {
            padding: 0;
            margin: 0;
            line-height: inherit;
            background-color: transparent;
            border-radius: 50%;

            image {
                width: 150rpx;
                height: 150rpx;
            }
        }
    }

    .form-submit {
        width: 100%;

        input {
            padding: 20rpx;
            margin: 20rpx;
            border-bottom: 1rpx solid #f2f2f2;
        }

        button {
            background-color: #a2c5e5;
            padding: 5rpx 0;
            margin: 55rpx 20rpx 0 20rpx;
        }

    }
}
</style>