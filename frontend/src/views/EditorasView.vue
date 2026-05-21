<template>
  <div>
    <div class="page-header">
      <h2>Editoras</h2>
      <button class="btn btn-primary btn-sm" @click="openCreate">
        <i class="bi bi-plus-lg me-1"></i>Nova Editora
      </button>
    </div>
    <div class="page-body">
      <div class="table-card">
        <div v-if="loading" class="empty-state"><i class="bi bi-hourglass-split"></i> Carregando...</div>
        <div v-else-if="!items.length" class="empty-state"><i class="bi bi-shop"></i> Nenhuma editora</div>
        <table v-else class="table">
          <thead>
            <tr><th>#</th><th>Nome</th><th>E-mail</th><th>Telefone</th><th>Endereço</th><th>Ações</th></tr>
          </thead>
          <tbody>
            <tr v-for="e in items" :key="e.id_editora">
              <td class="text-muted">{{ e.id_editora }}</td>
              <td class="fw-semibold">{{ e.nome }}</td>
              <td>{{ e.email || '—' }}</td>
              <td>{{ e.telefone || '—' }}</td>
              <td>{{ e.endereco || '—' }}</td>
              <td>
                <div class="action-btns">
                  <button class="btn btn-outline-primary btn-sm" @click="openEdit(e)"><i class="bi bi-pencil"></i></button>
                  <button class="btn btn-outline-danger btn-sm" @click="del(e)"><i class="bi bi-trash"></i></button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal-box" style="max-width:480px">
        <div class="modal-header">
          <h5>{{ editingId ? 'Editar Editora' : 'Nova Editora' }}</h5>
          <button class="btn-close" @click="showModal = false"></button>
        </div>
        <div class="modal-body">
          <div class="row g-3">
            <div class="col-12">
              <label class="form-label">Nome *</label>
              <input v-model="form.nome" class="form-control" />
            </div>
            <div class="col-md-6">
              <label class="form-label">E-mail</label>
              <input v-model="form.email" type="email" class="form-control" />
            </div>
            <div class="col-md-6">
              <label class="form-label">Telefone</label>
              <input v-model="form.telefone" class="form-control" />
            </div>
            <div class="col-12">
              <label class="form-label">Endereço</label>
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

const items = ref([])
const loading = ref(true)
const showModal = ref(false)
const editingId = ref(null)
const saving = ref(false)
const errorMsg = ref('')

const blank = () => ({ nome: '', email: '', telefone: '', endereco: '' })
const form = ref(blank())

async function load() {
  loading.value = true
  try { items.value = (await api.getEditoras()).data }
  finally { loading.value = false }
}

function openCreate() { editingId.value = null; form.value = blank(); errorMsg.value = ''; showModal.value = true }
function openEdit(e) {
  editingId.value = e.id_editora
  form.value = { nome: e.nome, email: e.email, telefone: e.telefone, endereco: e.endereco }
  errorMsg.value = ''; showModal.value = true
}

async function save() {
  saving.value = true; errorMsg.value = ''
  try {
    editingId.value ? await api.updateEditora(editingId.value, form.value) : await api.createEditora(form.value)
    showModal.value = false; await load()
  } catch (e) { errorMsg.value = e.response?.data?.detail || 'Erro ao salvar' }
  finally { saving.value = false }
}

async function del(e) {
  if (!confirm(`Excluir editora "${e.nome}"?`)) return
  try { await api.deleteEditora(e.id_editora); await load() }
  catch (e) { alert(e.response?.data?.detail || 'Erro ao excluir') }
}

onMounted(load)
</script>
