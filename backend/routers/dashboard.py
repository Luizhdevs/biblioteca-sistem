from fastapi import APIRouter, HTTPException
from database import get_cursor
from utils import db_error
import psycopg2

router = APIRouter()


@router.get("/stats")
def get_stats():
    try:
        with get_cursor() as cur:
            cur.execute("SELECT COUNT(*) AS total FROM livro")
            total_livros = cur.fetchone()["total"]
            cur.execute("SELECT COUNT(*) AS total FROM usuario_biblioteca")
            total_usuarios = cur.fetchone()["total"]
            cur.execute("SELECT COUNT(*) AS total FROM emprestimo WHERE situacao = 'ATIVO'")
            emprestimos_ativos = cur.fetchone()["total"]
            cur.execute("SELECT COUNT(*) AS total FROM emprestimo WHERE situacao = 'ATRASADO'")
            emprestimos_atrasados = cur.fetchone()["total"]
            cur.execute("SELECT COUNT(*) AS total FROM multa WHERE status_pagamento = 'PENDENTE'")
            multas_pendentes = cur.fetchone()["total"]
            cur.execute("SELECT COUNT(*) AS total FROM reserva WHERE status = 'ATIVA'")
            reservas_ativas = cur.fetchone()["total"]
            return {
                "total_livros": total_livros,
                "total_usuarios": total_usuarios,
                "emprestimos_ativos": emprestimos_ativos,
                "emprestimos_atrasados": emprestimos_atrasados,
                "multas_pendentes": multas_pendentes,
                "reservas_ativas": reservas_ativas,
            }
    except psycopg2.Error as e:
        raise db_error(e)


@router.get("/emprestimos-recentes")
def get_emprestimos_recentes():
    try:
        with get_cursor() as cur:
            cur.execute("""
                SELECT
                    e.id_emprestimo,
                    u.nome AS nome_usuario,
                    l.titulo AS titulo_livro,
                    e.data_emprestimo,
                    e.data_prevista_devolucao,
                    e.situacao
                FROM emprestimo e
                JOIN usuario_biblioteca u ON u.id_usuario = e.id_usuario
                JOIN exemplar ex ON ex.id_exemplar = e.id_exemplar
                JOIN livro l ON l.id_livro = ex.id_livro
                ORDER BY e.data_emprestimo DESC
                LIMIT 10
            """)
            return cur.fetchall()
    except psycopg2.Error as e:
        raise db_error(e)
