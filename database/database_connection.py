import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling
import os
from dotenv import load_dotenv

class DatabaseConnection:
    def __init__(self, host, user, password, database, pool_name="expoferia_pool", pool_size=5):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.pool_name = pool_name
        self.pool_size = pool_size
        self.connection_pool = None
        self.create_pool()

    def create_pool(self):
        try:
            self.connection_pool = pooling.MySQLConnectionPool(
                pool_name=self.pool_name,
                pool_size=self.pool_size,
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Connection pool created successfully")
        except Error as e:
            print(f"Error creating connection pool: {e}")
            raise

    def get_connection(self):
        try:
            return self.connection_pool.get_connection()
        except Error as e:
            print(f"Error getting connection from pool: {e}")
            raise

    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False, commit=False):
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            cursor.execute(query, params or ())
            
            if commit:
                connection.commit()
                return cursor.rowcount
            elif fetch_one:
                return cursor.fetchone()
            elif fetch_all:
                return cursor.fetchall()
            else:
                return None
                
        except Error as e:
            print(f"Error executing query: {e}")
            if connection:
                connection.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def execute_procedure(self, procedure, params=None, fetch_one=False, fetch_all=False):
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            cursor.callproc(procedure, params or ())
            
            results = []
            for result in cursor.stored_results():
                if fetch_one:
                    return result.fetchone()
                elif fetch_all:
                    results.extend(result.fetchall())
            
            return results if fetch_all else None
                
        except Error as e:
            print(f"Error executing procedure: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()