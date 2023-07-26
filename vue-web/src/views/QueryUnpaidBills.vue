<template>
  <div>
    <el-button type="primary" @click="getUnpaidBills">获取你的未付账单</el-button>
    <el-button @click="toHome">回到主页</el-button>
    <el-table :data="bills" style="width: 100%">
      <el-table-column prop="BillID" label="账单ID" width="180"></el-table-column>
      <el-table-column prop="UserID" label="用户ID" width="180"></el-table-column>
      <el-table-column prop="TotalCost" label="应收金额" width="180"></el-table-column>
      <el-table-column
        label="账期"
        width="180"
        header="customHeader"
        :custom-render="{ default: 'customData' }"
      >
        <template v-slot:customData="{ row }">
          {{ row.Year }}年{{ row.Month }}月
        </template>
      </el-table-column>
      <el-table-column prop="PaidStatus" label="还款状态" width="180"></el-table-column>
      <el-table-column label="操作" fixed="right">
        <template v-slot:default="{ row }">
          <el-button type="primary" @click="toPay(row)">支付</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { queryUnpaidBills } from '@/api'

export default {
  data() {
    return {
      bills: []
    }
  },
  methods: {
    getUnpaidBills() {
      console.log('调用获取未付账单方法')
      queryUnpaidBills().then(res => {
        console.log('获取未付账单成功,结果:', res)
        this.bills = res.data.data
        console.log('bills:', this.bills)
      }).catch(err => {
        console.log('获取未付账单失败,错误:', err)
      })
    },
    toHome() {
      this.$router.push('/')
    },
    toPay(bill) {  
      const dataToSave = { billID: bill.BillID, totalCost: bill.TotalCost };
      localStorage.setItem("chargeData", JSON.stringify(dataToSave));
      this.$router.push({ name: "pay" });
      // console.log('跳转到支付路由,传入账单ID:', bill.bill_id)  
      // this.$router.push({
      //   name: 'pay',
      //   params: {
      //     billID: bill.BillID,
      //   }
      // })
    }
  }
}
</script>
