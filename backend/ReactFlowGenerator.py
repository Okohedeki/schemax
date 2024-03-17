import pandas as pd
from DataFrameJoiner import DatabaseSchemaCollector

class ReactFlowNodeGenerator:
    def __init__(self, table_index_join_df):
        self.table_index_join_df = table_index_join_df

    def generate_node_edges_tablename_triggers(self):
        # Get unique connections between TABLE_NAME and TriggerName
        unique_connections = self.table_index_join_df[['TABLE_NAME', 'TriggerName']].drop_duplicates()

        # Generate initial nodes for TABLE_NAME
        nodes = []
        for table_name in unique_connections['TABLE_NAME'].unique():
            nodes.append({
                'id': table_name,
                'type': 'table_node',  # Define type for table nodes
                'data': {'label': table_name},  # Label is set to the TABLE_NAME
                'position': {'x': 0, 'y': 0},  # Initial position of the node
            })

        # Generate nodes for Triggers
        trigger_nodes = []
        for trigger_name in unique_connections['TriggerName'].unique():
            trigger_nodes.append({
                'id': f'trigger_{trigger_name}',
                'type': 'trigger_node',  # Define type for trigger nodes
                'data': {'label': trigger_name},  # Label is set to the TriggerName
                'position': {'x': 0, 'y': 0},  # Initial position of the node
            })

        nodes.extend(trigger_nodes)

        # Generate edges between TABLE_NAME nodes and Trigger nodes
        edges = []
        for index, row in unique_connections.iterrows():
            table_name = row['TABLE_NAME']
            trigger_name = row['TriggerName']
            edges.append({
                'id': f'{table_name}_{trigger_name}',
                'source': table_name,  # TABLE_NAME node ID
                'target': f'trigger_{trigger_name}',  # Trigger node ID
                'type': 'edge_type',  # Define edge types as needed
                'data': {'label': ''},  # Edge properties
            })

        return nodes, edges

if __name__ == "__main__":
    server = 'DESKTOP-1OCA8OH\\SQLEXPRESS'
    database = 'northwind'

    schema_collector = DatabaseSchemaCollector(server, database)
    schema_data = schema_collector.fetch_schema_data()

    cleaned_dataframes = schema_collector.manipulate_dataframes(schema_data)
    cleaned_dataframes = schema_collector.join_tables(cleaned_dataframes)


    table_index_join_df = cleaned_dataframes.get('table_joins_df')
    view_join_df = cleaned_dataframes.get('view_join_df')
    hash_join_df = cleaned_dataframes.get('hash_join_df')
    stored_procedure_df = cleaned_dataframes.get('stored_procedure_df')
    functions_df = cleaned_dataframes.get('functions_df')

    node_generator = ReactFlowNodeGenerator(table_index_join_df)
    # Generate initial nodes for React Flow
    table_nodes, table_edges = node_generator.generate_node_edges_tablename_triggers()

    # Print the generated nodes
    print(table_nodes)

    print('--------------------------')

    print(table_edges)

