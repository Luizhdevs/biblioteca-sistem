from fastapi import APIRouter, HTTPException, Query
from database import get_cursor
from utils import db_error
import psycopg2

router = APIRouter()


@router.get("/")
def list_multas(status: str = Query(default="")):
    try:
        with get_cursor() as cur:
            conds, params = [], []
            if status:
                conds.append("m.status_pagamento = %s")
                params.append(status)
            where = ("WHERE " + " AND ".join(conds)) if conds else ""
            cur.execute(
                f"""
                SELECT
                    m.*,
                    u.nome  AS nome_usuario,
                    l.titulo AS titulo_livro
                FROM multa m
                JOIN emprestimo e ON e.id_emprestimo = m.id_emprestimo
                JOIN usuario_biblioteca u ON u.id_usuario = e.id_usuario
                JOIN exemplar ex ON ex.id_exemplar = e.id_exemplar
                JOIN livro l ON l.id_livro = ex.id_livro
                {where}
                ORDER BY m.data_geracao DESC
                """,
                params,
            )
            return cur.fetchall()
    except psycopg2.Error as e:
        raise db_error(e)


@router.get("/{id_multa}")
def get_multa(id_multa: int):
    try:
        with get_cursor() as cur:
            cur.execute(
                """
                SELECT m.*, u.nome AS nome_usuario, l.titulo AS titulo_livro
                FROM multa m
                JOIN emprestimo e ON e.id_emprestimo = m.id_emprestimo
                JOIN usuario_biblioteca u ON u.id_usuario = e.id_usuario
                JOIN exemplar ex ON ex.id_exemplar = e.id_exemplar
                JOIN livro l ON l.id_livro = ex.id_livro
                WHERE m.id_multa = %s
                """,
                (id_multa,),
            )
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Multa não encontrada")
            return row
    except psycopg2.Error as e:
        raise db_error(e)


@router.post("/{id_multa}/pagar")
def pagar_multa(id_multa: int):
    try:
        with get_cursor() as cur:
            cur.execute("CALL sp_pagar_multa(%s)", (id_multa,))
            return {"message": "Multa paga com sucesso"}
    except psycopg2.Error as e:
        raise db_error(e)
