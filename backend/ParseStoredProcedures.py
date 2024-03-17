import pandas as pd
import re
from Utils import Utils

class SQLParser:
    def __init__(self):
        pass
    
    def parse_table_references(self, stored_procedure_df):
        rows = []
        for index, row in stored_procedure_df.iterrows():
            query = row['ProcedureText']
            query = ' '.join(query.splitlines())

            # Extract table names from the FROM clause
            from_clause = re.search(r'FROM\s*(.*?)(?=WHERE|GROUP BY|ORDER BY|HAVING|$)', query, re.IGNORECASE)
            if from_clause:
                tables = from_clause.group(1).split(',')
                for table in tables:
                    table = table.strip()
                    table = Utils.remove_before_first_space(table)
                    table = Utils.replace_non_alphanumeric(table)
                    rows.append([row['ProcedureName'], table])

            # Extract table names from the JOIN clauses
            join_tables = re.findall(r'JOIN\s*(\S+)', query, re.IGNORECASE)
            for table in join_tables:
                table = table.strip()
                table = Utils.replace_non_alphanumeric(table)
                rows.append([row['ProcedureName'], table])

        # Create a DataFrame from the collected data
        result_df = pd.DataFrame(rows, columns=['ProcedureName', 'TABLE_NAME'])
        return result_df


if __name__ == "__main__":
    server = 'DESKTOP-1OCA8OH\\SQLEXPRESS'
    database = 'northwind'
    
    # Create an instance of SQLParser
    sql_parser = SQLParser()
    
    # Fetch the stored_procedure_df (assuming it's already loaded into a DataFrame)
    stored_procedure_df = ...  # Replace ... with the actual DataFrame
    
    # Parse table references and print the result
    tables = sql_parser.parse_table_references(stored_procedure_df)
    print(tables)