<!-- vue-web\src\views\HomePage.vue -->
<template>
  <div>
    <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal">
      <el-menu-item index="1"><router-link to="/">首页</router-link></el-menu-item> 
      <el-menu-item index="2"><router-link to="/login">登录</router-link></el-menu-item>   
      <el-menu-item index="3"><router-link to="/users/register">注册</router-link></el-menu-item>
      <el-menu-item index="4"><router-link to="/profile">个人信息</router-link></el-menu-item>
      <!-- <el-menu-item index="5"><router-link to="/profile/update">信息修改</router-link></el-menu-item> -->
      <el-menu-item index="6"><router-link to="/bills">获取未支付账单</router-link></el-menu-item>
      <!-- <el-menu-item index="7"><router-link to="/payments">付款</router-link></el-menu-item> -->
    </el-menu>
    <el-button @click="handleLogout">登出</el-button>

  </div>
</template>

<script>
  import { logout } from "@/api";

export default {
  data() {
    return {
      activeIndex: '1'
    }
  },  
  methods: {
      async handleLogout() {
        try {
          await logout();
          this.$router.push("/");
          localStorage.removeItem("access_token");
        } catch (err) {
          console.log(err.message);
          if (err.message === "No access_token found.") return;
        }
      },
    },
}
</script>

<style scoped>
.el-menu-demo {
  background-color: #545C64;
}
</style>
