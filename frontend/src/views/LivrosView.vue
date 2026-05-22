<template>
  <div>
    <div class="page-header">
      <h2>Livros</h2>
      <button class="btn btn-primary btn-sm" @click="openCreate">
        <i class="bi bi-plus-lg me-1"></i>Novo Livro
      </button>
    </div>
    <div class="page-body">

      <!-- Search + Filter -->
      <div class="d-flex gap-2 mb-3 flex-wrap">
        <input v-model="search" @input="loadLivros" class="form-control search-bar"
          placeholder="Buscar por título, ISBN ou gênero..." />
      </div>

      <!-- Table -->
      <div class="table-card">
        <div v-if="loading" class="empty-state"><i class="bi bi-hourglass-split"></i> Carregando...</div>
        <div v-else-if="!livros.length" class="empty-state"><i class="bi bi-book"></i> Nenhum livro encontrado</div>
        <table v-else class="table">
          <thead>
            <tr>
              <th>#</th><th>Título</th><th>ISBN</th><th>Gênero</th><th>Editora</th><th>Autores</th><th>Estoque</th><th>Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="l in livros" :key="l.id_livro">
              <td class="text-muted">{{ l.id_livro }}</td>
              <td class="fw-semibold">{{ l.titulo }}</td>
              <td><small class="text-muted">{{ l.isbn }}</small></td>
              <td><span class="badge bg-light text-dark">{{ l.genero }}</span></td>
              <td>{{ l.nome_editora }}</td>
              <td>
                <small>{{ (l.autores || []).map(a => a.nome).join(', ') || '—' }}</small>
              </td>
              <td>
                <span :class="l.quantidade_estoque > 0 ? 'text-success fw-bold' : 'text-danger fw-bold'">
                  {{ l.quantidade_estoque }}
                </span>
              </td>
              <td>
                <div class="action-btns">
                  <button class="btn btn-outline-primary btn-sm" @click="openEdit(l)" title="Editar">
                    <i class="bi bi-pencil"></i>
                  </button>
                  <button class="btn btn-outline-danger btn-sm" @click="confirmDelete(l)" title="Excluir">
                    <i class="bi bi-trash"></i>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal-box">
        <div class="modal-header">
          <h5>{{ editingId ? 'Editar Livro' : 'Novo Livro' }}</h5>
          <button class="btn-close" @click="showModal = false"></button>
        </div>
        <div class="modal-body">
          <div class="row g-3">
            <div class="col-12">
              <label class="form-label">Título *</label>
              <input v-model="form.titulo" class="form-control" required />
            </div>
            <div class="col-md-6">
              <label class="form-label">ISBN *</label>
              <input v-model="form.isbn" class="form-control" :disabled="!!editingId" />
            </div>
            <div class="col-md-6">
              <label class="form-label">Ano de Publicação *</label>
              <input v-model.number="form.ano_publicacao" type="number" class="form-control" />
            </div>
            <div class="col-md-6">
              <label class="form-label">Editora *</label>
              <select v-model.number="form.id_editora" class="form-select">
                <option value="">Selecione...</option>
                <option v-for="e in editoras" :key="e.id_editora" :value="e.id_editora">{{ e.nome }}</option>
              </select>
            </div>
            <div class="col-md-6">
              <label class="form-label">Gênero *</label>
              <input v-model="form.genero" class="form-control" />
            </div>
            <div class="col-md-6">
              <label class="form-label">Idioma</label>
              <input v-model="form.idioma" class="form-control" />
            </div>
            <div class="col-md-6">
              <label class="form-label">Nº de Páginas</label>
              <input v-model.number="form.numero_paginas" type="number" class="form-control" />
            </div>
            <div class="col-12">
              <label class="form-label">Descrição</label>
              <textarea v-model="form.descricao" class="form-control" rows="2"></textarea>
            </div>
            <template v-if="!editingId">
              <div class="col-md-6">
                <label class="form-label">Qtd. de Exemplares</label>
                <input v-model.number="form.quantidade_exemplares" type="number" min="1" class="form-control" />
              </div>
              <div class="col-md-6">
                <label class="form-label">Localização</label>
                <input v-model="form.localizacao" class="form-control" />
              </div>
            </template>
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

const livros   = ref([])
const editoras = ref([])
const search   = ref('')
const loading  = ref(true)
const showModal = ref(false)
const editingId = ref(null)
const saving   = ref(false)
const errorMsg = ref('')

const defaultForm = () => ({
  titulo: '', isbn: '', ano_publicacao: new Date().getFullYear(),
  id_editora: '', genero: '', idioma: 'Portugues',
  numero_paginas: null, descricao: '',
  quantidade_exemplares: 1, localizacao: 'PRATELEIRA GERAL',
  autores: [],
})
const form = ref(defaultForm())

async function loadLivros() {
  loading.value = true
  try {
    const r = await api.getLivros({ search: search.value })
    livros.value = r.data
  } finally {
    loading.value = false
  }
}

function openCreate() {
  editingId.value = null
  form.value = defaultForm()
  errorMsg.value = ''
  showModal.value = true
}

function openEdit(l) {
  editingId.value = l.id_livro
  form.value = {
    titulo: l.titulo, isbn: l.isbn, ano_publicacao: l.ano_publicacao,
    id_editora: l.id_editora, genero: l.genero, idioma: l.idioma,
    numero_paginas: l.numero_paginas, descricao: l.descricao,
    quantidade_exemplares: 1, localizacao: 'PRATELEIRA GERAL', autores: [],
  }
  errorMsg.value = ''
  showModal.value = true
}

async function save() {
  saving.value = true
  errorMsg.value = ''
  try {
    if (editingId.value) {
      const { quantidade_exemplares, localizacao, autores, isbn, ...payload } = form.value
      await api.updateLivro(editingId.value, payload)
    } else {
      await api.createLivro(form.value)
    }
    showModal.value = false
    await loadLivros()
  } catch (e) {
    errorMsg.value = e.response?.data?.detail || 'Erro ao salvar'
  } finally {
    saving.value = false
  }
}

async function confirmDelete(l) {
  if (!confirm(`Excluir "${l.titulo}"? Esta ação não pode ser desfeita.`)) return
  try {
    await api.deleteLivro(l.id_livro)
    await loadLivros()
  } catch (e) {
    alert(e.response?.data?.detail || 'Erro ao excluir')
  }
}

onMounted(async () => {
  const [, ed] = await Promise.all([loadLivros(), api.getEditoras()])
  editoras.value = ed.data
})
</script>
