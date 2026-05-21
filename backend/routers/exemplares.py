from fastapi import APIRouter, HTTPException, Query
from database import get_cursor
from schemas import ExemplarUpdate
from utils import db_error
import psycopg2

router = APIRouter()


@router.get("/")
def list_exemplares(
    id_livro: int = Query(default=None),
    situacao: str = Query(default=""),
):
    try:
        with get_cursor() as cur:
            conditions = []
            params = []
            if id_livro:
                conditions.append("ex.id_livro = %s")
                params.append(id_livro)
            if situacao:
                conditions.append("ex.situacao = %s")
                params.append(situacao)
            where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
            cur.execute(
                f"""
                SELECT ex.*, l.titulo AS titulo_livro
                FROM exemplar ex
                JOIN livro l ON l.id_livro = ex.id_livro
                {where}
                ORDER BY ex.codigo_exemplar
                """,
                params,
            )
            return cur.fetchall()
    except psycopg2.Error as e:
        raise db_error(e)


@router.get("/{id_exemplar}")
def get_exemplar(id_exemplar: int):
    try:
        with get_cursor() as cur:
            cur.execute(
                """SELECT ex.*, l.titulo AS titulo_livro
                   FROM exemplar ex JOIN livro l ON l.id_livro = ex.id_livro
                   WHERE ex.id_exemplar = %s""",
                (id_exemplar,),
            )
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Exemplar não encontrado")
            return row
    except psycopg2.Error as e:
        raise db_error(e)


@router.patch("/{id_exemplar}")
def update_exemplar(id_exemplar: int, data: ExemplarUpdate):
    fields = data.model_dump(exclude_none=True)
    if not fields:
        raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
    try:
        with get_cursor() as cur:
            set_clause = ", ".join(f"{k} = %s" for k in fields)
            cur.execute(
                f"UPDATE exemplar SET {set_clause} WHERE id_exemplar = %s RETURNING *",
                list(fields.values()) + [id_exemplar],
            )
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Exemplar não encontrado")
            return row
    except psycopg2.Error as e:
        raise db_error(e)
