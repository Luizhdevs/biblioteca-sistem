import axios from 'axios'

// Em produção (Vercel), VITE_API_URL aponta para o Render. Em dev, o proxy do Vite usa /api.
const baseURL = import.meta.env.VITE_API_URL || '/api'

const http = axios.create({ baseURL })

export default {
  // Dashboard
  getStats:               ()         => http.get('/dashboard/stats'),
  getEmprestimosRecentes: ()         => http.get('/dashboard/emprestimos-recentes'),

  // Livros
  getLivros:    (p)  => http.get('/livros/', { params: p }),
  getLivro:     (id) => http.get(`/livros/${id}`),
  createLivro:  (d)  => http.post('/livros/', d),
  updateLivro:  (id, d) => http.put(`/livros/${id}`, d),
  deleteLivro:  (id) => http.delete(`/livros/${id}`),

  // Autores
  getAutores:   ()       => http.get('/autores/'),
  createAutor:  (d)      => http.post('/autores/', d),
  updateAutor:  (id, d)  => http.put(`/autores/${id}`, d),
  deleteAutor:  (id)     => http.delete(`/autores/${id}`),

  // Editoras
  getEditoras:   ()       => http.get('/editoras/'),
  createEditora: (d)      => http.post('/editoras/', d),
  updateEditora: (id, d)  => http.put(`/editoras/${id}`, d),
  deleteEditora: (id)     => http.delete(`/editoras/${id}`),

  // Usuários
  getUsuarios:   (p)      => http.get('/usuarios/', { params: p }),
  getUsuario:    (id)     => http.get(`/usuarios/${id}`),
  createUsuario: (d)      => http.post('/usuarios/', d),
  updateUsuario: (id, d)  => http.put(`/usuarios/${id}`, d),
  deleteUsuario: (id)     => http.delete(`/usuarios/${id}`),

  // Funcionários
  getFuncionarios:   ()       => http.get('/funcionarios/'),
  createFuncionario: (d)      => http.post('/funcionarios/', d),
  updateFuncionario: (id, d)  => http.put(`/funcionarios/${id}`, d),
  deleteFuncionario: (id)     => http.delete(`/funcionarios/${id}`),

  // Exemplares
  getExemplares: (p) => http.get('/exemplares/', { params: p }),

  // Empréstimos
  getEmprestimos:      (p)      => http.get('/emprestimos/', { params: p }),
  registrarEmprestimo: (d)      => http.post('/emprestimos/', d),
  devolverEmprestimo:  (id)     => http.post(`/emprestimos/${id}/devolver`),
  renovarEmprestimo:   (id, d)  => http.post(`/emprestimos/${id}/renovar`, d),

  // Multas
  getMultas:  (p)  => http.get('/multas/', { params: p }),
  pagarMulta: (id) => http.post(`/multas/${id}/pagar`),

  // Reservas
  getReservas:     (p)      => http.get('/reservas/', { params: p }),
  createReserva:   (d)      => http.post('/reservas/', d),
  cancelarReserva: (id, d)  => http.post(`/reservas/${id}/cancelar`, d),
  atenderReserva:  (id, d)  => http.post(`/reservas/${id}/atender`, d),

  // Relatórios
  getInadimplencia:      () => http.get('/relatorios/inadimplencia'),
  getLivrosDisponiveis:  () => http.get('/relatorios/livros-disponiveis'),
  getMultasPendentes:    () => http.get('/relatorios/multas-pendentes'),
}
