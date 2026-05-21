<template>
  <div>
    <div class="page-header">
      <h2>Usuários</h2>
      <button class="btn btn-primary btn-sm" @click="openCreate">
        <i class="bi bi-person-plus-fill me-1"></i>Novo Usuário
      </button>
    </div>
    <div class="page-body">
      <div class="d-flex gap-2 mb-3">
        <input v-model="search" @input="load" class="form-control search-bar"
          placeholder="Buscar por nome, CPF ou e-mail..." />
      </div>
      <div class="table-card">
        <div v-if="loading" class="empty-state"><i class="bi bi-hourglass-split"></i> Carregando...</div>
        <div v-else-if="!items.length" class="empty-state"><i class="bi bi-people"></i> Nenhum usuário encontrado</div>
        <table v-else class="table">
          <thead>
            <tr><th>#</th><th>Nome</th><th>CPF</th><th>E-mail</th><th>Telefone</th><th>Cadastro</th><th>Ações</th></tr>
          </thead>
          <tbody>
            <tr v-for="u in items" :key="u.id_usuario">
              <td class="text-muted">{{ u.id_usuario }}</td>
              <td class="fw-semibold">{{ u.nome }}</td>
              <td><small>{{ fCPF(u.cpf) }}</small></td>
              <td>{{ u.email }}</td>
              <td>{{ u.telefone || '—' }}</td>
              <td>{{ fDate(u.data_cadastro) }}</td>
              <td>
                <div class="action-btns">
                  <button class="btn btn-outline-primary btn-sm" @click="openEdit(u)"><i class="bi bi-pencil"></i></button>
                  <button class="btn btn-outline-danger btn-sm" @click="del(u)"><i class="bi bi-trash"></i></button>
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
          <h5>{{ editingId ? 'Editar Usuário' : 'Novo Usuário' }}</h5>
          <button class="btn-close" @click="showModal = false"></button>
        </div>
        <div class="modal-body">
          <div class="row g-3">
            <div class="col-12">
              <label class="form-label">Nome *</label>
              <input v-model="form.nome" class="form-control" />
            </div>
            <div class="col-md-6">
              <label class="form-label">CPF * <small class="text-muted">(somente números)</small></label>
              <input v-model="form.cpf" class="form-control" :disabled="!!editingId" maxlength="14" />
            </div>
            <div class="col-md-6">
              <label class="form-label">Telefone</label>
              <input v-model="form.telefone" class="form-control" />
            </div>
            <div class="col-12">
              <label class="form-label">E-mail *</label>
              <input v-model="form.email" type="email" class="form-control" />
            </div>
            <div class="col-12">
              <label class="form-label">Endereço *</label>
              <input v-model="form.endereco" class="form-control" />
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
import { formatDate, formatCPF } from '../utils/formatters.js'

const items = ref([])
const search = ref('')
const loading = ref(true)
const showModal = ref(false)
const editingId = ref(null)
const saving = ref(false)
const errorMsg = ref('')

const fDate = formatDate
const fCPF = formatCPF

const blank = () => ({ nome: '', cpf: '', endereco: '', telefone: '', email: '' })
const form = ref(blank())

async function load() {
  loading.value = true
  try { items.value = (await api.getUsuarios({ search: search.value })).data }
  finally { loading.value = false }
}

function openCreate() { editingId.value = null; form.value = blank(); errorMsg.value = ''; showModal.value = true }
function openEdit(u) {
  editingId.value = u.id_usuario
  form.value = { nome: u.nome, cpf: u.cpf, endereco: u.endereco, telefone: u.telefone, email: u.email }
  errorMsg.value = ''; showModal.value = true
}

async function save() {
  saving.value = true; errorMsg.value = ''
  try {
    if (editingId.value) {
      const { cpf, ...payload } = form.value
      await api.updateUsuario(editingId.value, payload)
    } else {
      await api.createUsuario(form.value)
    }
    showModal.value = false; await load()
  } catch (e) { errorMsg.value = e.response?.data?.detail || 'Erro ao salvar' }
  finally { saving.value = false }
}

async function del(u) {
  if (!confirm(`Excluir usuário "${u.nome}"?`)) return
  try { await api.deleteUsuario(u.id_usuario); await load() }
  catch (e) { alert(e.response?.data?.detail || 'Erro ao excluir') }
}

onMounted(load)
</script>
