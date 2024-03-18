from flask import Blueprint, jsonify
from flask_cors import CORS
from ReactFlowGenerator import ReactFlowNodeGenerator
from DataFrameJoiner import DatabaseSchemaCollector

bp = Blueprint('routes', __name__)
CORS(bp)  # Enable CORS for the blueprint

@bp.route('/getReactFlowData')
def get_react_flow_data():
    server = 'DESKTOP-1OCA8OH\\SQLEXPRESS'
    database = 'northwind'

    # Initialize DatabaseSchemaCollector
    schema_collector = DatabaseSchemaCollector(server, database)

    # Fetch schema data
    schema_data = schema_collector.fetch_schema_data()

    # Manipulate and join dataframes
    cleaned_dataframes = schema_collector.manipulate_dataframes(schema_data)
    cleaned_dataframes = schema_collector.join_tables(cleaned_dataframes)

    # Get the required dataframes
    table_index_join_df = cleaned_dataframes.get('table_joins_df')

    # Initialize ReactFlowNodeGenerator with the required dataframe
    node_generator = ReactFlowNodeGenerator(table_index_join_df)

    # Generate nodes and edges
    nodes, edges = node_generator.generate_node_edges_tablename_triggers()

    return jsonify({'nodes': nodes, 'edges': edges})
