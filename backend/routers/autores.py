from fastapi import APIRouter, HTTPException
from database import get_cursor
from schemas import AutorCreate, AutorUpdate
from utils import db_error
import psycopg2

router = APIRouter()


@router.get("/")
def list_autores():
    try:
        with get_cursor() as cur:
            cur.execute("SELECT * FROM autor ORDER BY nome")
            return cur.fetchall()
    except psycopg2.Error as e:
        raise db_error(e)


@router.get("/{id_autor}")
def get_autor(id_autor: int):
    try:
        with get_cursor() as cur:
            cur.execute("SELECT * FROM autor WHERE id_autor = %s", (id_autor,))
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Autor não encontrado")
            return row
    except psycopg2.Error as e:
        raise db_error(e)


@router.post("/", status_code=201)
def create_autor(data: AutorCreate):
    try:
        with get_cursor() as cur:
            cur.execute(
                "INSERT INTO autor (nome, nacionalidade, data_nascimento) VALUES (%s,%s,%s) RETURNING *",
                (data.nome, data.nacionalidade, data.data_nascimento),
            )
            return cur.fetchone()
    except psycopg2.Error as e:
        raise db_error(e)


@router.put("/{id_autor}")
def update_autor(id_autor: int, data: AutorUpdate):
    fields = data.model_dump(exclude_none=True)
    if not fields:
        raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
    try:
        with get_cursor() as cur:
            set_clause = ", ".join(f"{k} = %s" for k in fields)
            cur.execute(
                f"UPDATE autor SET {set_clause} WHERE id_autor = %s RETURNING *",
                list(fields.values()) + [id_autor],
            )
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Autor não encontrado")
            return row
    except psycopg2.Error as e:
        raise db_error(e)


@router.delete("/{id_autor}", status_code=204)
def delete_autor(id_autor: int):
    try:
        with get_cursor() as cur:
            cur.execute("DELETE FROM autor WHERE id_autor = %s RETURNING id_autor", (id_autor,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Autor não encontrado")
    except psycopg2.Error as e:
        raise db_error(e)
