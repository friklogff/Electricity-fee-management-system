<!-- <template>
  <div>
    <button @click="getUnpaidBills">获取未付账单</button>
    <button @click="toHome">回首页</button>
    <table>
      <thead>
        <tr>
          <th>账单ID</th>
          <th>用户ID</th>
          <th>应收金额</th>
          <th>账期</th>
          <th>还款状态</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="bill in bills" :key="bill.BillID">
          <td>{{ bill.BillID }}</td>
          <td>{{ bill.UserID }}</td>
          <td>{{ bill.TotalCost }}</td>
          <td>{{ bill.Year }}年{{ bill.Month }}月</td>
          <td>{{ bill.PaidStatus }}</td>
          <td>
            <button @click="toCharge(bill)">收费</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
<script>
import { getClerkUnpaidBills } from '@/api';

export default {
  data() {
    return {
      bills: [],
    };
  },
  methods: {
    getUnpaidBills() {
      console.log('调用获取未付账单方法');
      getClerkUnpaidBills()
        .then((res) => {
          console.log('获取未付账单成功,结果:', res);
          this.bills = res.data.data;
          console.log('bills:', this.bills);
        })
        .catch((err) => {
          console.log('获取未付账单失败,错误:', err);
        });
    },
    toHome() {
      this.$router.push('/');
    },
    // toCharge(bill) {
    //   this.$router.push({
    //     name: 'charge',
    //     // query: { billID: bill.BillID, totalCost: bill.TotalCost },
    //   });
    // },   
     toCharge(bill) {
      const dataToSave = { billID: bill.BillID, totalCost: bill.TotalCost };
    localStorage.setItem("chargeData", JSON.stringify(dataToSave));
    this.$router.push({ name: "charge" });
    },
  },
};
</script> -->
<template>
  <div>
    <el-button type="primary" @click="getUnpaidBills">获取未付账单</el-button>
    <el-button @click="tocHome">回到主页</el-button>
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
          <el-button type="primary" @click="toCharge(row)">收费</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { getClerkUnpaidBills } from '@/api';

export default {
  data() {
    return {
      bills: [],
    };
  },
  methods: {
    getUnpaidBills() {
      console.log('调用获取未付账单方法');
      getClerkUnpaidBills()
        .then((res) => {
          console.log('获取未付账单成功,结果:', res);
          this.bills = res.data.data;
          console.log('bills:', this.bills);
        })
        .catch((err) => {
          console.log('获取未付账单失败,错误:', err);
        });
    },
    tocHome() {
      this.$router.push('/c');
    },
    toCharge(bill) {
      const dataToSave = { billID: bill.BillID, totalCost: bill.TotalCost };
      localStorage.setItem("chargeData", JSON.stringify(dataToSave));
      this.$router.push({ name: "charge" });
    },
  },
};
</script>
