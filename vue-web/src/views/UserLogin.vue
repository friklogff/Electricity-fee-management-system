<!-- 
<template>
  <form @submit.prevent="submitLogin">
    <div>
      <label for="Username">用户名</label>
      <input v-model="user.Username" name="Username">
    </div>
    <div>
      <label for="Password">密码</label>
      <input v-model="user.Password" name="Password" type="password">
    </div>
    <button type="submit">登录</button>
  </form>
</template>

<script>
import { login } from '@/api'
import jwt_decode from 'jwt-decode'

export default {
  data() {
    return {
      user: {
        Username: '',
        Password: ''
      }
    }
  },
  methods: {
    async login() {
      console.log('login 方法被调用')
      try {
        if (!this.user.Username || !this.user.Password) {
          throw new Error('请输入用户名和密码')
        }
        console.log('发起登录请求')
        const res = await login(this.user)
        console.log('登录请求成功,获取响应结果')
        if (res.data && res.data.access_token) {
          // 存储token  
          localStorage.setItem('access_token', res.data.access_token)
          console.log(`用户 ${this.user.Username} 登录成功!access_token ${res.data.access_token} 已存储`)
 
          const accessToken = localStorage.getItem('access_token')
          const claims = jwt_decode(accessToken, 'secret')
          console.log('claims:', claims)
          const role = claims.privilege
          if (role == 1 || role ==0) {  
            this.$router.push({ path: '/c' })
          }
          else{
            this.$router.push({ path: '/profile' })
          }
          
        } else {
          console.log(`用户 ${this.user.Username} 登录失败,请检查用户名 ${this.user.Username} 和密码`)
        } 
      } catch (err) {
        console.log(err.message)
      }
    },
    submitLogin() {
      console.log('submitLogin 方法被调用')
      this.login()
    }
  }
}
</script> -->
<template>
  <el-form @submit.prevent="submitLogin" ref="LoginForm">
    <el-form-item label="用户名" prop="Username">
      <el-input v-model="user.Username" name="Username"></el-input>
    </el-form-item>
    <el-form-item label="密码" prop="Password">
      <el-input
        v-model="user.Password"
        name="Password"
        type="password"
      ></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" native-type="submit">登录</el-button>
    </el-form-item>
  </el-form>
</template>


<script>
import { login } from "@/api";
import jwt_decode from "jwt-decode";

export default {
  data() {
    return {
      user: {
        Username: "",
        Password: "",
      },
    };
  },
  methods: {
    async login() {
      console.log("login 方法被调用");
      if (!this.user.Username || !this.user.Password) {
        this.$message.error("请输入用户名和密码");
        return;
      }
      console.log("发起登录请求");
      try {
        const res = await login(this.user);
        console.log("登录请求成功,获取响应结果");

        if (res.data && res.data.access_token) {
          localStorage.setItem("access_token", res.data.access_token);
          console.log(
            `用户 ${this.user.Username} 登录成功!access_token ${res.data.access_token} 已存储`
          );

          const accessToken = localStorage.getItem("access_token");
          const claims = jwt_decode(accessToken, "secret");
          console.log("claims:", claims);

          const role = claims.privilege;
          if (role === 1 || role === 0) {
            this.$router.push({ path: "/c" });
          } else {
            this.$router.push({ path: "/profile" });
          }
        } else {
          this.$message.error(
            `用户 ${this.user.Username} 登录失败,请检查用户名与密码`
          );
        }
      } catch (err) {
        console.log(err.message);
      }
    },
    submitLogin() {
      console.log("submitLogin 方法被调用");
      this.login();
    },
  },
};
</script>
