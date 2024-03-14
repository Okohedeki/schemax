import pyodbc
import pandas as pl
import yaml
import time
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)


class DatabaseConnector:
    def __init__(self, server, database):
        self.server = 'DESKTOP-1OCA8OH\\SQLEXPRESS'
        self.database = database
        self.connection = None
        self.queries = None  # Dictionary to store queries loaded from YAML file

    def connect(self):
        try:
            # Establishing a connection using Windows Authentication
            self.connection = pyodbc.connect(
                f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                f'SERVER={self.server};'
                f'DATABASE={self.database};'
                'Trusted_Connection=yes;'  # Indicates Windows Authentication
                'TrustServerCertificate=yes;'  # For a secure connection, set up and use SSL
                'Encrypt=no;'  # Use SSL encryption for data
            )
            print("Connection successful.")
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            raise

    def load_queries_from_yaml(self, yaml_file):
        try:
            # Load queries from YAML file into a dictionary
            with open(yaml_file, 'r') as f:
                self.queries = yaml.safe_load(f)
            print("Queries loaded successfully.")
        except Exception as e:
            print(f"Error loading queries from YAML file: {e}")
            self.queries = None

    def reset_yaml_queries(self):
        self.queries = None  

    def general_queries(self):
        if not self.connection:
            print("Database is not connected. Please call the connect method first.")
            return None
        if not self.queries:
            print("No queries loaded. Please call load_queries_from_yaml method first.")
            return None
        try:
            result_dfs = {}  # Dictionary to store result DataFrames
            for query_name, query_info in self.queries.items():
                query_text = query_info.get('query')
                if query_text is None:
                    print(f"Query '{query_name}' not found in the YAML file.")
                    continue

                # Execute SQL query and fetch results
                cursor = self.connection.cursor()
                cursor.execute(query_text)
                data = cursor.fetchall()

                # Create Polars DataFrame
                df = pl.DataFrame([list(row) for row in data], columns=[column[0] for column in cursor.description])

                # Store the DataFrame in the result dictionary with the query name as the key
                result_dfs[query_name] = df

            return result_dfs
        except Exception as e:
            print(f"Error in execute_all_queries: {e}")
            return None

    def get_all_table_info(self, tables_df):
        if not self.connection:
            print("Database is not connected. Please call the connect method first.")
            return None
        if not self.queries:
            print("No queries loaded. Please call load_queries_from_yaml method first.")
            return None
        try:
            result_dfs = {}  # Dictionary to store result DataFrames

            for query_name, query_info in self.queries.items():
                query = query_info.get('query')
                if query is None:
                    print(f"Query '{query_name}' not found in the YAML file.")
                    continue

                result_df = None  # Initialize result DataFrame

                for index, row in tables_df.iterrows():
                    table_name = row['TABLE_NAME']

                    # Replace placeholders with actual table name
                    query_text = query.replace(':table_name', "'" + table_name + "'")

                    # Execute SQL query and fetch results
                    cursor = self.connection.cursor()
                    cursor.execute(query_text)
                    data = cursor.fetchall()

                    # Create Polars DataFrame
                    df = pl.DataFrame([list(row) for row in data], columns=[column[0] for column in cursor.description])

                    # Concatenate with previous result or set as result_df
                    if result_df is None:
                        result_df = df
                    else:
                        result_df = pl.concat([result_df, df], axis=0)

                # Store result DataFrame in dictionary
                result_dfs[query_name] = result_df

            return result_dfs
        except Exception as e:
            print(f"Error in get_all_table_info: {e}")
            return None
    
    def get_all_view_info(self, tables_df):
        if not self.connection:
            print("Database is not connected. Please call the connect method first.")
            return None
        if not self.queries:
            print("No queries loaded. Please call load_queries_from_yaml method first.")
            return None
        try:
            result_dfs = {}  # Dictionary to store result DataFrames

            for query_name, query_info in self.queries.items():
                query = query_info.get('query')
                if query is None:
                    print(f"Query '{query_name}' not found in the YAML file.")
                    continue

                result_df = None  # Initialize result DataFrame

                for index, row in tables_df.iterrows():
                    table_name = row['VIEW_NAME']

                    # Replace placeholders with actual table name
                    query_text = query.replace(':view_name', "'" + table_name + "'")

                    # Execute SQL query and fetch results
                    cursor = self.connection.cursor()
                    cursor.execute(query_text)
                    data = cursor.fetchall()

                    # Create Polars DataFrame
                    df = pl.DataFrame([list(row) for row in data], columns=[column[0] for column in cursor.description])

                    # Concatenate with previous result or set as result_df
                    if result_df is None:
                        result_df = df
                    else:
                        result_df = pl.concat([result_df, df], axis=0)

                # Store result DataFrame in dictionary
                result_dfs[query_name] = result_df

            return result_dfs
        except Exception as e:
            print(f"Error in get_all_view_info: {e}")
            return None

    def get_all_query_hash_info(self, tables_df):
        if not self.connection:
            print("Database is not connected. Please call the connect method first.")
            return None
        if not self.queries:
            print("No queries loaded. Please call load_queries_from_yaml method first.")
            return None
        try:
            result_dfs = {}  # Dictionary to store result DataFrames

            for query_name, query_info in self.queries.items():
                query = query_info.get('query')                
                if query is None:
                    print(f"Query '{query_name}' not found in the YAML file.")
                    continue

                result_df = None  # Initialize result DataFrame

                for index, row in tables_df.iterrows():
                    hash_byte = row['query_plan_hash']
                    hex_data = '0x' + hash_byte.hex()

                    # Replace placeholders with actual table name
                    query_text = query.replace(':query_hash', "'" + hex_data + "'")

                    # Execute SQL query and fetch results
                    cursor = self.connection.cursor()
                    cursor.execute(query_text)
                    data = cursor.fetchall()

                    # Create Polars DataFrame
                    df = pl.DataFrame([list(row) for row in data], columns=[column[0] for column in cursor.description])

                    # Concatenate with previous result or set as result_df
                    if result_df is None:
                        result_df = df
                    else:
                        result_df = pl.concat([result_df, df], axis=0)

                # Store result DataFrame in dictionary
                result_dfs[query_name] = result_df

            return result_dfs
        except Exception as e:
            print(f"Error in get_all_query_hash_info: {e}")
            return None

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Database connection closed.")

# Example usage
if __name__ == "__main__":
    server = 'DESKTOP-1OCA8OH\\SQLEXPRESS'
    database = 'northwind'

    yaml_file_table = 'SQLQueriesTable.yml'  # Path to your YAML file
    yaml_file_general = 'SQLQueriesGeneral.yml'  # Path to your YAML file
    yaml_file_hash = 'SQLQueriesHash.yml'
    yaml_file_views = 'SQLQueriesViews.yml'


    # Creating an instance of the DatabaseConnector
    db_connector = DatabaseConnector(server, database)
    db_connector.connect()  # Establish connection
    db_connector.load_queries_from_yaml(yaml_file_general)  # Load queries from YAML file

    # #Get all constraints 
    # constraints_df = db_connector.get_all_constraints()
    # Get all tables
    general_query_dict = db_connector.general_queries()
    
    table_df = general_query_dict.get('get_all_tables')
    constraints_df = general_query_dict.get('get_all_constraints_keys')
    views_df = general_query_dict.get('get_all_views')
    recent_queries_df = general_query_dict.get('get_recent_queries')

    db_connector.reset_yaml_queries()
    db_connector.load_queries_from_yaml(yaml_file_table)  # Load queries from YAML file

    if table_df is not None:
        # print("All tables:")

        # Get all columns for each table
       table_info_dict = db_connector.get_all_table_info(table_df)

    table_columns_df = table_info_dict.get('get_all_columns_tables')
    table_triggers_df = table_info_dict.get('get_all_triggers')
    table_indexes_df = table_info_dict.get('get_all_indexes')

    db_connector.reset_yaml_queries()
    db_connector.load_queries_from_yaml(yaml_file_views)  # Load queries from YAML file
    view_dict = db_connector.get_all_view_info(views_df)
    view_df = view_dict.get('get_all_view_columns')

    db_connector.reset_yaml_queries()
    db_connector.load_queries_from_yaml(yaml_file_hash)  # Load queries from YAML file
    hash_info_dict = db_connector.get_all_query_hash_info(recent_queries_df)
    hash_df = hash_info_dict.get('get_query_xml')

    db_connector.close_connection()  # Close the connection