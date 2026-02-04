"""
Basic database operations.
"""

import sqlite3


class Database():
    """
    Collect data from the database and the user.
    """
    def __init__(self, database_file, noisy=True):
        self.con = self.db_open(database_file)
        self.noisy = noisy


    def db_close(self):
        """
        Command and close database.
        """
        self.con.commit()
        self.con.close()


    def db_open(self, database_file):
        """
        Open database.
        """
        self.con = sqlite3.connect(database_file)
        return self.con


    def commit(self):
        """
        Commit the changes to the database.
        """
        self.con.commit()


    def get_id(self, table_name):
        """
        Get the latest ID value for a table.
        """
        sql = f'select seq from sqlite_sequence where name="{table_name}"'
        cursor = self.con.cursor()
        cursor.execute(sql)
        return cursor.fetchone()[0]


    def select(self, column_names, table_name, where, alt_selects=()):
        """
        Basic SELECT. Returns list of dicts using column_names as keys.
        Note: the where arg can also contain things like ORDER BY
        that follow the WHERE clause. Likewise, the table_name arg
        can contain JOIN clauses.

        if alt_selects is specified, it is a list of one or more
        [name, expr] pairs. This allows one to have an expression in
        the SELECT list: name AS expr. The name is used to return the
        expr in the as one of the keys.
        """
        sql = f"""SELECT
                  {', '.join([f'"{column}"' for column in column_names])}
                  {', ' + (','.join([alt_select[1] + ' AS ' + alt_select[0]
                                     for alt_select in alt_selects]))
        if alt_selects else ''}
                  FROM {table_name} WHERE {where}"""

        cursor = self.con.cursor()
        if self.noisy:
            print(sql)
        cursor.execute(sql)
        return [dict(zip(column_names +
                          [alt_select[0]
                           for alt_select in alt_selects],
                         result)) for result in cursor.fetchall()]


    def insert(self, table_name, columns):
        """
        Perform an SQL INSERT. Columns is dict where the keys are
        column names and the values are the values to be inserted.
        """
        sql = f"""INSERT INTO {table_name}
                  ({', '.join(columns.keys())})
                  VALUES (:{', :'.join(columns.keys())})"""
        cursor = self.con.cursor()
        if self.noisy:
            print(sql)
        cursor.execute(sql, columns)
        self.commit()


    def update(self, table_name, columns, values, unique_column, unique_value):
        """
        Do a simple DB update.
        """
        sets = [f"{col}={quote_value(val)}" for (col,val) in zip(columns, values)]

        sql = f"""UPDATE {table_name} SET {','.join(sets)}
                  WHERE {unique_column} = {unique_value}"""
        if self.noisy:
            print(sql)
        cursor = self.con.cursor()
        cursor.execute(sql)
        self.commit()


    def upsert(self, table_name, columns, unique_column):
        """
        Do an upsert, inserting if the record isn't there, updating if it
        already there.
        """
        # This is for SET if the unique_column already exists.
        # That is, these are the columns that are updated.
        # In this case, the unique_column is already there so
        # it is included in the SET clause.
        most_sets = [f"{col}=excluded.{col}" for col in columns
                     if col != unique_column]
        sql = f"""INSERT INTO {table_name}
                  ({', '.join(columns.keys())})
                  VALUES (:{', :'.join(columns.keys())})
                  ON CONFLICT({unique_column})
                  DO UPDATE SET {','.join(most_sets)}"""
        if self.noisy:
            print(sql)
        cursor = self.con.cursor()
        cursor.execute(sql, columns)
        self.commit()


def quote_value(value):
    """
    Quote the value, if necessary.
    """
    if value is not None and isinstance(value, str):
        return f"""'{value.replace("'", "''")}'"""
    return value
