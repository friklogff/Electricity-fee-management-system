<template>
  <div>
     <h1>软删除用户</h1>
     <el-form ref="form" :model="formData" label-width="100px">
       <el-form-item label="用户ID">
         <el-input v-model="formData.user_id"></el-input>
       </el-form-item>
       <el-form-item>
         <el-button type="danger" @click="softDeleteUser()">软删除</el-button>
       </el-form-item>
     </el-form>
   </div>
 </template>
 
 <script>
 import { softDelete } from '@/api';
 
 export default {
   data() {
     return {
       formData: {
         user_id: '',
       },
     };
   },
   methods: {
     async softDeleteUser() {
       try {
         console.log('软删除方法开始调用', this.formData);
 
         await softDelete({ user_id: this.formData.user_id });
 
         console.log('软删除成功', this.formData);
 
         this.$message({
           message: '软删除成功！',
           type: 'success',
         });
         this.$router.push("/c");

         // 在这里添加其他代码以更新您的 UI 或进行其他操作
       } catch (err) {
         console.error('软删除失败', err);
 
         this.$message({
           message:'不存在该用户软删除失败！',
           type: 'error',
         });
         // 在这里添加其他代码以更新您的 UI 或进行其他操作
       }
     },
   },
 };
 </script>
 