from fastapi import APIRouter, HTTPException, Query
from database import get_cursor
from schemas import EmprestimoCreate, EmprestimoRenovar
from utils import db_error
import psycopg2

router = APIRouter()

_JOIN = """
    SELECT
        e.*,
        u.nome  AS nome_usuario,
        f.nome  AS nome_funcionario,
        ex.codigo_exemplar,
        l.titulo AS titulo_livro
    FROM emprestimo e
    JOIN usuario_biblioteca u  ON u.id_usuario     = e.id_usuario
    JOIN funcionario f         ON f.id_funcionario = e.id_funcionario
    JOIN exemplar ex           ON ex.id_exemplar   = e.id_exemplar
    JOIN livro l               ON l.id_livro       = ex.id_livro
"""


@router.get("/")
def list_emprestimos(
    situacao: str = Query(default=""),
    id_usuario: int = Query(default=None),
    skip: int = 0,
    limit: int = 100,
):
    try:
        with get_cursor() as cur:
            conds, params = [], []
            if situacao:
                conds.append("e.situacao = %s")
                params.append(situacao)
            if id_usuario:
                conds.append("e.id_usuario = %s")
                params.append(id_usuario)
            where = ("WHERE " + " AND ".join(conds)) if conds else ""
            cur.execute(
                f"{_JOIN} {where} ORDER BY e.data_emprestimo DESC LIMIT %s OFFSET %s",
                params + [limit, skip],
            )
            return cur.fetchall()
    except psycopg2.Error as e:
        raise db_error(e)


@router.get("/{id_emprestimo}")
def get_emprestimo(id_emprestimo: int):
    try:
        with get_cursor() as cur:
            cur.execute(f"{_JOIN} WHERE e.id_emprestimo = %s", (id_emprestimo,))
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Empréstimo não encontrado")
            return row
    except psycopg2.Error as e:
        raise db_error(e)


@router.post("/", status_code=201)
def registrar_emprestimo(data: EmprestimoCreate):
    try:
        with get_cursor() as cur:
            cur.execute(
                "CALL sp_registrar_emprestimo(%s,%s,%s,%s)",
                (data.id_usuario, data.id_funcionario, data.id_exemplar, data.dias_prazo),
            )
            if data.observacoes:
                cur.execute(
                    """UPDATE emprestimo SET observacoes = %s
                       WHERE id_emprestimo = (
                           SELECT MAX(id_emprestimo) FROM emprestimo WHERE id_exemplar = %s
                       )""",
                    (data.observacoes, data.id_exemplar),
                )
            return {"message": "Empréstimo registrado com sucesso"}
    except psycopg2.Error as e:
        raise db_error(e)


@router.post("/{id_emprestimo}/devolver")
def devolver_emprestimo(id_emprestimo: int):
    try:
        with get_cursor() as cur:
            cur.execute("CALL sp_registrar_devolucao(%s)", (id_emprestimo,))
            return {"message": "Devolução registrada com sucesso"}
    except psycopg2.Error as e:
        raise db_error(e)


@router.post("/{id_emprestimo}/renovar")
def renovar_emprestimo(id_emprestimo: int, data: EmprestimoRenovar):
    try:
        with get_cursor() as cur:
            cur.execute("CALL sp_renovar_emprestimo(%s,%s)", (id_emprestimo, data.dias_adicionais))
            return {"message": "Empréstimo renovado com sucesso"}
    except psycopg2.Error as e:
        raise db_error(e)
