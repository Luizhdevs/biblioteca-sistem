from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import (
    dashboard, livros, autores, editoras,
    usuarios, funcionarios, exemplares,
    emprestimos, multas, reservas, relatorios,
)

app = FastAPI(
    title="Sistema de Gerenciamento de Biblioteca",
    version="1.0.0",
)

import os

_raw = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
_origins = [o.strip() for o in _raw.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard.router,    prefix="/dashboard",    tags=["Dashboard"])
app.include_router(livros.router,       prefix="/livros",       tags=["Livros"])
app.include_router(autores.router,      prefix="/autores",      tags=["Autores"])
app.include_router(editoras.router,     prefix="/editoras",     tags=["Editoras"])
app.include_router(usuarios.router,     prefix="/usuarios",     tags=["Usuários"])
app.include_router(funcionarios.router, prefix="/funcionarios", tags=["Funcionários"])
app.include_router(exemplares.router,   prefix="/exemplares",   tags=["Exemplares"])
app.include_router(emprestimos.router,  prefix="/emprestimos",  tags=["Empréstimos"])
app.include_router(multas.router,       prefix="/multas",       tags=["Multas"])
app.include_router(reservas.router,     prefix="/reservas",     tags=["Reservas"])
app.include_router(relatorios.router,   prefix="/relatorios",   tags=["Relatórios"])


@app.get("/")
def root():
    return {"message": "Biblioteca API v1.0"}


@app.get("/health")
def health():
    import os
    try:
        from database import get_cursor
        with get_cursor() as cur:
            cur.execute("SELECT 1")
        return {"status": "ok", "db": "connected"}
    except Exception as e:
        return {"status": "error", "detail": str(e), "db_url_set": bool(os.getenv("DATABASE_URL"))}
