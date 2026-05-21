from fastapi import APIRouter, HTTPException, Query
from database import get_cursor
from schemas import LivroCreate, LivroUpdate
from utils import db_error
import psycopg2

router = APIRouter()


@router.get("/")
def list_livros(
    search: str = Query(default=""),
    skip: int = 0,
    limit: int = 100,
):
    try:
        with get_cursor() as cur:
            pattern = f"%{search}%"
            cur.execute(
                """
                SELECT
                    l.*,
                    e.nome AS nome_editora,
                    COALESCE(
                        json_agg(json_build_object('id_autor', a.id_autor, 'nome', a.nome))
                        FILTER (WHERE a.id_autor IS NOT NULL), '[]'
                    ) AS autores
                FROM livro l
                LEFT JOIN editora e ON e.id_editora = l.id_editora
                LEFT JOIN livro_autor la ON la.id_livro = l.id_livro
                LEFT JOIN autor a ON a.id_autor = la.id_autor
                WHERE l.titulo ILIKE %s OR l.isbn ILIKE %s OR l.genero ILIKE %s
                GROUP BY l.id_livro, e.nome
                ORDER BY l.titulo
                LIMIT %s OFFSET %s
                """,
                (pattern, pattern, pattern, limit, skip),
            )
            return cur.fetchall()
    except psycopg2.Error as e:
        raise db_error(e)


@router.get("/{id_livro}")
def get_livro(id_livro: int):
    try:
        with get_cursor() as cur:
            cur.execute(
                """
                SELECT
                    l.*,
                    e.nome AS nome_editora,
                    COALESCE(
                        json_agg(json_build_object('id_autor', a.id_autor, 'nome', a.nome))
                        FILTER (WHERE a.id_autor IS NOT NULL), '[]'
                    ) AS autores
                FROM livro l
                LEFT JOIN editora e ON e.id_editora = l.id_editora
                LEFT JOIN livro_autor la ON la.id_livro = l.id_livro
                LEFT JOIN autor a ON a.id_autor = la.id_autor
                WHERE l.id_livro = %s
                GROUP BY l.id_livro, e.nome
                """,
                (id_livro,),
            )
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Livro não encontrado")
            return row
    except psycopg2.Error as e:
        raise db_error(e)


@router.post("/", status_code=201)
def create_livro(data: LivroCreate):
    try:
        with get_cursor() as cur:
            cur.execute(
                "CALL sp_cadastrar_livro_com_exemplares(%s,%s,%s,%s,%s,%s,%s,%s)",
                (
                    data.id_editora,
                    data.isbn,
                    data.titulo,
                    data.ano_publicacao,
                    data.genero,
                    data.numero_paginas,
                    data.quantidade_exemplares,
                    data.localizacao,
                ),
            )
            cur.execute("SELECT id_livro FROM livro WHERE isbn = %s", (data.isbn,))
            id_livro = cur.fetchone()["id_livro"]
            for id_autor in data.autores:
                cur.execute(
                    "INSERT INTO livro_autor (id_livro, id_autor) VALUES (%s,%s) ON CONFLICT DO NOTHING",
                    (id_livro, id_autor),
                )
            return {"id_livro": id_livro, "message": "Livro cadastrado com sucesso"}
    except psycopg2.Error as e:
        raise db_error(e)


@router.put("/{id_livro}")
def update_livro(id_livro: int, data: LivroUpdate):
    fields = data.model_dump(exclude_none=True)
    if not fields:
        raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
    try:
        with get_cursor() as cur:
            set_clause = ", ".join(f"{k} = %s" for k in fields)
            cur.execute(
                f"UPDATE livro SET {set_clause} WHERE id_livro = %s RETURNING id_livro",
                list(fields.values()) + [id_livro],
            )
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Livro não encontrado")
            return {"message": "Livro atualizado com sucesso"}
    except psycopg2.Error as e:
        raise db_error(e)


@router.delete("/{id_livro}", status_code=204)
def delete_livro(id_livro: int):
    try:
        with get_cursor() as cur:
            cur.execute("DELETE FROM livro WHERE id_livro = %s RETURNING id_livro", (id_livro,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Livro não encontrado")
    except psycopg2.Error as e:
        raise db_error(e)
