<template>
    <div>
      <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal">
        <el-menu-item index="1">
          <router-link to="/">首页</router-link>
        </el-menu-item>
        <el-menu-item index="2">
          <router-link to="/login">登录</router-link>
        </el-menu-item>
        <el-menu-item index="5">
          <router-link to="/bills/generate">账单生成</router-link>
        </el-menu-item>
        <el-menu-item index="8">
          <router-link to="/clerk/unpaid_bills">收费员查账</router-link>
        </el-menu-item>
        <!-- <el-menu-item index="9">
          <router-link to="/clerk/charge">收费员收费</router-link>
        </el-menu-item> -->
        <el-menu-item index="10">
          <router-link to="/users/soft_delete">软删除</router-link>
        </el-menu-item> 
        <!-- <el-menu-item index="10"> -->
          <!-- <router-link to="/users/hard_delete">硬删除</router-link> -->
        <!-- </el-menu-item> -->
      </el-menu>
      <el-button @click="handleLogout">登出</el-button>
    </div>
  </template>

  
  <script>
  import { logout } from "@/api";
  
  export default {
    data() {
      return {
        activeIndex: "1",
      };
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
  };
  </script>
  
  <style scoped>
  .el-menu-demo {
    background-color: #545c64;
  }
  </style>
  