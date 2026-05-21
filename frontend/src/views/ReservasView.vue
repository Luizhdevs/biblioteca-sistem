<template>
  <div>
    <div class="page-header">
      <h2>Reservas</h2>
      <button class="btn btn-primary btn-sm" @click="openCreate">
        <i class="bi bi-bookmark-plus me-1"></i>Nova Reserva
      </button>
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
        <div v-else-if="!items.length" class="empty-state"><i class="bi bi-bookmark"></i> Nenhuma reserva</div>
        <table v-else class="table">
          <thead>
            <tr><th>#</th><th>Usuário</th><th>Livro</th><th>Reservado em</th><th>Validade</th><th>Status</th><th>Ações</th></tr>
          </thead>
          <tbody>
            <tr v-for="r in items" :key="r.id_reserva">
              <td class="text-muted">{{ r.id_reserva }}</td>
              <td>{{ r.nome_usuario }}</td>
              <td>{{ r.titulo_livro }}</td>
              <td>{{ fDate(r.data_reserva) }}</td>
              <td>{{ fDate(r.data_validade) }}</td>
              <td>
                <span class="badge badge-status" :class="badge(r.status).bg">{{ badge(r.status).text }}</span>
              </td>
              <td>
                <div class="action-btns">
                  <button v-if="r.status === 'ATIVA'" class="btn btn-outline-success btn-sm"
                    title="Atender reserva" @click="openAtender(r)">
                    <i class="bi bi-check2-circle"></i>
                  </button>
                  <button v-if="r.status === 'ATIVA'" class="btn btn-outline-danger btn-sm"
                    title="Cancelar" @click="cancelar(r)">
                    <i class="bi bi-x-circle"></i>
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
          <h5>Nova Reserva</h5>
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
              <label class="form-label">Livro *</label>
              <select v-model.number="createForm.id_livro" class="form-select">
                <option value="">Selecione...</option>
                <option v-for="l in livros" :key="l.id_livro" :value="l.id_livro">{{ l.titulo }}</option>
              </select>
            </div>
            <div class="col-md-6">
              <label class="form-label">Data de Validade</label>
              <input v-model="createForm.data_validade" type="date" class="form-control" />
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
          <button class="btn btn-primary" :disabled="saving" @click="saveReserva">
            <span v-if="saving" class="spinner-border spinner-border-sm me-1"></span>Reservar
          </button>
        </div>
      </div>
    </div>

    <!-- Atender Modal -->
    <div v-if="showAtender" class="modal-overlay" @click.self="showAtender = false">
      <div class="modal-box">
        <div class="modal-header">
          <h5>Atender Reserva #{{ atenderReserva?.id_reserva }}</h5>
          <button class="btn-close" @click="showAtender = false"></button>
        </div>
        <div class="modal-body">
          <div class="row g-3">
            <div class="col-12">
              <label class="form-label">Funcionário *</label>
              <select v-model.number="atenderForm.id_funcionario" class="form-select">
                <option value="">Selecione...</option>
                <option v-for="f in funcionarios" :key="f.id_funcionario" :value="f.id_funcionario">{{ f.nome }}</option>
              </select>
            </div>
            <div class="col-12">
              <label class="form-label">Exemplar Disponível *</label>
              <select v-model.number="atenderForm.id_exemplar" class="form-select">
                <option value="">Selecione...</option>
                <option v-for="ex in exemplares" :key="ex.id_exemplar" :value="ex.id_exemplar">
                  {{ ex.codigo_exemplar }} — {{ ex.titulo_livro }}
                </option>
              </select>
            </div>
            <div class="col-md-6">
              <label class="form-label">Prazo (dias)</label>
              <input v-model.number="atenderForm.dias_prazo" type="number" min="1" class="form-control" />
            </div>
          </div>
          <div v-if="errorMsg" class="alert alert-danger mt-3 mb-0">{{ errorMsg }}</div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-light" @click="showAtender = false">Cancelar</button>
          <button class="btn btn-success" :disabled="saving" @click="saveAtender">
            <span v-if="saving" class="spinner-border spinner-border-sm me-1"></span>Confirmar Empréstimo
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
const livros      = ref([])
const funcionarios = ref([])
const exemplares  = ref([])
const loading     = ref(true)
const saving      = ref(false)
const errorMsg    = ref('')
const activeFilter = ref('')
const showCreate  = ref(false)
const showAtender = ref(false)
const atenderReserva = ref(null)

const fDate = formatDate
const badge = statusBadge

const filters = [
  { label: 'Todas', value: '' },
  { label: 'Ativas', value: 'ATIVA' },
  { label: 'Atendidas', value: 'ATENDIDA' },
  { label: 'Canceladas', value: 'CANCELADA' },
  { label: 'Expiradas', value: 'EXPIRADA' },
]

const createForm = ref({ id_usuario: '', id_livro: '', data_validade: '', observacoes: '' })
const atenderForm = ref({ id_funcionario: '', id_exemplar: '', dias_prazo: 15 })

async function load() {
  loading.value = true
  try { items.value = (await api.getReservas({ status: activeFilter.value })).data }
  finally { loading.value = false }
}

function setFilter(v) { activeFilter.value = v; load() }

async function openCreate() {
  const [u, l] = await Promise.all([api.getUsuarios(), api.getLivros()])
  usuarios.value = u.data; livros.value = l.data
  createForm.value = { id_usuario: '', id_livro: '', data_validade: '', observacoes: '' }
  errorMsg.value = ''; showCreate.value = true
}

async function saveReserva() {
  saving.value = true; errorMsg.value = ''
  try {
    await api.createReserva({
      ...createForm.value,
      id_usuario: Number(createForm.value.id_usuario),
      id_livro: Number(createForm.value.id_livro),
      data_validade: createForm.value.data_validade || null,
    })
    showCreate.value = false; await load()
  } catch (e) { errorMsg.value = e.response?.data?.detail || 'Erro ao criar reserva' }
  finally { saving.value = false }
}

async function cancelar(r) {
  if (!confirm(`Cancelar reserva #${r.id_reserva}?`)) return
  try { await api.cancelarReserva(r.id_reserva, { motivo: 'Cancelado pelo operador' }); await load() }
  catch (e) { alert(e.response?.data?.detail || 'Erro ao cancelar') }
}

async function openAtender(r) {
  atenderReserva.value = r
  const [f, ex] = await Promise.all([api.getFuncionarios(), api.getExemplares({ situacao: 'DISPONIVEL' })])
  funcionarios.value = f.data; exemplares.value = ex.data
  atenderForm.value = { id_funcionario: '', id_exemplar: '', dias_prazo: 15 }
  errorMsg.value = ''; showAtender.value = true
}

async function saveAtender() {
  saving.value = true; errorMsg.value = ''
  try {
    await api.atenderReserva(atenderReserva.value.id_reserva, atenderForm.value)
    showAtender.value = false; await load()
  } catch (e) { errorMsg.value = e.response?.data?.detail || 'Erro ao atender' }
  finally { saving.value = false }
}

onMounted(load)
</script>
