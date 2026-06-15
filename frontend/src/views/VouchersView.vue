<script setup>
import { computed, onMounted } from 'vue'
import StatusBanner from '../components/StatusBanner.vue'
import { useLoyaltyData } from '../stores/useLoyaltyData'

const { state, refreshAll, fetchBirthdayStatus, issueBirthdayVouchers } = useLoyaltyData()

const isSubmitting = computed(() => state.loading)

const birthdayStatus = computed(() => state.birthdayStatus)

const allIssued = computed(() => birthdayStatus.value?.all_issued === true)

const hasNoBirthdayMembers = computed(() => birthdayStatus.value?.total_birthday_members === 0)

const buttonDisabled = computed(() => isSubmitting.value || allIssued.value || hasNoBirthdayMembers.value)

const issueResult = computed(() => state.birthdayIssueResult)

const isAllSkipped = computed(() => {
  if (!issueResult.value) return false
  return issueResult.value.total_birthday_members > 0 && issueResult.value.issued_count === 0 && issueResult.value.skipped_count > 0
})

onMounted(async () => {
  await refreshAll()
  await fetchBirthdayStatus()
})

async function submitIssue() {
  if (buttonDisabled.value) return
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
        :disabled="buttonDisabled"
        :class="{ 'is-loading': isSubmitting, 'is-done': allIssued }"
        @click="submitIssue"
      >
        <span v-if="isSubmitting">发放中...</span>
        <span v-else-if="allIssued">今日已发放完毕</span>
        <span v-else-if="hasNoBirthdayMembers">今日无生日会员</span>
        <span v-else>发放今日生日礼券</span>
      </button>
      <div v-if="birthdayStatus && !hasNoBirthdayMembers" class="issue-summary">
        <span class="summary-item">今日生日会员：<b>{{ birthdayStatus.total_birthday_members }}</b> 人</span>
        <span v-if="allIssued" class="summary-item done">全部已发放 ✓</span>
        <template v-else-if="birthdayStatus.already_issued_count > 0">
          <span class="summary-item success">已发放：<b>{{ birthdayStatus.already_issued_count }}</b> 张</span>
          <span class="summary-item skipped">待发放：<b>{{ birthdayStatus.total_birthday_members - birthdayStatus.already_issued_count }}</b> 人</span>
        </template>
      </div>
    </div>

    <div v-if="isAllSkipped" class="panel already-issued-notice">
      <h3 class="notice-title">今日生日礼券已发放完毕</h3>
      <p>所有今日生日会员均已在本年度发放过生日礼券，无需重复操作。</p>
    </div>

    <div v-if="issueResult && !isAllSkipped && issueResult.issued.length > 0" class="panel issue-detail-panel success-panel">
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

    <div v-if="issueResult && !isAllSkipped && issueResult.skipped.length > 0" class="panel issue-detail-panel skipped-panel">
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

.primary-button.is-done {
  background: #78909c;
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

.summary-item.done {
  background: #e8f5e9;
  color: #2e7d32;
}

.summary-item.done b {
  color: #1b5e20;
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

.already-issued-notice {
  border-left: 4px solid #1565c0;
  background: #e3f2fd;
}

.notice-title {
  color: #1565c0;
  margin-top: 0;
}

.already-issued-notice p {
  margin-bottom: 0;
  color: #1976d2;
}

.issue-detail-panel {
  border-left: 4px solid;
}

.success-panel {
  border-left-color: #4caf50;
}

.skipped-panel {
  border-left-color: #ff9800;
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
