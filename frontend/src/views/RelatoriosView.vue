<template>
  <div>
    <div class="page-header">
      <h2>Relatórios</h2>
    </div>
    <div class="page-body">

      <!-- Tabs -->
      <ul class="nav nav-tabs mb-4">
        <li class="nav-item" v-for="t in tabs" :key="t.key">
          <button class="nav-link" :class="{ active: activeTab === t.key }" @click="setTab(t.key)">
            <i :class="t.icon + ' me-1'"></i>{{ t.label }}
          </button>
        </li>
      </ul>

      <!-- Inadimplência -->
      <div v-if="activeTab === 'inadimplencia'">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <span class="text-muted">Usuários com multas pendentes</span>
          <button class="btn btn-outline-secondary btn-sm" @click="loadInadimplencia">
            <i class="bi bi-arrow-clockwise me-1"></i>Atualizar
          </button>
        </div>
        <div class="table-card">
          <div v-if="loadingTab" class="empty-state"><i class="bi bi-hourglass-split"></i> Carregando...</div>
          <div v-else-if="!inadimplencia.length" class="empty-state"><i class="bi bi-check-circle"></i> Nenhum inadimplente</div>
          <table v-else class="table">
            <thead>
              <tr><th>Usuário</th><th>E-mail</th><th>Livro</th><th>Valor</th><th>Vencimento</th><th>Dias Vencidos</th></tr>
            </thead>
            <tbody>
              <tr v-for="(r, i) in inadimplencia" :key="i">
                <td class="fw-semibold">{{ r.usuario }}</td>
                <td>{{ r.email }}</td>
                <td>{{ r.livro }}</td>
                <td class="text-danger fw-bold">{{ fCur(r.valor) }}</td>
                <td class="text-danger">{{ fDate(r.data_vencimento) }}</td>
                <td>
                  <span class="badge bg-danger">{{ r.dias_vencidos }} dias</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Livros Disponíveis -->
      <div v-if="activeTab === 'livros'">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <span class="text-muted">Exemplares disponíveis para empréstimo</span>
          <button class="btn btn-outline-secondary btn-sm" @click="loadLivros">
            <i class="bi bi-arrow-clockwise me-1"></i>Atualizar
          </button>
        </div>
        <div class="table-card">
          <div v-if="loadingTab" class="empty-state"><i class="bi bi-hourglass-split"></i> Carregando...</div>
          <div v-else-if="!livrosDisp.length" class="empty-state"><i class="bi bi-book"></i> Nenhum disponível</div>
          <table v-else class="table">
            <thead><tr><th>#</th><th>Título</th><th>Código do Exemplar</th><th>Situação</th></tr></thead>
            <tbody>
              <tr v-for="(r, i) in livrosDisp" :key="i">
                <td class="text-muted">{{ r.id_livro }}</td>
                <td>{{ r.titulo }}</td>
                <td><small class="text-muted">{{ r.codigo_exemplar }}</small></td>
                <td><span class="badge bg-success">Disponível</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Multas Pendentes -->
      <div v-if="activeTab === 'multas'">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <span class="text-muted">Multas pendentes de pagamento</span>
          <button class="btn btn-outline-secondary btn-sm" @click="loadMultas">
            <i class="bi bi-arrow-clockwise me-1"></i>Atualizar
          </button>
        </div>
        <div class="table-card">
          <div v-if="loadingTab" class="empty-state"><i class="bi bi-hourglass-split"></i> Carregando...</div>
          <div v-else-if="!multasPend.length" class="empty-state"><i class="bi bi-check-circle"></i> Sem multas pendentes</div>
          <table v-else class="table">
            <thead><tr><th>#</th><th>Usuário</th><th>Livro</th><th>Valor</th><th>Vencimento</th></tr></thead>
            <tbody>
              <tr v-for="(r, i) in multasPend" :key="i">
                <td class="text-muted">{{ r.id_multa }}</td>
                <td>{{ r.usuario }}</td>
                <td>{{ r.livro }}</td>
                <td class="fw-bold text-warning">{{ fCur(r.valor) }}</td>
                <td>{{ fDate(r.data_vencimento) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api/index.js'
import { formatDate, formatCurrency } from '../utils/formatters.js'

const activeTab = ref('inadimplencia')
const loadingTab = ref(false)
const inadimplencia = ref([])
const livrosDisp    = ref([])
const multasPend    = ref([])

const fDate = formatDate
const fCur  = formatCurrency

const tabs = [
  { key: 'inadimplencia', label: 'Inadimplência',       icon: 'bi bi-exclamation-triangle' },
  { key: 'livros',        label: 'Livros Disponíveis',   icon: 'bi bi-book' },
  { key: 'multas',        label: 'Multas Pendentes',     icon: 'bi bi-receipt' },
]

async function setTab(key) {
  activeTab.value = key
  if (key === 'inadimplencia' && !inadimplencia.value.length) await loadInadimplencia()
  if (key === 'livros'        && !livrosDisp.value.length)    await loadLivros()
  if (key === 'multas'        && !multasPend.value.length)    await loadMultas()
}

async function loadInadimplencia() {
  loadingTab.value = true
  try { inadimplencia.value = (await api.getInadimplencia()).data }
  finally { loadingTab.value = false }
}

async function loadLivros() {
  loadingTab.value = true
  try { livrosDisp.value = (await api.getLivrosDisponiveis()).data }
  finally { loadingTab.value = false }
}

async function loadMultas() {
  loadingTab.value = true
  try { multasPend.value = (await api.getMultasPendentes()).data }
  finally { loadingTab.value = false }
}

onMounted(loadInadimplencia)
</script>
