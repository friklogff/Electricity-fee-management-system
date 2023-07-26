<!-- <template>
  <div>
    <form @submit.prevent="generateUnpaidBill">
      <div>
        <label for="year">Year:</label> 
        <input id="year" v-model="unpaidBillForm.year">
      </div>
      <div>
        <label for="month">Month:</label> 
        <input id="month" v-model="unpaidBillForm.month">
      </div>
      <button type="submit">Generate Unpaid Bill</button>
    </form>
  </div>
</template>


<script>
import { generateUnpaidBill } from '@/api'


export default {
  data() {
    return {
      unpaidBillForm: {
        year: '',
        month: ''  
      }
    }
  },
  methods: {
    generateUnpaidBill() {   
      // 获取 access_token  
      const accessToken = localStorage.getItem('access_token')  

      // 调用方法,传入 accessToken  
      generateUnpaidBill(this.unpaidBillForm, accessToken)  
        .then(res => {
          alert(res.data.errmsg)
        })
        .catch(err => {
          if (err === '权限不足,无法生成未付账单') {
            alert(err)
          } else {
            alert('Generate unpaid bill failed. Please try again!')
          }
        })
    }
  }
}
</script> -->

<template>
  <div>
      <el-form @submit.prevent="generateUnpaidBill">
          <el-form-item label="年份：" prop="year">
              <el-input id="year" v-model="unpaidBillForm.year"></el-input>
          </el-form-item>
          <el-form-item label="月份：" prop="month">
              <el-input id="month" v-model="unpaidBillForm.month"></el-input>
          </el-form-item>
          <el-form-item>
              <el-button type="primary" native-type="submit">生成未付账单</el-button>
          </el-form-item>
      </el-form>
  </div>
</template>

<script>
import { generateUnpaidBill } from '@/api'

export default {
  data() {
    return {
      unpaidBillForm: {
        year: '',
        month: ''
      }
    }
  },
  methods: {
    generateUnpaidBill() {
      // 获取 access_token
      const accessToken = localStorage.getItem('access_token')

      // 调用方法,传入 accessToken
      generateUnpaidBill(this.unpaidBillForm, accessToken)
        .then(res => {
          if (res.data.errmsg === '生成成功') {
            this.$message.success(res.data.errmsg)
            this.$message({
           message: '生成成功',
           type: 'success',
         });
            this.$router.push("/c");

          } else {
            this.$message.error('生成未付账单失败，请重试！')
            // this.$router.push("/c");

          }
        })
        .catch(err => {
          if (err === '权限不足,无法生成未付单') {
            this.$message.error(err)
            this.$router.push("/c");

          } 
        })
    }
  }
}
</script>
