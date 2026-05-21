export function formatDate(d) {
  if (!d) return '—'
  const s = d.includes('T') ? d.split('T')[0] : d
  const [y, m, day] = s.split('-')
  return `${day}/${m}/${y}`
}

export function formatCurrency(v) {
  if (v == null) return '—'
  return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(v)
}

export function formatCPF(cpf) {
  if (!cpf) return '—'
  return cpf.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4')
}

export function statusBadge(status) {
  const map = {
    ATIVO:       { bg: 'bg-primary',   text: 'Ativo' },
    DEVOLVIDO:   { bg: 'bg-success',   text: 'Devolvido' },
    ATRASADO:    { bg: 'bg-danger',    text: 'Atrasado' },
    PENDENTE:    { bg: 'bg-warning text-dark', text: 'Pendente' },
    PAGO:        { bg: 'bg-success',   text: 'Pago' },
    CANCELADO:   { bg: 'bg-secondary', text: 'Cancelado' },
    ATIVA:       { bg: 'bg-primary',   text: 'Ativa' },
    ATENDIDA:    { bg: 'bg-success',   text: 'Atendida' },
    EXPIRADA:    { bg: 'bg-secondary', text: 'Expirada' },
    DISPONIVEL:  { bg: 'bg-success',   text: 'Disponível' },
    EMPRESTADO:  { bg: 'bg-primary',   text: 'Emprestado' },
    RESERVADO:   { bg: 'bg-warning text-dark', text: 'Reservado' },
    MANUTENCAO:  { bg: 'bg-danger',    text: 'Manutenção' },
  }
  return map[status] || { bg: 'bg-light text-dark', text: status }
}
