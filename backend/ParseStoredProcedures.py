from DataFrameJoiner import DatabaseSchemaCollector
import pandas as pd
import re

class SQLParser:
    def __init__(self, server, database):
        # Initialize DatabaseSchemaCollector
        self.schema_collector = DatabaseSchemaCollector(server, database)
    
    def parse_table_references(self):
        # Fetch schema data
        schema_data = self.schema_collector.fetch_schema_data()
        
        # Assuming 'fetch_schema_data' returns a dictionary of DataFrames, including 'stored_procedure_df'
        stored_procedure_df = schema_data.get('stored_procedure_df') 

        for index, row in stored_procedure_df.iterrows():
            query = row['ProcedureText']
            print(query)
            query = ' '.join(query.splitlines())
            print(query)
            real_tables = []
            hash_tables = []
            global_temp_tables = []

            # Extract table names from the FROM clause
            from_clause = re.search(r'FROM\s*(.*?)(?=WHERE|GROUP BY|ORDER BY|HAVING|$)', query, re.IGNORECASE)
            if from_clause:
                tables = from_clause.group(1).split(',')
                for table in tables:
                    table = table.strip()
                    if table.startswith('#'):
                        if table.startswith('##'):
                            global_temp_tables.append(table[2:])
                        else:
                            hash_tables.append(table[1:])
                    else:
                        real_tables.append(table)
            else:
                print('Not Found')

            # Extract table names from the JOIN clauses
            join_tables = re.findall(r'JOIN\s*(\S+)', query, re.IGNORECASE)
            for table in join_tables:
                table = table.strip()
                if table.startswith('#'):
                    if table.startswith('##'):
                        global_temp_tables.append(table[2:])
                    else:
                        hash_tables.append(table[1:])
                else:
                    real_tables.append(table)

            return [real_tables, hash_tables, global_temp_tables]


if __name__ == "__main__":
    server = 'DESKTOP-1OCA8OH\\SQLEXPRESS'
    database = 'northwind'
    
    # Initialize SQLParser with server and database
    sql_parser = SQLParser(server, database)
    
    # Fetch and print the top row of the stored_procedure_df
    tables  = sql_parser.parse_table_references()
    print(tables)