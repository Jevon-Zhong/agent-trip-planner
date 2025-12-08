<template>
  <view class="steps-view">
    <!-- 单个步骤 -->
    <view class="step-item" v-for="(step, index) in toolList" :key="index">
      <!-- 左边（点和线） -->
      <view class="steps-left">
        <!-- 圆点 -->
        <text
          class="step-circle"
          :class="{
            active: index < toolList.length - 1,
            finished: index < toolList.length,
          }"
        ></text>
        <!-- 线（最后一个步骤没有线） -->
        <text v-if="index < toolList.length - 1" class="step-line"></text>
      </view>

      <!-- 右边（内容） -->
      <view class="steps-right">
        <text>
          {{ step }}
        </text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
defineProps<{
  toolList: string[];
}>();
</script>

<style scoped>
.steps-view {
  display: flex;
  flex-direction: column;
  padding: 15rpx;
}

/* 每个步骤 */
.step-item {
  display: flex;
  align-items: flex-start;
}

/* 左边点和线 */
.steps-left {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-right: 15rpx;
  position: relative;
  margin-top: 10rpx;
}

/* 圆点 */
.step-circle {
  width: 20rpx;
  height: 20rpx;
  border-radius: 50%;
}

/* 连接线 */
.step-line {
  width: 4rpx;
  height: 40rpx; /* 固定高度，保证每个圆点下方有一条竖线 */
  margin-top: 10rpx;
  background-color: #3c9cff;
}

/* 右边文字 */
.steps-right {
  flex: 1;
}
.steps-right text {
  font-size: 28rpx;
  color: #999;
}
/* 开始走，完成状态变化 */
.active {
  background-color: #3c9cff !important;
}
.finished {
  background-color: #969799;
}
</style>
