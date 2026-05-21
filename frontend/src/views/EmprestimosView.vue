<template>
  <div>
    <div class="page-header">
      <h2>Empréstimos</h2>
      <button class="btn btn-primary btn-sm" @click="openCreate">
        <i class="bi bi-plus-lg me-1"></i>Registrar Empréstimo
      </button>
    </div>
    <div class="page-body">

      <!-- Filters -->
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
        <div v-else-if="!items.length" class="empty-state"><i class="bi bi-arrow-left-right"></i> Nenhum empréstimo</div>
        <table v-else class="table">
          <thead>
            <tr><th>#</th><th>Usuário</th><th>Livro</th><th>Exemplar</th><th>Emprestado</th><th>Prazo</th><th>Devolução</th><th>Status</th><th>Ações</th></tr>
          </thead>
          <tbody>
            <tr v-for="e in items" :key="e.id_emprestimo">
              <td class="text-muted">{{ e.id_emprestimo }}</td>
              <td>{{ e.nome_usuario }}</td>
              <td>{{ e.titulo_livro }}</td>
              <td><small class="text-muted">{{ e.codigo_exemplar }}</small></td>
              <td>{{ fDate(e.data_emprestimo) }}</td>
              <td :class="isOverdue(e) ? 'text-danger fw-bold' : ''">{{ fDate(e.data_prevista_devolucao) }}</td>
              <td>{{ fDate(e.data_real_devolucao) }}</td>
              <td>
                <span class="badge badge-status" :class="badge(e.situacao).bg">{{ badge(e.situacao).text }}</span>
              </td>
              <td>
                <div class="action-btns">
                  <button v-if="e.situacao === 'ATIVO'"
                    class="btn btn-outline-success btn-sm" title="Devolver"
                    @click="devolver(e)">
                    <i class="bi bi-check2-circle"></i>
                  </button>
                  <button v-if="e.situacao === 'ATIVO'"
                    class="btn btn-outline-warning btn-sm" title="Renovar"
                    @click="openRenovar(e)">
                    <i class="bi bi-arrow-repeat"></i>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Create Modal -->
    <div v-if="showCreate" class="modal-overlay" @click.self="showCreate = false">
      <div class="modal-box">
        <div class="modal-header">
          <h5>Registrar Empréstimo</h5>
          <button class="btn-close" @click="showCreate = false"></button>
        </div>
        <div class="modal-body">
          <div class="row g-3">
            <div class="col-12">
              <label class="form-label">Usuário *</label>
              <select v-model.number="createForm.id_usuario" class="form-select">
                <option value="">Selecione...</option>
                <option v-for="u in usuarios" :key="u.id_usuario" :value="u.id_usuario">{{ u.nome }}</option>
              </select>
            </div>
            <div class="col-12">
              <label class="form-label">Funcionário *</label>
              <select v-model.number="createForm.id_funcionario" class="form-select">
                <option value="">Selecione...</option>
                <option v-for="f in funcionarios" :key="f.id_funcionario" :value="f.id_funcionario">{{ f.nome }}</option>
              </select>
            </div>
            <div class="col-12">
              <label class="form-label">Exemplar *</label>
              <select v-model.number="createForm.id_exemplar" class="form-select">
                <option value="">Selecione...</option>
                <option v-for="ex in exemplares" :key="ex.id_exemplar" :value="ex.id_exemplar">
                  {{ ex.codigo_exemplar }} — {{ ex.titulo_livro }}
                </option>
              </select>
            </div>
            <div class="col-md-6">
              <label class="form-label">Prazo (dias)</label>
              <input v-model.number="createForm.dias_prazo" type="number" min="1" class="form-control" />
            </div>
            <div class="col-12">
              <label class="form-label">Observações</label>
              <textarea v-model="createForm.observacoes" class="form-control" rows="2"></textarea>
            </div>
          </div>
          <div v-if="errorMsg" class="alert alert-danger mt-3 mb-0">{{ errorMsg }}</div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-light" @click="showCreate = false">Cancelar</button>
          <button class="btn btn-primary" :disabled="saving" @click="saveEmprestimo">
            <span v-if="saving" class="spinner-border spinner-border-sm me-1"></span>Registrar
          </button>
        </div>
      </div>
    </div>

    <!-- Renovar Modal -->
    <div v-if="showRenovar" class="modal-overlay" @click.self="showRenovar = false">
      <div class="modal-box" style="max-width:360px">
        <div class="modal-header">
          <h5>Renovar Empréstimo #{{ renovarId }}</h5>
          <button class="btn-close" @click="showRenovar = false"></button>
        </div>
        <div class="modal-body">
          <label class="form-label">Dias adicionais</label>
          <input v-model.number="diasRenovar" type="number" min="1" class="form-control" />
          <div v-if="errorMsg" class="alert alert-danger mt-3 mb-0">{{ errorMsg }}</div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-light" @click="showRenovar = false">Cancelar</button>
          <button class="btn btn-warning" :disabled="saving" @click="saveRenovar">
            <span v-if="saving" class="spinner-border spinner-border-sm me-1"></span>Renovar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api/index.js'
import { formatDate, statusBadge } from '../utils/formatters.js'

const items       = ref([])
const usuarios    = ref([])
const funcionarios = ref([])
const exemplares  = ref([])
const loading     = ref(true)
const saving      = ref(false)
const errorMsg    = ref('')
const activeFilter = ref('')
const showCreate  = ref(false)
const showRenovar = ref(false)
const renovarId   = ref(null)
const diasRenovar = ref(7)

const fDate = formatDate
const badge = statusBadge

const filters = [
  { label: 'Todos', value: '' },
  { label: 'Ativos', value: 'ATIVO' },
  { label: 'Devolvidos', value: 'DEVOLVIDO' },
  { label: 'Atrasados', value: 'ATRASADO' },
]

const createForm = ref({ id_usuario: '', id_funcionario: '', id_exemplar: '', dias_prazo: 15, observacoes: '' })

function isOverdue(e) {
  return e.situacao === 'ATIVO' && new Date(e.data_prevista_devolucao) < new Date()
}

async function load() {
  loading.value = true
  try { items.value = (await api.getEmprestimos({ situacao: activeFilter.value })).data }
  finally { loading.value = false }
}

function setFilter(v) { activeFilter.value = v; load() }

async function openCreate() {
  if (!usuarios.value.length) {
    const [u, f, ex] = await Promise.all([
      api.getUsuarios(), api.getFuncionarios(),
      api.getExemplares({ situacao: 'DISPONIVEL' })
    ])
    usuarios.value = u.data; funcionarios.value = f.data; exemplares.value = ex.data
  }
  createForm.value = { id_usuario: '', id_funcionario: '', id_exemplar: '', dias_prazo: 15, observacoes: '' }
  errorMsg.value = ''; showCreate.value = true
}

async function saveEmprestimo() {
  saving.value = true; errorMsg.value = ''
  try {
    await api.registrarEmprestimo(createForm.value)
    showCreate.value = false; await load()
    exemplares.value = (await api.getExemplares({ situacao: 'DISPONIVEL' })).data
  } catch (e) { errorMsg.value = e.response?.data?.detail || 'Erro ao registrar' }
  finally { saving.value = false }
}

async function devolver(e) {
  if (!confirm(`Registrar devolução do empréstimo #${e.id_emprestimo}?`)) return
  try { await api.devolverEmprestimo(e.id_emprestimo); await load() }
  catch (err) { alert(err.response?.data?.detail || 'Erro ao devolver') }
}

function openRenovar(e) {
  renovarId.value = e.id_emprestimo; diasRenovar.value = 7; errorMsg.value = ''; showRenovar.value = true
}

async function saveRenovar() {
  saving.value = true; errorMsg.value = ''
  try {
    await api.renovarEmprestimo(renovarId.value, { dias_adicionais: diasRenovar.value })
    showRenovar.value = false; await load()
  } catch (e) { errorMsg.value = e.response?.data?.detail || 'Erro ao renovar' }
  finally { saving.value = false }
}

onMounted(load)
</script>
