<template>
  <div class="app-layout">
    <aside class="sidebar">
      <div class="sidebar-brand">
        <i class="bi bi-building-fill"></i>
        <h1>Biblioteca</h1>
      </div>

      <div class="sidebar-section">Principal</div>
      <RouterLink to="/" class="nav-link-item" exact-active-class="router-link-active">
        <i class="bi bi-house-fill"></i> Dashboard
      </RouterLink>

      <div class="sidebar-section">Acervo</div>
      <RouterLink to="/livros" class="nav-link-item">
        <i class="bi bi-book-fill"></i> Livros
      </RouterLink>
      <RouterLink to="/autores" class="nav-link-item">
        <i class="bi bi-person-lines-fill"></i> Autores
      </RouterLink>
      <RouterLink to="/editoras" class="nav-link-item">
        <i class="bi bi-shop"></i> Editoras
      </RouterLink>

      <div class="sidebar-section">Pessoas</div>
      <RouterLink to="/usuarios" class="nav-link-item">
        <i class="bi bi-people-fill"></i> Usuários
      </RouterLink>
      <RouterLink to="/funcionarios" class="nav-link-item">
        <i class="bi bi-person-badge-fill"></i> Funcionários
      </RouterLink>

      <div class="sidebar-section">Circulação</div>
      <RouterLink to="/emprestimos" class="nav-link-item">
        <i class="bi bi-arrow-left-right"></i> Empréstimos
      </RouterLink>
      <RouterLink to="/multas" class="nav-link-item">
        <i class="bi bi-exclamation-triangle-fill"></i> Multas
      </RouterLink>
      <RouterLink to="/reservas" class="nav-link-item">
        <i class="bi bi-bookmark-fill"></i> Reservas
      </RouterLink>

      <div class="sidebar-section">Relatórios</div>
      <RouterLink to="/relatorios" class="nav-link-item">
        <i class="bi bi-bar-chart-fill"></i> Relatórios
      </RouterLink>
    </aside>

    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>
