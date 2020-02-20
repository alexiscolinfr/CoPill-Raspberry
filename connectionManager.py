import mysql.connector

config = {
  'user': 'miage2020',
  'password': 'k5HKw26D4x',
  'host': 'db4free.net',
  'database': 'copill_db',
  'raise_on_warnings': True
}

class ConnectionManager:
    def __init__(self):
        self._conn = mysql.connector.connect(**config)
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.cursor.close()
        self.connection.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()
