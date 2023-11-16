import psycopg2
from psycopg2.extras import DictCursor

class Database:
    def __init__(self, host, user, password, db, port=None):
        if port:
            self.conn = psycopg2.connect(host=host, port=port, user=user, password=password, dbname=db)
            self.conn.set_client_encoding('UTF8')
        else:
            self.conn = psycopg2.connect(host=host, user=user, password=password, dbname=db)
        self.cursor = self.conn.cursor(cursor_factory=DictCursor)

    def execute_query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def insert_or_update(self, table, columns, values, unique_columns=[]):
        columns_quoted = [f'"{col}"' for col in columns]
        
        base_query = f"""INSERT INTO "{table}" ({', '.join(columns_quoted)})
                    VALUES ({', '.join(['%s' for _ in columns])}) """
        
        if unique_columns:
            unique_columns_quoted = [f'"{col}"' for col in unique_columns]
            conflict_query = f"""ON CONFLICT ({', '.join(unique_columns_quoted)}) DO UPDATE SET """
            conflict_query += ', '.join([f'"{col}" = EXCLUDED."{col}"' for col in columns])
            query = base_query + conflict_query
        else:
            query = base_query

        self.cursor.executemany(query, values)
        self.conn.commit()

    def update(self, table, update_values, conditions=None):
        columns = list(update_values.keys())
        values = list(update_values.values())
        
        set_clause = ', '.join([f'{col} = %s' for col in columns])
        
        if conditions:
            where_clause = ' AND '.join([f'{col} = %s' for col in conditions.keys()])
            values.extend(list(conditions.values()))
            query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        else:
            query = f"UPDATE {table} SET {set_clause}"
        
        self.cursor.execute(query, tuple(values))
        self.conn.commit()

    def insert(self, table, columns, values):
        query = f"""INSERT INTO {table} ({', '.join(columns)}) 
                    VALUES ({', '.join(['%s' for _ in columns])})"""
        self.cursor.executemany(query, values)
        self.conn.commit()

    def select(self, table, columns=None, condition=None):
        cols = ', '.join(columns) if columns else '*'
        query = f"SELECT {cols} FROM {table}"
        
        if condition:
            condition_text = ' AND '.join([f'{k} = %s' for k, v in condition.items()])
            query += f" WHERE {condition_text}"
            self.cursor.execute(query, list(condition.values()))
        else:
            self.cursor.execute(query)
            
        return self.cursor.fetchall()
