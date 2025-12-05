<template>
    <image class="login-image" src="/static/login-new.jpg" mode="widthFix" />
    <text class="login-tip">登陆开启你的AI行程</text>
    <view class="login-view">
        <button open-type="chooseAvatar">
            <image src="/static/touxiang.png"/>
        </button>
    </view>
    <form class="form-submit">
        <input type="nickname" placeholder="请输入昵称">
        <button form-type="submit">登陆</button>
    </form>
</template>

<script setup lang="ts">

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