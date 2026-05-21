<template>
  <div>
    <div class="page-header">
      <h2>Dashboard</h2>
    </div>
    <div class="page-body">

      <!-- Stat Cards -->
      <div class="row g-3 mb-4">
        <div class="col-6 col-md-4 col-lg-2" v-for="s in statCards" :key="s.label">
          <div class="stat-card text-center">
            <div class="stat-value" :class="s.color">{{ s.value }}</div>
            <div class="stat-label">{{ s.label }}</div>
          </div>
        </div>
      </div>

      <!-- Recent Loans -->
      <div class="table-card">
        <div class="d-flex align-items-center justify-content-between px-3 py-2 border-bottom">
          <span class="fw-semibold" style="font-size:.9rem">Empréstimos Recentes</span>
        </div>
        <div v-if="loading" class="empty-state"><i class="bi bi-hourglass-split"></i> Carregando...</div>
        <div v-else-if="!loans.length" class="empty-state"><i class="bi bi-inbox"></i> Nenhum empréstimo</div>
        <table v-else class="table">
          <thead>
            <tr>
              <th>Usuário</th><th>Livro</th><th>Emprestado em</th><th>Prazo</th><th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="e in loans" :key="e.id_emprestimo">
              <td>{{ e.nome_usuario }}</td>
              <td>{{ e.titulo_livro }}</td>
              <td>{{ fDate(e.data_emprestimo) }}</td>
              <td>{{ fDate(e.data_prevista_devolucao) }}</td>
              <td>
                <span class="badge badge-status" :class="badge(e.situacao).bg">
                  {{ badge(e.situacao).text }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../api/index.js'
import { formatDate, statusBadge } from '../utils/formatters.js'

const stats = ref({})
const loans = ref([])
const loading = ref(true)

const fDate = formatDate
const badge = statusBadge

const statCards = computed(() => [
  { label: 'Total Livros',        value: stats.value.total_livros ?? '—',         color: 'text-primary' },
  { label: 'Usuários',            value: stats.value.total_usuarios ?? '—',        color: 'text-success' },
  { label: 'Empréstimos Ativos',  value: stats.value.emprestimos_ativos ?? '—',    color: 'text-info' },
  { label: 'Em Atraso',           value: stats.value.emprestimos_atrasados ?? '—', color: 'text-danger' },
  { label: 'Multas Pendentes',    value: stats.value.multas_pendentes ?? '—',      color: 'text-warning' },
  { label: 'Reservas Ativas',     value: stats.value.reservas_ativas ?? '—',       color: 'text-secondary' },
])

onMounted(async () => {
  try {
    const [s, l] = await Promise.all([api.getStats(), api.getEmprestimosRecentes()])
    stats.value = s.data
    loans.value = l.data
  } finally {
    loading.value = false
  }
})
</script>
