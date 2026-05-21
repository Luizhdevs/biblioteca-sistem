from fastapi import APIRouter, HTTPException, Query
from database import get_cursor
from schemas import ReservaCreate, ReservaCancelar, ReservaAtender
from utils import db_error
import psycopg2

router = APIRouter()


@router.get("/")
def list_reservas(status: str = Query(default="")):
    try:
        with get_cursor() as cur:
            conds, params = [], []
            if status:
                conds.append("r.status = %s")
                params.append(status)
            where = ("WHERE " + " AND ".join(conds)) if conds else ""
            cur.execute(
                f"""
                SELECT r.*, u.nome AS nome_usuario, l.titulo AS titulo_livro
                FROM reserva r
                JOIN usuario_biblioteca u ON u.id_usuario = r.id_usuario
                JOIN livro l ON l.id_livro = r.id_livro
                {where}
                ORDER BY r.data_reserva DESC
                """,
                params,
            )
            return cur.fetchall()
    except psycopg2.Error as e:
        raise db_error(e)


@router.get("/{id_reserva}")
def get_reserva(id_reserva: int):
    try:
        with get_cursor() as cur:
            cur.execute(
                """SELECT r.*, u.nome AS nome_usuario, l.titulo AS titulo_livro
                   FROM reserva r
                   JOIN usuario_biblioteca u ON u.id_usuario = r.id_usuario
                   JOIN livro l ON l.id_livro = r.id_livro
                   WHERE r.id_reserva = %s""",
                (id_reserva,),
            )
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Reserva não encontrada")
            return row
    except psycopg2.Error as e:
        raise db_error(e)


@router.post("/", status_code=201)
def create_reserva(data: ReservaCreate):
    try:
        with get_cursor() as cur:
            cur.execute(
                """INSERT INTO reserva (id_usuario, id_livro, data_validade, observacoes)
                   VALUES (%s,%s,%s,%s) RETURNING *""",
                (data.id_usuario, data.id_livro, data.data_validade, data.observacoes),
            )
            return cur.fetchone()
    except psycopg2.Error as e:
        raise db_error(e)


@router.post("/{id_reserva}/cancelar")
def cancelar_reserva(id_reserva: int, data: ReservaCancelar):
    try:
        with get_cursor() as cur:
            cur.execute("CALL sp_cancelar_reserva(%s,%s)", (id_reserva, data.motivo))
            return {"message": "Reserva cancelada com sucesso"}
    except psycopg2.Error as e:
        raise db_error(e)


@router.post("/{id_reserva}/atender")
def atender_reserva(id_reserva: int, data: ReservaAtender):
    try:
        with get_cursor() as cur:
            cur.execute(
                "CALL sp_atender_reserva(%s,%s,%s,%s)",
                (id_reserva, data.id_funcionario, data.id_exemplar, data.dias_prazo),
            )
            return {"message": "Reserva atendida e empréstimo criado"}
    except psycopg2.Error as e:
        raise db_error(e)
