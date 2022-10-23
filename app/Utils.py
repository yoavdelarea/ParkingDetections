import psycopg2

import os


def db_connect():
    conn_string = "host='localhost' dbname='parking' user='postgres' password='123'"
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    return conn, cursor
