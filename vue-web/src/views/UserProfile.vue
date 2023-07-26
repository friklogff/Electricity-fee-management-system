<template>
  <el-container>
    <el-main>
      <el-card>
        <h2>用户信息</h2>
        <p>姓名: {{ user.RealName }}</p>
        <p>手机号: {{ user.Phone }}</p>
        <p>ID: {{ user.IDCard }}</p>
        <p>邮箱: {{ user.Email }}</p>
        <p>地址: {{ user.Address }}</p>
        <p>用电类型: {{ user.ElecType }}</p>
      </el-card>

      <el-space direction="vertical" :size="50">
        <el-button @click="logout" type="danger">登出</el-button>
        <el-button @click="goUpdate" type="primary">修改信息</el-button>
        <el-button @click="goHome" type="success">返回首页</el-button>
      </el-space>
    </el-main>
  </el-container>
</template>
<script>
import { getProfile, logout } from '@/api'
export default {
  data() {
    return {
      user: {},
    }
  },
  created() {
    console.log('调用getProfile接口获取用户信息')
    this.getProfile()
  },
  methods: {
    // 获取用户信息
    getProfile() {
      getProfile()
        .then((res) => {
          console.log('获取用户信息成功!响应内容:', res)
          this.user = res.data[0]
          console.log('user对象填充成功:', this.user)
        })
        .catch((err) => {
          console.log('获取用户信息失败!错误信息:', err.message)
          this.$router.push('/')
        })
    },
    // 登出
    logout() {
      logout()
        .then(() => {
          this.$router.push('/')
          localStorage.removeItem('access_token')
        })
        .catch((err) => {
          if (err.message === 'No access_token found.') {
            console.log(err.message)
            return
          }
          console.log(err.message)
        })
    }, goHome() {
      this.$router.push('/')
    },
    // 跳转至修改用户信息界面
    goUpdate() {
      const access_token = localStorage.getItem('access_token')
      if (!access_token) {
        console.log('No access token found.')
        return
      }
      this.$router.push('/profile/update')
    },
  },
}
</script>
