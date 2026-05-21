from fastapi import APIRouter, HTTPException
from database import get_cursor
from schemas import FuncionarioCreate, FuncionarioUpdate
from utils import db_error
import psycopg2

router = APIRouter()


@router.get("/")
def list_funcionarios():
    try:
        with get_cursor() as cur:
            cur.execute("SELECT * FROM funcionario ORDER BY nome")
            return cur.fetchall()
    except psycopg2.Error as e:
        raise db_error(e)


@router.get("/{id_funcionario}")
def get_funcionario(id_funcionario: int):
    try:
        with get_cursor() as cur:
            cur.execute("SELECT * FROM funcionario WHERE id_funcionario = %s", (id_funcionario,))
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Funcionário não encontrado")
            return row
    except psycopg2.Error as e:
        raise db_error(e)


@router.post("/", status_code=201)
def create_funcionario(data: FuncionarioCreate):
    try:
        with get_cursor() as cur:
            cur.execute(
                "INSERT INTO funcionario (nome, cargo, telefone, email) VALUES (%s,%s,%s,%s) RETURNING *",
                (data.nome, data.cargo, data.telefone, data.email),
            )
            return cur.fetchone()
    except psycopg2.Error as e:
        raise db_error(e)


@router.put("/{id_funcionario}")
def update_funcionario(id_funcionario: int, data: FuncionarioUpdate):
    fields = data.model_dump(exclude_none=True)
    if not fields:
        raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
    try:
        with get_cursor() as cur:
            set_clause = ", ".join(f"{k} = %s" for k in fields)
            cur.execute(
                f"UPDATE funcionario SET {set_clause} WHERE id_funcionario = %s RETURNING *",
                list(fields.values()) + [id_funcionario],
            )
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Funcionário não encontrado")
            return row
    except psycopg2.Error as e:
        raise db_error(e)


@router.delete("/{id_funcionario}", status_code=204)
def delete_funcionario(id_funcionario: int):
    try:
        with get_cursor() as cur:
            cur.execute(
                "DELETE FROM funcionario WHERE id_funcionario = %s RETURNING id_funcionario",
                (id_funcionario,),
            )
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    except psycopg2.Error as e:
        raise db_error(e)
