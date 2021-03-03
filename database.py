import psycopg2 as psg

class Database():
    def __init__(self, db, user, password, host, port):
        self.Database = psg.connect(
            database=db, user=user, password=password, host=host, port=port
        )

        self.cursor = self.Database.cursor()

    def select(self, table, columns, condition, size=None, order_by=None):
        if order_by is None:
            self.cursor.execute(f"SELECT {columns} FROM {table} WHERE {condition};")
        else:
            self.cursor.execute(
                f"SELECT {columns} FROM {table} WHERE {condition} ORDER BY {order_by};"
            )
        if size is None:
            return self.cursor.fetchall()
        else:
            return self.cursor.fetchmany(size)

    def update(self, table, command, condition):
        try:
            self.cursor.execute(f"UPDATE {table} SET {command} WHERE {condition};")
            e = 1
        except Exception as j:
            e = j
            self.cursor.execute("ROLLBACK;")

        self.Database.commit()
        return e

    def insert(self, table, values: tuple):
        try:
            self.cursor.execute(f"INSERT INTO {table} VALUES {values};")
            e = 1
        except Exception as j:
            e = j
            self.cursor.execute("ROLLBACK;")

        self.Database.commit()
        return e

    def delete(self, table, condition):
        try:
            self.cursor.execute(f"DELETE FROM {table} WHERE {condition};")
            e = 1
        except Exception as j:
            e = j
            self.cursor.execute("ROLLBACK;")

        self.Database.commit()
        return e

    def insert_ignore(self, table, values):
        try:
            self.cursor.execute(
                f"INSERT INTO {table} VALUES {values} ON CONFLICT DO NOTHING;"
            )
            e = 1
        except Exception as j:
            e = j
            self.cursor.execute("ROLLBACK;")

        self.Database.commit()
        return e