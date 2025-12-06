<script setup lang="ts">
import { onLaunch, onShow, onHide } from "@dcloudio/uni-app";
onLaunch(() => {
  console.log("App Launch");
  // 获取胶囊按钮坐标
  const buttonPosition = uni.getStorageSync('buttonPosition')
  if (!buttonPosition) {
    const res = uni.getMenuButtonBoundingClientRect()
    // 存储本地缓存
    uni.setStorageSync('buttonPosition', res)
  }

});
onShow(() => {
  console.log("App Show");
});
onHide(() => {
  console.log("App Hide");
});
</script>
<style></style>
