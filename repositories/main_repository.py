import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import RealDictCursor
from config.sql_config import SQLALCHEMY_DATABASE_URI


def get_db_connection():
    return psycopg2.connect(SQLALCHEMY_DATABASE_URI, cursor_factory=RealDictCursor)


def make_structure_query(query: str):
    with get_db_connection() as connection:  # type: _connection
        with connection.cursor() as cursor:  # type: RealDictCursor
            cursor.execute(query)
            connection.commit()


def make_data_modify_query(query: str, params: tuple = ()):
    with get_db_connection() as connection:  # type: _connection
        with connection.cursor() as cursor:  # type: RealDictCursor
            cursor.execute(query, params)
            connection.commit()
            return cursor.rowcount


def make_insert_query(query: str, params: tuple = ()):
    with get_db_connection() as connection, connection.cursor() as cursor:  # type
        cursor.execute(query, params)
        new_id = cursor.fetchone()["id"]
        connection.commit()
        return new_id


def get_one(query):
    with get_db_connection() as connection:  # type: _connection
        with connection.cursor() as cursor:  # type: RealDictCursor
            cursor.execute(query)
            res = cursor.fetchone()
            connection.commit()
    return res


def get_all(query):
    with get_db_connection() as connection:  # type: _connection
        with connection.cursor() as cursor:  # type: RealDictCursor
            cursor.execute(query)
            res = cursor.fetchall()
            connection.commit()
    return res


