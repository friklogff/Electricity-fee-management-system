<!-- <template>
  <div>
    <h2>职员收费页面</h2>
    <form @submit.prevent="chargeBill" novalidate>
      <p>账单ID: {{ billId }}</p>
      <p>应收金额: {{ totalCost }}</p>
      <input
        type="number"
        placeholder="输入实收金额"
        v-model="paidFee"
    />
      <div v-if="errorMsg" class="error">{{ errorMsg }}</div>
      <button type="submit">收费</button>
    </form>
  </div>
</template>
<script>
import { clerkCharge } from '@/api';

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
      clerkCharge(data)
        .then((res) => {
          console.log('收费成功', res);
          this.errorMsg = '';
        })
        .catch((err) => {
          console.log('收费失败', err);
        });
    },
    validatePaidFee() {
      if (parseFloat(this.paidFee).toFixed(1) !== parseFloat(this.totalCost).toFixed(1)) {
        this.errorMsg = '收费金额和账单金额不一致，请重新输入';
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
</style> -->
<template>
  <div>
    <h2>职员收费页面</h2>
    <el-form @submit.prevent="chargeBill" novalidate>
      <p>账单ID: {{ billId }}</p>
      <p>应收金额: {{ totalCost }}</p>
      <el-input type="number" placeholder="输入实收金额" v-model="paidFee" />
      <div v-if="errorMsg" class="error">{{ errorMsg }}</div>
      <el-button type="primary" native-type="submit">收费</el-button>
    </el-form>
  </div>
</template>

<script>
import { clerkCharge } from "@/api";

export default {
  data() {
    const receivedData = JSON.parse(localStorage.getItem("chargeData"));
    return {
      billId: receivedData.billID,
      totalCost: receivedData.totalCost,
      paidFee: "",
      errorMsg: "",
    };
  },

  methods: {
    async chargeBill() {
      if (!this.validatePaidFee()) {
        return;
      }
      const data = {
        bill_id: this.billId,
        paid_fee: this.paidFee,
      };
      try {
        const res = await clerkCharge(data);
        console.log("收费成功", res);
        this.$message({
            message: '收费成功',
            type: 'success',
          });
        this.$router.push('/c');
      } catch (err) {
        console.log("收费失败", err);
      }
    },

    validatePaidFee() {
      if (
        parseFloat(this.paidFee).toFixed(1) !==
        parseFloat(this.totalCost).toFixed(1)
      ) {
        this.errorMsg = "收费金额和账单金额不一致，请重新输入";
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
