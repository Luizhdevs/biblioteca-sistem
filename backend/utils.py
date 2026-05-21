import psycopg2
from fastapi import HTTPException


def db_error(e: psycopg2.Error) -> HTTPException:
    if hasattr(e, "diag") and e.diag.message_primary:
        detail = e.diag.message_primary
    else:
        detail = str(e).strip()
    if isinstance(e, psycopg2.errors.UniqueViolation):
        return HTTPException(status_code=409, detail=detail)
    if isinstance(e, psycopg2.errors.ForeignKeyViolation):
        return HTTPException(status_code=422, detail=detail)
    return HTTPException(status_code=400, detail=detail)
