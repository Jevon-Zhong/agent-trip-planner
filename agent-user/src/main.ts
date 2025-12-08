import { createSSRApp } from "vue";
import App from "./App.vue";
// @ts-ignore  // 忽略当前文件的 TS 检查
import uviewPlus from 'uview-plus'
export function createApp() {
  const app = createSSRApp(App);
  app.use(uviewPlus)
  return {
    app,
  };
}
