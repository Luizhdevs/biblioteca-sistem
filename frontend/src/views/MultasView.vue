<template>
  <div>
    <div class="page-header">
      <h2>Multas</h2>
    </div>
    <div class="page-body">
      <div class="d-flex gap-2 mb-3 flex-wrap">
        <button v-for="f in filters" :key="f.value"
          class="btn btn-sm"
          :class="activeFilter === f.value ? 'btn-dark' : 'btn-outline-secondary'"
          @click="setFilter(f.value)">
          {{ f.label }}
        </button>
      </div>

      <div class="table-card">
        <div v-if="loading" class="empty-state"><i class="bi bi-hourglass-split"></i> Carregando...</div>
        <div v-else-if="!items.length" class="empty-state"><i class="bi bi-receipt"></i> Nenhuma multa encontrada</div>
        <table v-else class="table">
          <thead>
            <tr><th>#</th><th>Usuário</th><th>Livro</th><th>Valor</th><th>Gerada em</th><th>Vencimento</th><th>Pagamento</th><th>Status</th><th>Ações</th></tr>
          </thead>
          <tbody>
            <tr v-for="m in items" :key="m.id_multa">
              <td class="text-muted">{{ m.id_multa }}</td>
              <td>{{ m.nome_usuario }}</td>
              <td>{{ m.titulo_livro }}</td>
              <td class="fw-bold">{{ fCur(m.valor) }}</td>
              <td>{{ fDate(m.data_geracao) }}</td>
              <td :class="isOverdue(m) ? 'text-danger fw-bold' : ''">{{ fDate(m.data_vencimento) }}</td>
              <td>{{ fDate(m.data_pagamento) }}</td>
              <td>
                <span class="badge badge-status" :class="badge(m.status_pagamento).bg">{{ badge(m.status_pagamento).text }}</span>
              </td>
              <td>
                <button v-if="m.status_pagamento === 'PENDENTE'"
                  class="btn btn-success btn-sm" @click="pagar(m)">
                  <i class="bi bi-cash-coin me-1"></i>Pagar
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api/index.js'
import { formatDate, formatCurrency, statusBadge } from '../utils/formatters.js'

const items = ref([])
const loading = ref(true)
const activeFilter = ref('')

const fDate = formatDate
const fCur = formatCurrency
const badge = statusBadge

const filters = [
  { label: 'Todas', value: '' },
  { label: 'Pendentes', value: 'PENDENTE' },
  { label: 'Pagas', value: 'PAGO' },
  { label: 'Canceladas', value: 'CANCELADO' },
]

function isOverdue(m) {
  return m.status_pagamento === 'PENDENTE' && new Date(m.data_vencimento) < new Date()
}

async function load() {
  loading.value = true
  try { items.value = (await api.getMultas({ status: activeFilter.value })).data }
  finally { loading.value = false }
}

function setFilter(v) { activeFilter.value = v; load() }

async function pagar(m) {
  if (!confirm(`Confirmar pagamento da multa #${m.id_multa} no valor de ${fCur(m.valor)}?`)) return
  try { await api.pagarMulta(m.id_multa); await load() }
  catch (e) { alert(e.response?.data?.detail || 'Erro ao pagar') }
}

onMounted(load)
</script>
