import { createRouter, createWebHistory } from 'vue-router'
import DashboardView   from '../views/DashboardView.vue'
import LivrosView      from '../views/LivrosView.vue'
import UsuariosView    from '../views/UsuariosView.vue'
import FuncionariosView from '../views/FuncionariosView.vue'
import AutoresView     from '../views/AutoresView.vue'
import EditorasView    from '../views/EditorasView.vue'
import EmprestimosView from '../views/EmprestimosView.vue'
import MultasView      from '../views/MultasView.vue'
import ReservasView    from '../views/ReservasView.vue'
import RelatoriosView  from '../views/RelatoriosView.vue'

const routes = [
  { path: '/',              component: DashboardView,    name: 'dashboard' },
  { path: '/livros',        component: LivrosView,       name: 'livros' },
  { path: '/usuarios',      component: UsuariosView,     name: 'usuarios' },
  { path: '/funcionarios',  component: FuncionariosView, name: 'funcionarios' },
  { path: '/autores',       component: AutoresView,      name: 'autores' },
  { path: '/editoras',      component: EditorasView,     name: 'editoras' },
  { path: '/emprestimos',   component: EmprestimosView,  name: 'emprestimos' },
  { path: '/multas',        component: MultasView,       name: 'multas' },
  { path: '/reservas',      component: ReservasView,     name: 'reservas' },
  { path: '/relatorios',    component: RelatoriosView,   name: 'relatorios' },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
