// main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// 导入Element Plus
import ElementPlus from 'element-plus'
// 导入Element Plus CSS
import 'element-plus/dist/index.css'


// 创建Vue应用,并use Element Plus、router和vuex 
const app = createApp(App)
app.use(ElementPlus)
app.use(router)

// 挂载Vue应用
app.mount('#app')
