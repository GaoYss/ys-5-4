<script setup>
import { computed, onMounted } from 'vue'
import StatusBanner from '../components/StatusBanner.vue'
import { useLoyaltyData } from '../stores/useLoyaltyData'

const { state, refreshAll, issueBirthdayVouchers } = useLoyaltyData()

const isSubmitting = computed(() => state.loading)

const issueResult = computed(() => state.birthdayIssueResult)

onMounted(refreshAll)

async function submitIssue() {
  if (isSubmitting.value) return
  await issueBirthdayVouchers()
}
</script>

<template>
  <section class="view-stack">
    <div class="section-header">
      <div>
        <p class="eyebrow">Birthday</p>
        <h2>生日礼券发放</h2>
      </div>
      <StatusBanner :error="state.error" :notice="state.notice" :loading="state.loading" />
    </div>

    <div class="toolbar-panel">
      <button
        class="primary-button"
        type="button"
        :disabled="isSubmitting"
        :class="{ 'is-loading': isSubmitting }"
        @click="submitIssue"
      >
        <span v-if="isSubmitting">发放中...</span>
        <span v-else>发放今日生日礼券</span>
      </button>
      <div v-if="issueResult" class="issue-summary">
        <span class="summary-item">今日生日会员：<b>{{ issueResult.total_birthday_members }}</b> 人</span>
        <span class="summary-item success">已发放：<b>{{ issueResult.issued_count }}</b> 张</span>
        <span class="summary-item skipped">已跳过：<b>{{ issueResult.skipped_count }}</b> 人</span>
      </div>
    </div>

    <div v-if="issueResult && issueResult.issued.length > 0" class="panel issue-detail-panel">
      <h3 class="success-title">✓ 已发放礼券</h3>
      <div class="data-table">
        <div class="table-head voucher-cols">
          <span>会员</span>
          <span>礼券</span>
          <span>内容</span>
          <span>有效期</span>
          <span>状态</span>
        </div>
        <div v-for="voucher in issueResult.issued" :key="voucher.id" class="table-row voucher-cols">
          <span>{{ voucher.member_name }}</span>
          <span>{{ voucher.title }}</span>
          <span>{{ voucher.value }}</span>
          <span>{{ voucher.expires_at }}</span>
          <span class="status-success">{{ voucher.status }}</span>
        </div>
      </div>
    </div>

    <div v-if="issueResult && issueResult.skipped.length > 0" class="panel issue-detail-panel">
      <h3 class="skipped-title">⊘ 已跳过会员</h3>
      <div class="data-table">
        <div class="table-head skipped-cols">
          <span>会员</span>
          <span>跳过原因</span>
        </div>
        <div v-for="member in issueResult.skipped" :key="member.member_id" class="table-row skipped-cols">
          <span>{{ member.member_name }}</span>
          <span class="skipped-reason">{{ member.reason }}</span>
        </div>
      </div>
    </div>

    <section class="panel">
      <h3>礼券记录</h3>
      <div class="data-table">
        <div class="table-head voucher-cols">
          <span>会员</span>
          <span>礼券</span>
          <span>内容</span>
          <span>有效期</span>
          <span>状态</span>
        </div>
        <div v-for="voucher in state.vouchers" :key="voucher.id" class="table-row voucher-cols">
          <span>{{ voucher.member_name }}</span>
          <span>{{ voucher.title }}</span>
          <span>{{ voucher.value }}</span>
          <span>{{ voucher.expires_at }}</span>
          <span>{{ voucher.status }}</span>
        </div>
      </div>
    </section>
  </section>
</template>

<style scoped>
.toolbar-panel {
  display: flex;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
}

.primary-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.primary-button.is-loading {
  position: relative;
  pointer-events: none;
}

.issue-summary {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.summary-item {
  padding: 6px 12px;
  border-radius: 6px;
  background: #f5f5f5;
  font-size: 14px;
  color: #555;
}

.summary-item b {
  color: #333;
  margin-left: 2px;
}

.summary-item.success {
  background: #e8f5e9;
  color: #2e7d32;
}

.summary-item.success b {
  color: #1b5e20;
}

.summary-item.skipped {
  background: #fff3e0;
  color: #e65100;
}

.summary-item.skipped b {
  color: #bf360c;
}

.issue-detail-panel {
  border-left: 4px solid;
}

.issue-detail-panel:first-of-type {
  margin-top: 0;
}

.success-title {
  color: #2e7d32;
  margin-top: 0;
}

.skipped-title {
  color: #e65100;
  margin-top: 0;
}

.status-success {
  color: #2e7d32;
  font-weight: 500;
}

.skipped-cols {
  grid-template-columns: 1fr 2fr;
}

.skipped-reason {
  color: #e65100;
}

.panel:first-of-type {
  margin-top: 0;
}
</style>
