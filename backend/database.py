from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from urllib.parse import urlparse, unquote
from dotenv import load_dotenv
import os

load_dotenv()

_pool: ThreadedConnectionPool | None = None


def get_pool() -> ThreadedConnectionPool:
    global _pool
    if _pool is None:
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            p = urlparse(database_url)
            _pool = ThreadedConnectionPool(
                minconn=1,
                maxconn=10,
                host=p.hostname,
                port=p.port or 5432,
                dbname=p.path.lstrip("/"),
                user=unquote(p.username),
                password=unquote(p.password),
                sslmode="require",
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
    schema = os.getenv("DB_SCHEMA", "biblioteca")
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(f"SET search_path TO {schema}")
            yield cur
