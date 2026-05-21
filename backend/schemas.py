from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date
import re


# ── Editora ───────────────────────────────────────────────────────────────────

class EditoraCreate(BaseModel):
    nome: str
    endereco: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None


class EditoraUpdate(BaseModel):
    nome: Optional[str] = None
    endereco: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None


# ── Autor ─────────────────────────────────────────────────────────────────────

class AutorCreate(BaseModel):
    nome: str
    nacionalidade: Optional[str] = None
    data_nascimento: Optional[date] = None


class AutorUpdate(BaseModel):
    nome: Optional[str] = None
    nacionalidade: Optional[str] = None
    data_nascimento: Optional[date] = None


# ── Livro ─────────────────────────────────────────────────────────────────────

class LivroCreate(BaseModel):
    id_editora: int
    isbn: str
    titulo: str
    ano_publicacao: int
    genero: str
    idioma: Optional[str] = "Portugues"
    numero_paginas: Optional[int] = None
    descricao: Optional[str] = None
    quantidade_exemplares: int = 1
    localizacao: Optional[str] = "PRATELEIRA GERAL"
    autores: list[int] = []


class LivroUpdate(BaseModel):
    id_editora: Optional[int] = None
    isbn: Optional[str] = None
    titulo: Optional[str] = None
    ano_publicacao: Optional[int] = None
    genero: Optional[str] = None
    idioma: Optional[str] = None
    numero_paginas: Optional[int] = None
    descricao: Optional[str] = None


# ── Exemplar ──────────────────────────────────────────────────────────────────

class ExemplarUpdate(BaseModel):
    situacao: Optional[str] = None
    localizacao: Optional[str] = None


# ── Usuario ───────────────────────────────────────────────────────────────────

class UsuarioCreate(BaseModel):
    nome: str
    cpf: str
    endereco: str
    telefone: Optional[str] = None
    email: str

    @field_validator("cpf")
    @classmethod
    def cpf_only_digits(cls, v: str) -> str:
        clean = re.sub(r"[^\d]", "", v)
        if len(clean) != 11:
            raise ValueError("CPF deve ter 11 dígitos")
        return clean


class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    endereco: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None


# ── Funcionario ───────────────────────────────────────────────────────────────

class FuncionarioCreate(BaseModel):
    nome: str
    cargo: str
    telefone: Optional[str] = None
    email: str


class FuncionarioUpdate(BaseModel):
    nome: Optional[str] = None
    cargo: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None


# ── Emprestimo ────────────────────────────────────────────────────────────────

class EmprestimoCreate(BaseModel):
    id_usuario: int
    id_funcionario: int
    id_exemplar: int
    dias_prazo: int = 15
    observacoes: Optional[str] = None


class EmprestimoRenovar(BaseModel):
    dias_adicionais: int = 7


# ── Reserva ───────────────────────────────────────────────────────────────────

class ReservaCreate(BaseModel):
    id_usuario: int
    id_livro: int
    data_validade: Optional[date] = None
    observacoes: Optional[str] = None


class ReservaCancelar(BaseModel):
    motivo: str = "Cancelado pelo operador"


class ReservaAtender(BaseModel):
    id_funcionario: int
    id_exemplar: int
    dias_prazo: int = 15
