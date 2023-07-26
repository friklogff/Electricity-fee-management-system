
<template>
  <div>
    <h2>网上支付</h2>
    <el-form @submit.prevent="chargeBill" novalidate>
      <p>账单ID: {{ billId }}</p>
      <p>应付金额: {{ totalCost }}</p>
      <el-input type="number" placeholder="输入缴费金额" v-model="paidFee" />
      <div v-if="errorMsg" class="error">{{ errorMsg }}</div>
      <el-button type="primary" native-type="submit">支付</el-button>
    </el-form>
  </div>
</template>

<script>
import { makePayment } from '@/api'

export default {
  data() {
    const receivedData = JSON.parse(localStorage.getItem("chargeData"));
    return {
      billId: receivedData.billID,
      totalCost: receivedData.totalCost,
      paidFee: '',
      errorMsg: '',
    };
  },

  methods: {
    chargeBill() {
      if (!this.validatePaidFee()) {
        return;
      }
      const data = {
        bill_id: this.billId,
        paid_fee: this.paidFee,
      };
      makePayment(data)
        .then((res) => {
          console.log('支付成功', res);
          this.$message({
            message: '支付成功',
            type: 'success',
          });
          this.$router.push("/");

        })
        .catch((err) => {
          console.log('支付失败', err);
        });
    },
    validatePaidFee() {
      if (parseFloat(this.paidFee).toFixed(1) !== parseFloat(this.totalCost).toFixed(1)) {
        this.errorMsg = '支付金额和账单金额不一致，请重新输入';
        return false;
      }
      return true;
    },
  },
    mounted() {
    localStorage.removeItem("chargeData");
  },
};
</script>

<style scoped>
.error {
  color: red;
}
</style>
