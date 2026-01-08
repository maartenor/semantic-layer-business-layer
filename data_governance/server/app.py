"""
Mock Data Governance Application (think: Collibra)
Demonstrates a data governance platform with REST API for testing and development.
"""

import os
import csv
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)

# Data storage
assets = {}
domains = {}
relationships = {}

# Data directory path
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')


def load_csv_as_dicts(file_path):
    """Load CSV file and return list of dictionaries"""
    with open(file_path, 'r', encoding='utf-8') as f:
        # Detect delimiter by reading first line
        first_line = f.readline()
        f.seek(0)
        delimiter = ';' if ';' in first_line else ','
        reader = csv.DictReader(f, delimiter=delimiter)
        return list(reader)


def load_data():
    """Load CSV data files into memory"""
    global assets, domains, relationships

    # Load domains
    domains_data = load_csv_as_dicts(os.path.join(DATA_DIR, 'domains.csv'))
    for row in domains_data:
        domains[row['domain_id']] = {
            'id': row['domain_id'],
            'name': row['domain_name'],
            'type': {'name': row['domain_type']},
            'description': row['description'],
            'parentId': row['parent_domain'] if row['parent_domain'] else None
        }

    # Load business data objects
    business_data = load_csv_as_dicts(os.path.join(DATA_DIR, 'business_data_objects.csv'))
    for row in business_data:
        assets[row['asset_id']] = create_asset_impl(row, 'business')

    # Load logical data objects
    logical_data = load_csv_as_dicts(os.path.join(DATA_DIR, 'logical_data_objects.csv'))
    for row in logical_data:
        assets[row['asset_id']] = create_asset_impl(row, 'logical')

    # Load technical data objects
    technical_data = load_csv_as_dicts(os.path.join(DATA_DIR, 'technical_data_objects.csv'))
    for row in technical_data:
        assets[row['asset_id']] = create_asset_impl(row, 'technical')

    # Load relationships
    relations_data = load_csv_as_dicts(os.path.join(DATA_DIR, 'relationships.csv'))
    for row in relations_data:
        relationships[row['relation_id']] = {
            'id': row['relation_id'],
            'sourceId': row['source_asset_id'],
            'targetId': row['target_asset_id'],
            'type': {'name': row['relation_type']},
            'description': row['description']
        }

    print(f"Loaded {len(assets)} assets, {len(domains)} domains, and {len(relationships)} relationships")


def create_asset_impl(row, layer_type):
    """Create an AssetImpl object matching Collibra API structure"""
    timestamp = int(datetime.now().timestamp() * 1000)

    # Build attributes based on layer type
    attributes = {}
    excluded_cols = ['asset_id', 'asset_name', 'display_name', 'asset_type', 'domain_id', 'description']
    for col, value in row.items():
        if col not in excluded_cols and value:
            attributes[col] = value

    asset = {
        'id': row['asset_id'],
        'name': row['asset_name'],
        'displayName': row['display_name'],
        'type': {
            'id': str(uuid.uuid4()),
            'name': row['asset_type']
        },
        'domain': {
            'id': row['domain_id'],
            'name': domains.get(row['domain_id'], {}).get('name', 'Unknown Domain')
        },
        'status': {
            'id': str(uuid.uuid4()),
            'name': 'Accepted'
        },
        'createdBy': str(uuid.uuid4()),
        'createdOn': timestamp,
        'lastModifiedBy': str(uuid.uuid4()),
        'lastModifiedOn': timestamp,
        'system': False,
        'resourceType': 'Asset'
    }

    # Add description if available
    if 'description' in row and row['description']:
        asset['description'] = row['description']

    # Add custom attributes
    if attributes:
        asset['attributes'] = attributes

    return asset


@app.route('/api/v2/assets/<asset_id>', methods=['GET'])
def get_asset(asset_id):
    """
    Get a single asset by ID
    Mimics: GET /rest/2.0/assets/{assetId}
    """
    if asset_id not in assets:
        return jsonify({
            'errorCode': 'RESOURCE_NOT_FOUND',
            'message': f'Asset with id {asset_id} not found'
        }), 404

    return jsonify(assets[asset_id])


@app.route('/api/v2/assets', methods=['GET'])
def find_assets():
    """
    Find assets with optional filtering
    Mimics: GET /rest/2.0/assets
    """
    # Get query parameters
    name = request.args.get('name')
    asset_type = request.args.get('typeId') or request.args.get('type')
    domain_id = request.args.get('domainId')
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 100))

    # Filter assets
    filtered_assets = list(assets.values())

    if name:
        filtered_assets = [a for a in filtered_assets if name.lower() in a['name'].lower()]

    if asset_type:
        filtered_assets = [a for a in filtered_assets if a['type']['name'] == asset_type]

    if domain_id:
        filtered_assets = [a for a in filtered_assets if a['domain']['id'] == domain_id]

    # Apply pagination
    total = len(filtered_assets)
    paginated_assets = filtered_assets[offset:offset + limit]

    return jsonify({
        'total': total,
        'offset': offset,
        'limit': limit,
        'results': paginated_assets
    })


@app.route('/api/v2/assets/search', methods=['POST'])
def search_assets():
    """
    Search assets using complex criteria
    Mimics: POST /rest/2.0/assets/search
    """
    search_criteria = request.json or {}

    # Extract search parameters
    name = search_criteria.get('name')
    asset_types = search_criteria.get('typeIds', [])
    domain_ids = search_criteria.get('domainIds', [])
    offset = search_criteria.get('offset', 0)
    limit = search_criteria.get('limit', 100)

    # Filter assets
    filtered_assets = list(assets.values())

    if name:
        filtered_assets = [a for a in filtered_assets if name.lower() in a['name'].lower()]

    if asset_types:
        filtered_assets = [a for a in filtered_assets if a['type']['name'] in asset_types]

    if domain_ids:
        filtered_assets = [a for a in filtered_assets if a['domain']['id'] in domain_ids]

    # Apply pagination
    total = len(filtered_assets)
    paginated_assets = filtered_assets[offset:offset + limit]

    return jsonify({
        'total': total,
        'offset': offset,
        'limit': limit,
        'results': paginated_assets
    })


@app.route('/api/v2/domains', methods=['GET'])
def get_domains():
    """
    Get all domains
    Mimics: GET /rest/2.0/domains
    """
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 100))

    all_domains = list(domains.values())
    total = len(all_domains)
    paginated_domains = all_domains[offset:offset + limit]

    return jsonify({
        'total': total,
        'offset': offset,
        'limit': limit,
        'results': paginated_domains
    })


@app.route('/api/v2/domains/<domain_id>', methods=['GET'])
def get_domain(domain_id):
    """
    Get a single domain by ID
    Mimics: GET /rest/2.0/domains/{domainId}
    """
    if domain_id not in domains:
        return jsonify({
            'errorCode': 'RESOURCE_NOT_FOUND',
            'message': f'Domain with id {domain_id} not found'
        }), 404

    return jsonify(domains[domain_id])


@app.route('/api/v2/relations', methods=['GET'])
def get_relations():
    """
    Get all relations with optional filtering
    Mimics: GET /rest/2.0/relations
    """
    source_id = request.args.get('sourceId')
    target_id = request.args.get('targetId')
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 100))

    # Filter relationships
    filtered_relations = list(relationships.values())

    if source_id:
        filtered_relations = [r for r in filtered_relations if r['sourceId'] == source_id]

    if target_id:
        filtered_relations = [r for r in filtered_relations if r['targetId'] == target_id]

    # Apply pagination
    total = len(filtered_relations)
    paginated_relations = filtered_relations[offset:offset + limit]

    return jsonify({
        'total': total,
        'offset': offset,
        'limit': limit,
        'results': paginated_relations
    })


@app.route('/api/v2/relations/<relation_id>', methods=['GET'])
def get_relation(relation_id):
    """
    Get a single relation by ID
    Mimics: GET /rest/2.0/relations/{relationId}
    """
    if relation_id not in relationships:
        return jsonify({
            'errorCode': 'RESOURCE_NOT_FOUND',
            'message': f'Relation with id {relation_id} not found'
        }), 404

    return jsonify(relationships[relation_id])


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'assets_count': len(assets),
        'domains_count': len(domains),
        'relationships_count': len(relationships)
    })


@app.route('/reload', methods=['POST'])
def reload_data():
    """Reload CSV data from files"""
    try:
        load_data()
        return jsonify({
            'status': 'success',
            'message': 'Data reloaded successfully',
            'assets_count': len(assets),
            'domains_count': len(domains),
            'relationships_count': len(relationships)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api', methods=['GET'])
@app.route('/api/', methods=['GET'])
def api_index():
    """API information endpoint"""
    return jsonify({
        'name': 'Mock Data Governance Application',
        'version': '1.0.0',
        'description': 'A data governance platform (similar to Collibra) with REST API for testing and development',
        'endpoints': {
            'assets': {
                'GET /api/v2/assets/{assetId}': 'Get a single asset by ID',
                'GET /api/v2/assets': 'Find assets with filtering',
                'POST /api/v2/assets/search': 'Search assets using complex criteria'
            },
            'domains': {
                'GET /api/v2/domains': 'Get all domains',
                'GET /api/v2/domains/{domainId}': 'Get a single domain by ID'
            },
            'relations': {
                'GET /api/v2/relations': 'Get all relations with filtering',
                'GET /api/v2/relations/{relationId}': 'Get a single relation by ID'
            },
            'health': {
                'GET /health': 'Health check endpoint'
            }
        }
    })


# Web UI Routes
@app.route('/')
def index():
    """Main web UI landing page"""
    return render_template('index.html',
                         assets_count=len(assets),
                         domains_count=len(domains),
                         relationships_count=len(relationships))


@app.route('/ui/visualization')
def visualization():
    """Relationship model visualization page"""
    # Prepare data for visualization
    nodes = []
    edges = []

    # Helper function to determine if asset is a parent object (not an attribute)
    def is_parent_object(asset_type):
        return 'Data Object' in asset_type or 'Table' in asset_type

    # Helper function to get layer level (for top-down rendering)
    def get_layer_level(asset_type):
        if 'Business' in asset_type:
            return 0  # Top layer
        elif 'Logical' in asset_type:
            return 1  # Middle layer
        elif 'Technical' in asset_type:
            return 2  # Bottom layer
        return 3  # Domain or other

    # Group assets by domain to find parent-child relationships
    domain_objects = {}  # domain_id -> parent object asset_id
    for asset_id, asset in assets.items():
        if is_parent_object(asset['type']['name']):
            domain_objects[asset['domain']['id']] = asset_id

    # Add asset nodes with hierarchy information
    for asset_id, asset in assets.items():
        asset_type = asset['type']['name']
        is_parent = is_parent_object(asset_type)
        level = get_layer_level(asset_type)

        node = {
            'id': asset_id,
            'label': asset['displayName'],
            'group': asset_type,
            'title': f"{asset['name']}\n{asset.get('description', '')}",
            'level': level,
            'is_parent': is_parent
        }

        # If this is an attribute (not a parent object), add edge to parent
        if not is_parent and asset['domain']['id'] in domain_objects:
            parent_id = domain_objects[asset['domain']['id']]
            edges.append({
                'from': parent_id,
                'to': asset_id,
                'label': 'has attribute',
                'color': {'color': '#95a5a6'},
                'dashes': True,
                'arrows': 'to'
            })

        nodes.append(node)

    # Add relationship edges (between layers)
    for rel_id, rel in relationships.items():
        edges.append({
            'from': rel['sourceId'],
            'to': rel['targetId'],
            'label': rel['type']['name'],
            'title': rel.get('description', ''),
            'arrows': 'to'
        })

    return render_template('visualization.html',
                         nodes=nodes,
                         edges=edges)


@app.route('/ui/assets')
def ui_assets():
    """Assets table view page"""
    # Helper functions
    def is_parent_object(asset_type):
        return 'Data Object' in asset_type or 'Table' in asset_type

    def group_by_hierarchy(assets_list):
        """Group assets into parent objects with their attributes"""
        grouped = []
        parents = [a for a in assets_list if is_parent_object(a['type']['name'])]

        for parent in parents:
            # Find attributes in the same domain
            attributes = [a for a in assets_list
                         if not is_parent_object(a['type']['name'])
                         and a['domain']['id'] == parent['domain']['id']]
            grouped.append({
                'parent': parent,
                'attributes': attributes
            })

        return grouped

    # Group assets by type
    business_assets = [a for a in assets.values() if 'Business' in a['type']['name']]
    logical_assets = [a for a in assets.values() if 'Logical' in a['type']['name']]
    technical_assets = [a for a in assets.values() if 'Technical' in a['type']['name']]

    # Create hierarchical groupings
    business_hierarchy = group_by_hierarchy(business_assets)
    logical_hierarchy = group_by_hierarchy(logical_assets)
    technical_hierarchy = group_by_hierarchy(technical_assets)

    return render_template('assets.html',
                         business_assets=business_assets,
                         logical_assets=logical_assets,
                         technical_assets=technical_assets,
                         business_hierarchy=business_hierarchy,
                         logical_hierarchy=logical_hierarchy,
                         technical_hierarchy=technical_hierarchy,
                         all_assets=assets.values())


@app.route('/ui/relationships')
def ui_relationships():
    """Relationships table view page"""
    return render_template('relationships.html',
                         relationships=relationships.values(),
                         domains=domains)


if __name__ == '__main__':
    print("Loading data from CSV files...")
    load_data()
    print(f"Starting Mock Data Governance Application on http://localhost:35000")
    app.run(host='0.0.0.0', port=35000, debug=True)
