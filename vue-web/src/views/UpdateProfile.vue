<!-- src\views\UpdateProfile.vue -->
<template>
  <div>
   <el-form ref="updateForm" :model="user" status-icon :rules="rules" @submit.prevent="submitUpdateProfile">
      <el-form-item label="真实姓名" prop="RealName">
        <el-input v-model="user.RealName" />
      </el-form-item>
      <el-form-item label="手机号" prop="Phone">
        <el-input v-model="user.Phone" />
      </el-form-item>
      <el-form-item label="邮箱" prop="Email">
        <el-input v-model="user.Email" />
      </el-form-item>
      <el-form-item label="地址" prop="Address">
        <el-input v-model="user.Address" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" native-type="submit">更新</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>
<script>
import { ElForm, ElFormItem, ElInput, ElButton } from 'element-plus';
import { updateProfile } from '@/api';

export default {
  components: {
    ElForm,
    ElFormItem,
    ElInput,
    ElButton,
  },
  data() {
    return {
      user: {
        RealName: '',
        Phone: '',
        Email: '',
        Address: '',
      },
      rules: {
        RealName: [{ required: true, message: '请输入真实姓名', trigger: 'blur' }],
        Phone: [
          { required: true, message: '请输入手机号', trigger: 'blur' },
          { pattern: /^1[3459]\d{9}$/, message: '手机号格式不正确', trigger: 'blur' },
        ],
        Email: [
          { required: true, message: '请输入邮箱地址', trigger: 'blur' },
          { type: 'email', message: '邮箱格式不正确', trigger: 'blur' },
        ],
        Address: [{ required: true, message: '请输入地址', trigger: 'blur' }],
      },
    };
  },
  methods: {
    submitUpdateProfile() {
      this.$refs.updateForm.validate(valid => {
        if (valid) {
          this.updateProfile();
        } else {
          return false;
        }
      });
    },
    updateProfile() {
      updateProfile(this.user)
        .then(() => {
          this.$message({
            message: '资料更新成功',
            type: 'success',
          });
          this.$router.push('/Profile');
          console.log('user对象填充成功:', this.user)
        })
        .catch(err => {
          console.log(err.message);
          this.$router.push('/');
        });
    },
  },
};

</script>
<!-- <template>
  <div>
    <form @submit.prevent="updateProfile">
      <div>
        <label for="RealName">真实姓名</label>
        <input v-model="user.RealName">
      </div>
      <div>
        <label for="Phone">手机号</label>
        <input v-model="user.Phone"> 
      </div>
      <div>
        <label for="Email">邮箱</label>
        <input v-model="user.Email">
      </div>
      <div>
        <label for="Address">地址</label>
        <input v-model="user.Address">
      </div>
      <button type="submit">更新</button>
    </form>
  </div>
</template>

<script>
import { updateProfile } from '@/api'

export default {
  data() { 
    return {
      user: {}  
    }
  },
  methods: {
    updateProfile() {     
      updateProfile(this.user)
        .then(() => {  
          this.$router.push('/Profile') 
        })
        .catch(err => {
          console.log(err.message)
        })
    }
  }
}
</script> -->
