<!-- UserRegister.vue -->

<template>
  <!-- 用户注册页面 -->
  <el-form :model="data" :rules="rules" ref="form" label-width="100px">
    <el-form-item label="用户名" prop="Username">
      <el-input v-model="data.Username"></el-input>
    </el-form-item>
    <el-form-item label="密码" prop="Password">
      <el-input type="password" v-model="data.Password"></el-input>
    </el-form-item>
    <el-form-item label="确认密码" prop="PasswordConfirm">
      <el-input type="password" v-model="data.PasswordConfirm"></el-input>
    </el-form-item>
    <el-form-item label="身份证号" prop="IDCard">
      <el-input v-model="data.IDCard"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="register('form')">注册</el-button>
      <el-button>取消</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
// 导入axios和注册接口  
import { register } from '@/api'   

export default {
  data() {     
    return {     
      // 用户名、密码、确认密码、身份证号     
      data: {
        Username: '',      
        Password: '',       
        PasswordConfirm: '',
        IDCard: ''    
      },
      // 表单验证规则     
      rules: {
        // 用户名必填         
        Username: [          
          { required: true, message: '请输入用户名', trigger: 'blur' }       
        ],
        // 密码必填、6位以上          
        Password: [           
          { required: true, message: '请输入密码', trigger: 'blur' },          
          { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }         
        ],         
        // 确认密码必填、与密码一致        
        PasswordConfirm: [         
          { required: true, message: '请再次输入密码', trigger: 'blur' },   
          { validator: this.confirmPassword, trigger: 'blur' }          
        ],          
        // 身份证号必填           
        IDCard: [            
          { required: true, message: '请输入身份证号', trigger: 'blur' },   
          { min: 18,max: 18, message: '身份证号为18位', trigger: 'blur' }         
      
        ]    
      }   
    }
  },
  methods: {
    // 确认密码自定义校验方法
    confirmPassword(rule, value, callback) {  
      console.log('调用confirmPassword方法,Password值为:', this.data.Password) 
      console.log('调用confirmPassword方法,PasswordConfirm值为:', value)   
      if (value !== this.data.Password) {
        callback(new Error('两次输入的密码不一致!'))  
        console.log('两次密码输入不一致!')  
      } else {   
        callback()  
        console.log('两次密码输入一致!')  
      }  
    },
    // 注册方法,调用axios发起注册请求
    // register(formName) {    
    //   console.log('调用register方法,formName值为:', formName)    
    //   this.$refs[formName].validate((valid) => { 
    //     if (valid) {     
    //       console.log('表单校验通过,用户名为:', this.data.Username)    
    //       const params = {      
    //         Username: this.data.Username,      
    //         Password: this.data.Password,       
    //         IDCard: this.data.IDCard     
    //       }   
    //       console.log('注册接口请求参数为:', params) 
    //       register(params)   
    //         .then(res => {    
    //           console.log('注册成功,结果为:', res.data.errmsg)  
    //           this.$message.success(res.data.errmsg)  
    //           this.$router.push('/login')  
    //         })   
    //         .catch(err => {    
    //           console.log('注册失败,错误信息为:', err.response.data.errmsg)  
    //           this.$message.error(err.response.data.errmsg)  
    //         })     
    //     } else {     
    //       this.$message.error('注册信息不完整!')  
    //       console.log('表单校验未通过,显示提示信息!')  
    //       return false    
    //     }   
    //  })  
    // }
    register(formName) {   
    this.$refs[formName].validate((valid) => { 
      if (valid) {    
        const params = {      
          Username: this.data.Username,      
          Password: this.data.Password,       
          IDCard: this.data.IDCard    
        } 
      register(params)   
        .then(res => {  
          // this.$message({
          //   message: '注册成功',
          //   type: res.type,
          // });
          console.log('接受到错误结果为:', res.data) 
          if (res.data.errmsg == '用户名已存在'||res.data.errmsg=='参数不完整'||res.data.errmsg=='身份证号已存在') {
            this.$message.error(res.data.errmsg) }
            else{
              this.$message({
            message: '注册成功',
            type: 'success',
          });
          this.$router.push("/login");
        }
          // this.$router.push("/login");

          // if (res.data.errmsg == '用户注册成功') {
          //   this.$message.success(res.data.errmsg)
          //   this.$router.push("/login");

          // } else {
          //   console.log('接受到结果为:', res.data.errmsg) 
          // this.$message.error(res.data.errmsg) 
          // }     
        })
        // .catch(err => {
        //   console.log('接受到错误结果为:', err) 
        // })     
     }
    //   else {    
    //    this.$message.error('注册信息不完整!')    
    //    return false   
    //  }  
   })
  }


  }
}
</script>
