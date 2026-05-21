from fastapi import APIRouter, HTTPException, Query
from database import get_cursor
from schemas import UsuarioCreate, UsuarioUpdate
from utils import db_error
import psycopg2

router = APIRouter()


@router.get("/")
def list_usuarios(search: str = Query(default="")):
    try:
        with get_cursor() as cur:
            pattern = f"%{search}%"
            cur.execute(
                """SELECT * FROM usuario_biblioteca
                   WHERE nome ILIKE %s OR cpf ILIKE %s OR email ILIKE %s
                   ORDER BY nome""",
                (pattern, pattern, pattern),
            )
            return cur.fetchall()
    except psycopg2.Error as e:
        raise db_error(e)


@router.get("/{id_usuario}")
def get_usuario(id_usuario: int):
    try:
        with get_cursor() as cur:
            cur.execute("SELECT * FROM usuario_biblioteca WHERE id_usuario = %s", (id_usuario,))
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Usuário não encontrado")
            return row
    except psycopg2.Error as e:
        raise db_error(e)


@router.post("/", status_code=201)
def create_usuario(data: UsuarioCreate):
    try:
        with get_cursor() as cur:
            cur.execute(
                """INSERT INTO usuario_biblioteca (nome, cpf, endereco, telefone, email)
                   VALUES (%s,%s,%s,%s,%s) RETURNING *""",
                (data.nome, data.cpf, data.endereco, data.telefone, data.email),
            )
            return cur.fetchone()
    except psycopg2.Error as e:
        raise db_error(e)


@router.put("/{id_usuario}")
def update_usuario(id_usuario: int, data: UsuarioUpdate):
    fields = data.model_dump(exclude_none=True)
    if not fields:
        raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
    try:
        with get_cursor() as cur:
            set_clause = ", ".join(f"{k} = %s" for k in fields)
            cur.execute(
                f"UPDATE usuario_biblioteca SET {set_clause} WHERE id_usuario = %s RETURNING *",
                list(fields.values()) + [id_usuario],
            )
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Usuário não encontrado")
            return row
    except psycopg2.Error as e:
        raise db_error(e)


@router.delete("/{id_usuario}", status_code=204)
def delete_usuario(id_usuario: int):
    try:
        with get_cursor() as cur:
            cur.execute(
                "DELETE FROM usuario_biblioteca WHERE id_usuario = %s RETURNING id_usuario",
                (id_usuario,),
            )
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Usuário não encontrado")
    except psycopg2.Error as e:
        raise db_error(e)
