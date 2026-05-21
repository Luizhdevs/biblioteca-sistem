<template>
  <div>
    <div class="page-header">
      <h2>Funcionários</h2>
      <button class="btn btn-primary btn-sm" @click="openCreate">
        <i class="bi bi-person-plus-fill me-1"></i>Novo Funcionário
      </button>
    </div>
    <div class="page-body">
      <div class="table-card">
        <div v-if="loading" class="empty-state"><i class="bi bi-hourglass-split"></i> Carregando...</div>
        <div v-else-if="!items.length" class="empty-state"><i class="bi bi-person-badge"></i> Nenhum funcionário</div>
        <table v-else class="table">
          <thead>
            <tr><th>#</th><th>Nome</th><th>Cargo</th><th>E-mail</th><th>Telefone</th><th>Admissão</th><th>Ações</th></tr>
          </thead>
          <tbody>
            <tr v-for="f in items" :key="f.id_funcionario">
              <td class="text-muted">{{ f.id_funcionario }}</td>
              <td class="fw-semibold">{{ f.nome }}</td>
              <td><span class="badge bg-light text-dark">{{ f.cargo }}</span></td>
              <td>{{ f.email }}</td>
              <td>{{ f.telefone || '—' }}</td>
              <td>{{ fDate(f.data_admissao) }}</td>
              <td>
                <div class="action-btns">
                  <button class="btn btn-outline-primary btn-sm" @click="openEdit(f)"><i class="bi bi-pencil"></i></button>
                  <button class="btn btn-outline-danger btn-sm" @click="del(f)"><i class="bi bi-trash"></i></button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal-box">
        <div class="modal-header">
          <h5>{{ editingId ? 'Editar Funcionário' : 'Novo Funcionário' }}</h5>
          <button class="btn-close" @click="showModal = false"></button>
        </div>
        <div class="modal-body">
          <div class="row g-3">
            <div class="col-12">
              <label class="form-label">Nome *</label>
              <input v-model="form.nome" class="form-control" />
            </div>
            <div class="col-md-6">
              <label class="form-label">Cargo *</label>
              <input v-model="form.cargo" class="form-control" />
            </div>
            <div class="col-md-6">
              <label class="form-label">Telefone</label>
              <input v-model="form.telefone" class="form-control" />
            </div>
            <div class="col-12">
              <label class="form-label">E-mail *</label>
              <input v-model="form.email" type="email" class="form-control" />
            </div>
          </div>
          <div v-if="errorMsg" class="alert alert-danger mt-3 mb-0">{{ errorMsg }}</div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-light" @click="showModal = false">Cancelar</button>
          <button class="btn btn-primary" :disabled="saving" @click="save">
            <span v-if="saving" class="spinner-border spinner-border-sm me-1"></span>
            {{ editingId ? 'Salvar' : 'Cadastrar' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api/index.js'
import { formatDate } from '../utils/formatters.js'

const items = ref([])
const loading = ref(true)
const showModal = ref(false)
const editingId = ref(null)
const saving = ref(false)
const errorMsg = ref('')
const fDate = formatDate

const blank = () => ({ nome: '', cargo: '', telefone: '', email: '' })
const form = ref(blank())

async function load() {
  loading.value = true
  try { items.value = (await api.getFuncionarios()).data }
  finally { loading.value = false }
}

function openCreate() { editingId.value = null; form.value = blank(); errorMsg.value = ''; showModal.value = true }
function openEdit(f) {
  editingId.value = f.id_funcionario
  form.value = { nome: f.nome, cargo: f.cargo, telefone: f.telefone, email: f.email }
  errorMsg.value = ''; showModal.value = true
}

async function save() {
  saving.value = true; errorMsg.value = ''
  try {
    editingId.value
      ? await api.updateFuncionario(editingId.value, form.value)
      : await api.createFuncionario(form.value)
    showModal.value = false; await load()
  } catch (e) { errorMsg.value = e.response?.data?.detail || 'Erro ao salvar' }
  finally { saving.value = false }
}

async function del(f) {
  if (!confirm(`Excluir funcionário "${f.nome}"?`)) return
  try { await api.deleteFuncionario(f.id_funcionario); await load() }
  catch (e) { alert(e.response?.data?.detail || 'Erro ao excluir') }
}

onMounted(load)
</script>
