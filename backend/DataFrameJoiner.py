from GetSchemaData import DatabaseConnector
import warnings
import os

warnings.simplefilter(action='ignore', category=FutureWarning)

class DatabaseSchemaCollector:
    def __init__(self, server, database):
        self.server = server
        self.database = database
        self.db_connector = None

    def fetch_schema_data(self):
        self.db_connector = DatabaseConnector(self.server, self.database)
        self.db_connector.connect()

        # Load general queries
        yaml_file_general = 'SQLQueriesGeneral.yml'
        self.db_connector.load_queries_from_yaml(yaml_file_general)
        general_query_dict = self.db_connector.general_queries()

        table_df = general_query_dict.get('get_all_tables')
        constraints_df = general_query_dict.get('get_all_constraints_keys')
        views_df = general_query_dict.get('get_all_views')
        recent_queries_df = general_query_dict.get('get_recent_queries')

        # Load table queries
        yaml_file_table = 'SQLQueriesTable.yml'
        self.db_connector.reset_yaml_queries()
        self.db_connector.load_queries_from_yaml(yaml_file_table)

        table_info_dict = None
        if table_df is not None:
            table_info_dict = self.db_connector.get_all_table_info(table_df)

        table_columns_df = table_info_dict.get('get_all_columns_tables') if table_info_dict else None
        table_triggers_df = table_info_dict.get('get_all_triggers') if table_info_dict else None
        table_indexes_df = table_info_dict.get('get_all_indexes') if table_info_dict else None

        # Load view queries
        yaml_file_views = 'SQLQueriesViews.yml'
        self.db_connector.reset_yaml_queries()
        self.db_connector.load_queries_from_yaml(yaml_file_views)
        view_dict = self.db_connector.get_all_view_info(views_df)
        view_df = view_dict.get('get_all_view_columns') if view_dict else None

        # Load hash queries
        yaml_file_hash = 'SQLQueriesHash.yml'
        self.db_connector.reset_yaml_queries()
        self.db_connector.load_queries_from_yaml(yaml_file_hash)
        hash_info_dict = self.db_connector.get_all_query_hash_info(recent_queries_df)
        hash_df = hash_info_dict.get('get_query_xml') if hash_info_dict else None

        self.db_connector.close_connection()

        # Returning all fetched data frames
        return {
            'table_df': table_df,
            'constraints_df': constraints_df,
            'views_df': views_df,
            'recent_queries_df': recent_queries_df,
            'table_columns_df': table_columns_df,
            'table_triggers_df': table_triggers_df,
            'table_indexes_df': table_indexes_df,
            'view_df': view_df,
            'hash_df': hash_df,
        }

    def manipulate_dataframes(self, result_dict):
        if 'table_triggers_df' in result_dict:
            # Rename column 'TableName' to 'TABLE_NAME'
            table_triggers_df = result_dict['table_triggers_df'].rename(columns={'TableName': 'TABLE_NAME'})
            result_dict['table_triggers_df'] = table_triggers_df

        if 'constraints_df' in result_dict:
            # Replace 'dbo.' in 'table_view' column and rename to 'TABLE_NAME'
            constraints_df = result_dict['constraints_df']
            constraints_df['TABLE_NAME'] = constraints_df['table_view'].str.replace('dbo.', '')
            result_dict['constraints_df'] = constraints_df.drop(columns=['table_view'])

        if 'table_indexes_df' in result_dict:
            table_indexes_df = result_dict['table_indexes_df'].rename(columns={'TableName': 'TABLE_NAME'})
            result_dict['table_indexes_df'] = table_indexes_df

        return result_dict

    def join_tables(self, result_dict):
            table_df = result_dict.get('table_df')
            constraints_df = result_dict.get('constraints_df')
            views_df = result_dict.get('views_df')
            recent_queries_df = result_dict.get('recent_queries_df')
            table_columns_df = result_dict.get('table_columns_df')
            table_triggers_df = result_dict.get('table_triggers_df')
            table_indexes_df = result_dict.get('table_indexes_df')
            view_df = result_dict.get('view_df')
            hash_df = result_dict.get('hash_df')

            try:
                # Perform left join
                table_index_join_df = table_df.merge(table_triggers_df, how='left', on='TABLE_NAME')
                table_index_join_df = table_index_join_df.merge(table_columns_df, how='left', on='TABLE_NAME')
                table_index_join_df = table_index_join_df.merge(table_indexes_df, how='left', on='TABLE_NAME')
                table_index_join_df = table_index_join_df.merge(constraints_df, how='left', on='TABLE_NAME')

                view_join_df = views_df.merge(view_df, how='left', on='VIEW_NAME')
                hash_join_df = recent_queries_df.merge(hash_df, how='left', on='query_plan_hash')

                return {'table_joins_df':table_index_join_df, 'view_joins_df':view_join_df, 'hash_joins_df':hash_join_df}
            except Exception as e:
                print(f"Error during left join operation: {e}")
                return None

if __name__ == "__main__":
    server = 'DESKTOP-1OCA8OH\\SQLEXPRESS'
    database = 'northwind'

    schema_collector = DatabaseSchemaCollector(server, database)
    schema_data = schema_collector.fetch_schema_data()

    cleaned_dataframes = schema_collector.manipulate_dataframes(schema_data)
    data = schema_collector.join_tables(cleaned_dataframes)
    print(data)