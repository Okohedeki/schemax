import networkx as nx
import matplotlib.pyplot as plt
from DataFrameJoiner import DatabaseSchemaCollector

class CreateNetwork:
    def __init__(self, server, database):
        self.server = server
        self.database = database
        self.schema_collector = DatabaseSchemaCollector(server, database)
        self.graph = nx.Graph()
    
    def build_network(self):
        # Fetch schema data
        schema_data = self.schema_collector.fetch_schema_data()
        cleaned_dataframes = self.schema_collector.manipulate_dataframes(schema_data)
        data = self.schema_collector.join_tables(cleaned_dataframes)
        
        # Use 'table_joins_df' to build the network
        df = data['table_joins_df']
        
        # Ensure only unique edges are added
        unique_pairs = set()

        for _, row in df.drop_duplicates(subset=['TABLE_NAME', 'TriggerName']).iterrows():
            table_name = row['TABLE_NAME']
            trigger_name = row['TriggerName']
            
            # Add nodes
            if table_name not in self.graph:
                self.graph.add_node(table_name, node_type='table')
            if trigger_name not in self.graph:
                self.graph.add_node(trigger_name, node_type='trigger')
            
            # Add edge if the pair hasn't been added yet
            if (table_name, trigger_name) not in unique_pairs:
                self.graph.add_edge(table_name, trigger_name)
                unique_pairs.add((table_name, trigger_name))

    def visualize_network(self):
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(self.graph, seed=7)  # for consistent layout
        nx.draw(self.graph, pos, with_labels=True, node_size=1500, node_color='lightblue', font_size=10, font_weight='bold')
        plt.show()

if __name__ == "__main__":
    server = 'DESKTOP-1OCA8OH\\SQLEXPRESS'
    database = 'northwind'
    
    network_creator = CreateNetwork(server, database)
    network_creator.build_network()
    network_creator.visualize_network()