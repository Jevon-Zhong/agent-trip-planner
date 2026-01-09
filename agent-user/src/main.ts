import { createSSRApp } from "vue";
import App from "./App.vue";
import { createPinia } from 'pinia'
import piniaPersist from 'pinia-plugin-persistedstate';
// @ts-ignore  // 忽略当前文件的 TS 检查
import uviewPlus from 'uview-plus'
const pinia = createPinia()
pinia.use(piniaPersist)
export function createApp() {
  const app = createSSRApp(App);
  app.use(uviewPlus)
  app.use(pinia)
  return {
    app,
  };
}
