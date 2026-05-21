# Sistema de Gerenciamento de Biblioteca

Aplicação web para o banco de dados da biblioteca. Backend em FastAPI (Python) + Frontend em Vue 3.

## Pré-requisitos

- Python 3.11+
- Node.js 18+
- PostgreSQL com o banco `biblioteca` já criado (executar os scripts da pasta `scripts/`)

## Configuração do Backend

```bash
cd app/backend

# Copiar e editar as credenciais do banco
copy .env.example .env
# Editar .env com seu usuário/senha do PostgreSQL

# Criar ambiente virtual e instalar dependências
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt

# Iniciar o servidor
uvicorn main:app --reload --port 8000
```

A API ficará disponível em `http://localhost:8000`
Documentação automática: `http://localhost:8000/docs`

## Configuração do Frontend

```bash
cd app/frontend

npm install
npm run dev
```

O frontend ficará em `http://localhost:5173`

## Estrutura da Aplicação

```
app/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── database.py          # Pool de conexões PostgreSQL
│   ├── schemas.py           # Modelos Pydantic
│   ├── utils.py             # Tratamento de erros
│   ├── requirements.txt
│   ├── .env                 # Credenciais (não versionar)
│   └── routers/
│       ├── dashboard.py     # Stats e empréstimos recentes
│       ├── livros.py        # CRUD livros
│       ├── autores.py       # CRUD autores
│       ├── editoras.py      # CRUD editoras
│       ├── usuarios.py      # CRUD usuários
│       ├── funcionarios.py  # CRUD funcionários
│       ├── exemplares.py    # Consulta exemplares
│       ├── emprestimos.py   # Empréstimos, devoluções, renovações
│       ├── multas.py        # Multas e pagamentos
│       ├── reservas.py      # Reservas
│       └── relatorios.py    # Relatórios via views/functions
└── frontend/
    └── src/
        ├── views/
        │   ├── DashboardView.vue
        │   ├── LivrosView.vue
        │   ├── UsuariosView.vue
        │   ├── FuncionariosView.vue
        │   ├── AutoresView.vue
        │   ├── EditorasView.vue
        │   ├── EmprestimosView.vue
        │   ├── MultasView.vue
        │   ├── ReservasView.vue
        │   └── RelatoriosView.vue
        ├── api/index.js     # Chamadas axios
        └── utils/formatters.js
```

## Funcionalidades

| Módulo | Funcionalidades |
|---|---|
| Dashboard | Cards de estatísticas + empréstimos recentes |
| Livros | Listar, buscar, cadastrar (com exemplares), editar, excluir |
| Autores / Editoras | CRUD completo |
| Usuários / Funcionários | CRUD completo |
| Empréstimos | Registrar, devolver, renovar, filtrar por status |
| Multas | Listar por status, registrar pagamento |
| Reservas | Criar, cancelar, atender (gera empréstimo) |
| Relatórios | Inadimplência, livros disponíveis, multas pendentes |

## Variáveis de Ambiente (.env)

| Variável | Padrão | Descrição |
|---|---|---|
| DB_HOST | localhost | Host do PostgreSQL |
| DB_PORT | 5432 | Porta |
| DB_NAME | postgres | Nome do banco |
| DB_USER | postgres | Usuário |
| DB_PASSWORD | postgres | Senha |
| DB_SCHEMA | biblioteca | Schema |
