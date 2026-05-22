from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from dotenv import load_dotenv
import os

load_dotenv()

_pool: ThreadedConnectionPool | None = None


def get_pool() -> ThreadedConnectionPool:
    global _pool
    if _pool is None:
        # Supabase / Render fornecem DATABASE_URL; variáveis individuais para local
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            if "sslmode" not in database_url:
                database_url += ("&" if "?" in database_url else "?") + "sslmode=require"
            _pool = ThreadedConnectionPool(
                minconn=1,
                maxconn=10,
                dsn=database_url,
                options=f"-c search_path={os.getenv('DB_SCHEMA', 'biblioteca')}",
            )
        else:
            _pool = ThreadedConnectionPool(
                minconn=1,
                maxconn=10,
                host=os.getenv("DB_HOST", "localhost"),
                port=int(os.getenv("DB_PORT", "5432")),
                dbname=os.getenv("DB_NAME", "postgres"),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASSWORD", "postgres"),
                options=f"-c search_path={os.getenv('DB_SCHEMA', 'biblioteca')}",
            )
    return _pool


@contextmanager
def get_conn():
    pool = get_pool()
    conn = pool.getconn()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        pool.putconn(conn)


@contextmanager
def get_cursor():
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            yield cur
