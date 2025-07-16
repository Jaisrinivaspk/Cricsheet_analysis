import sqlite3
import pandas as pd

def run_query(sql):
    conn = sqlite3.connect("database/cricsheet.db")
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df
