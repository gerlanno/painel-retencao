import mysql.connector
import psycopg2
import pymysql
import pyodbc

from configs.config import Settings


def get_atrix_connection():
    return mysql.connector.connect(
        host=Settings.ATRIX_HOST,
        database=Settings.ATRIX_DB,
        user=Settings.ATRIX_USER,
        password=Settings.ATRIX_PASSWORD
    )


def get_supabase_connection():
    return psycopg2.connect(
        dbname=Settings.SUPABASE_DB,
        user=Settings.SUPABASE_USER,
        password=Settings.SUPABASE_PASSWORD,
        host=Settings.SUPABASE_HOST,
        port=Settings.SUPABASE_PORT
    )