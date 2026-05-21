from fastapi import APIRouter
from database import get_cursor
from utils import db_error
import psycopg2

router = APIRouter()


@router.get("/inadimplencia")
def relatorio_inadimplencia():
    try:
        with get_cursor() as cur:
            cur.execute("SELECT * FROM fn_relatorio_inadimplencia()")
            return cur.fetchall()
    except psycopg2.Error as e:
        raise db_error(e)


@router.get("/livros-disponiveis")
def relatorio_livros_disponiveis():
    try:
        with get_cursor() as cur:
            cur.execute("SELECT * FROM vw_livros_disponiveis ORDER BY titulo")
            return cur.fetchall()
    except psycopg2.Error as e:
        raise db_error(e)


@router.get("/multas-pendentes")
def relatorio_multas_pendentes():
    try:
        with get_cursor() as cur:
            cur.execute("SELECT * FROM vw_multas_pendentes ORDER BY data_vencimento")
            return cur.fetchall()
    except psycopg2.Error as e:
        raise db_error(e)
