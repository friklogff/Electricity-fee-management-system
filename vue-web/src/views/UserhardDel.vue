<template>
    <div>
      <h1>软删除/硬删除用户</h1>    
      <el-form ref="form" :model="formData" label-width="100px">
        <el-form-item label="用户ID">
          <el-input v-model="formData.user_id"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="danger" @click="hardDeleteUser()">硬删除</el-button>
        </el-form-item>
      </el-form>
    </div>
  </template>

  



<script>
import {  hardDelete } from '@/api';

export default {
  data() {
    return {
      formData: {
        user_id: null,
      },
    };
  },
  methods: {
    async hardDeleteUser() {
      try {
        console.log('硬删除方法开始调用', this.formData);

        await hardDelete({ user_id: this.formData.user_id });

        console.log('硬删除成功', this.formData);

        this.$message({
          message: '硬删除成功！',
          type: 'success',
        });
        // 在这里添加其他代码以更新您的 UI 或进行其他操作
      } catch (err) {
        console.error('硬删除失败', err);

        this.$message({
          message: '硬删除失败！',
          type: 'error',
        });
        // 在这里添加其他代码以更新您的 UI 或进行其他操作
      }
    },
  },
};
</script>


