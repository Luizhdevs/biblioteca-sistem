from fastapi import APIRouter, HTTPException
from database import get_cursor
from schemas import EditoraCreate, EditoraUpdate
from utils import db_error
import psycopg2

router = APIRouter()


@router.get("/")
def list_editoras():
    try:
        with get_cursor() as cur:
            cur.execute("SELECT * FROM editora ORDER BY nome")
            return cur.fetchall()
    except psycopg2.Error as e:
        raise db_error(e)


@router.get("/{id_editora}")
def get_editora(id_editora: int):
    try:
        with get_cursor() as cur:
            cur.execute("SELECT * FROM editora WHERE id_editora = %s", (id_editora,))
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Editora não encontrada")
            return row
    except psycopg2.Error as e:
        raise db_error(e)


@router.post("/", status_code=201)
def create_editora(data: EditoraCreate):
    try:
        with get_cursor() as cur:
            cur.execute(
                "INSERT INTO editora (nome, endereco, telefone, email) VALUES (%s,%s,%s,%s) RETURNING *",
                (data.nome, data.endereco, data.telefone, data.email),
            )
            return cur.fetchone()
    except psycopg2.Error as e:
        raise db_error(e)


@router.put("/{id_editora}")
def update_editora(id_editora: int, data: EditoraUpdate):
    fields = data.model_dump(exclude_none=True)
    if not fields:
        raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
    try:
        with get_cursor() as cur:
            set_clause = ", ".join(f"{k} = %s" for k in fields)
            cur.execute(
                f"UPDATE editora SET {set_clause} WHERE id_editora = %s RETURNING *",
                list(fields.values()) + [id_editora],
            )
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Editora não encontrada")
            return row
    except psycopg2.Error as e:
        raise db_error(e)


@router.delete("/{id_editora}", status_code=204)
def delete_editora(id_editora: int):
    try:
        with get_cursor() as cur:
            cur.execute("DELETE FROM editora WHERE id_editora = %s RETURNING id_editora", (id_editora,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Editora não encontrada")
    except psycopg2.Error as e:
        raise db_error(e)
