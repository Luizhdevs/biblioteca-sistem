<template>
  <div>
    <div class="page-header">
      <h2>Autores</h2>
      <button class="btn btn-primary btn-sm" @click="openCreate">
        <i class="bi bi-plus-lg me-1"></i>Novo Autor
      </button>
    </div>
    <div class="page-body">
      <div class="table-card">
        <div v-if="loading" class="empty-state"><i class="bi bi-hourglass-split"></i> Carregando...</div>
        <div v-else-if="!items.length" class="empty-state"><i class="bi bi-person-lines-fill"></i> Nenhum autor</div>
        <table v-else class="table">
          <thead>
            <tr><th>#</th><th>Nome</th><th>Nacionalidade</th><th>Nascimento</th><th>Ações</th></tr>
          </thead>
          <tbody>
            <tr v-for="a in items" :key="a.id_autor">
              <td class="text-muted">{{ a.id_autor }}</td>
              <td class="fw-semibold">{{ a.nome }}</td>
              <td>{{ a.nacionalidade || '—' }}</td>
              <td>{{ fDate(a.data_nascimento) }}</td>
              <td>
                <div class="action-btns">
                  <button class="btn btn-outline-primary btn-sm" @click="openEdit(a)"><i class="bi bi-pencil"></i></button>
                  <button class="btn btn-outline-danger btn-sm" @click="del(a)"><i class="bi bi-trash"></i></button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal-box" style="max-width:440px">
        <div class="modal-header">
          <h5>{{ editingId ? 'Editar Autor' : 'Novo Autor' }}</h5>
          <button class="btn-close" @click="showModal = false"></button>
        </div>
        <div class="modal-body">
          <div class="row g-3">
            <div class="col-12">
              <label class="form-label">Nome *</label>
              <input v-model="form.nome" class="form-control" />
            </div>
            <div class="col-md-6">
              <label class="form-label">Nacionalidade</label>
              <input v-model="form.nacionalidade" class="form-control" />
            </div>
            <div class="col-md-6">
              <label class="form-label">Data de Nascimento</label>
              <input v-model="form.data_nascimento" type="date" class="form-control" />
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

const blank = () => ({ nome: '', nacionalidade: '', data_nascimento: '' })
const form = ref(blank())

async function load() {
  loading.value = true
  try { items.value = (await api.getAutores()).data }
  finally { loading.value = false }
}

function openCreate() { editingId.value = null; form.value = blank(); errorMsg.value = ''; showModal.value = true }
function openEdit(a) {
  editingId.value = a.id_autor
  form.value = { nome: a.nome, nacionalidade: a.nacionalidade, data_nascimento: a.data_nascimento?.split('T')[0] || '' }
  errorMsg.value = ''; showModal.value = true
}

async function save() {
  saving.value = true; errorMsg.value = ''
  try {
    const payload = { ...form.value, data_nascimento: form.value.data_nascimento || null }
    editingId.value ? await api.updateAutor(editingId.value, payload) : await api.createAutor(payload)
    showModal.value = false; await load()
  } catch (e) { errorMsg.value = e.response?.data?.detail || 'Erro ao salvar' }
  finally { saving.value = false }
}

async function del(a) {
  if (!confirm(`Excluir autor "${a.nome}"?`)) return
  try { await api.deleteAutor(a.id_autor); await load() }
  catch (e) { alert(e.response?.data?.detail || 'Erro ao excluir') }
}

onMounted(load)
</script>
