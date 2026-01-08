# Mock Data Governance Application (think: Collibra)

A lightweight Python Flask application that demonstrates a data governance platform (similar to Collibra) for testing and development purposes, with an interactive web UI for visualizing data governance models and a REST API.

## Features

- Implements REST API endpoints for assets, domains, and relationships (Collibra-compatible format)
- Returns data in AssetImpl structure format similar to Collibra API
- Loads data from CSV files representing business, logical, and technical data objects
- Supports filtering, pagination, and search operations
- CORS enabled for cross-origin requests
- **Interactive Web UI** with hierarchical relationship visualization and collapsible table views

## Installation

1. Install dependencies:
```bash
python.exe -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

1. Start the server:
```bash
python app.py
```

The server will start on `http://localhost:35000`

2. Access the Web UI:

Open your browser and navigate to `http://localhost:35000` to access the interactive web interface.

## Web UI

The server includes a comprehensive web interface for visualizing and browsing your data governance model:

### Pages

1. **Home** (`/`) - Dashboard with statistics and quick links
2. **Relationship Model** (`/ui/visualization`) - Interactive hierarchical network diagram showing data objects, their attributes, and cross-layer relationships
3. **Assets** (`/ui/assets`) - Hierarchical tabular view with collapsible groups showing data objects and their attributes
4. **Relationships** (`/ui/relationships`) - Detailed table of all relationships with filtering and search

### Key Features

#### Hierarchical Visualization
- **Top-down layering**: Business layer at top → Logical layer in middle → Technical layer at bottom
- **Object-Attribute Hierarchy**: Data objects (Customer, Machine) shown as boxes with their attributes as ellipses
- **Visual Relationships**: Solid lines show cross-layer mappings, dashed lines show object-to-attribute relationships
- **Interactive Controls**: Zoom, pan, fit-to-screen, and click-to-explore
- **Color-coded nodes**: Different colors for Business (blue), Logical (purple), and Technical (green) layers

#### Hierarchical Tables
- **Collapsible Groups**: Each data object is a collapsible section containing its attributes
- **Layer-specific Views**:
  - Business: Shows business definitions, ownership, and stewardship
  - Logical: Shows data types, nullability, and primary keys
  - Technical: Shows physical columns with data types, lengths, and constraints
- **Tree Visualization**: Attributes displayed with `└─` symbols showing parent-child relationships
- **Search and Filter**: Quick search across all assets within each layer

#### General Features
- Interactive network visualization using vis.js
- Real-time data from CSV files
- Responsive design
- CORS enabled for API access

## API Testing

Test the REST API endpoints:
```bash
# Get server info
curl http://localhost:35000/

# Health check
curl http://localhost:35000/health

# Get all assets
curl http://localhost:35000/api/v2/assets

# Get specific asset
curl http://localhost:35000/api/v2/assets/BDO-CUST-001

# Get all domains
curl http://localhost:35000/api/v2/domains

# Get relations for an asset
curl "http://localhost:35000/api/v2/relations?sourceId=LDO-CUST-001"
```

## API Endpoints

### Assets

- `GET /api/v2/assets/{assetId}` - Get a single asset by ID
- `GET /api/v2/assets?name={name}&typeId={type}&domainId={domain}` - Find assets with filtering
- `POST /api/v2/assets/search` - Search assets using complex criteria

### Domains

- `GET /api/v2/domains` - Get all domains
- `GET /api/v2/domains/{domainId}` - Get a single domain by ID

### Relations

- `GET /api/v2/relations?sourceId={id}&targetId={id}` - Get relations with filtering
- `GET /api/v2/relations/{relationId}` - Get a single relation by ID

### Utility

- `GET /health` - Health check endpoint
- `GET /` - API information and documentation

## Data Structure

The server loads data from CSV files in the `../data` directory:

- `business_data_objects.csv` - Business layer with 2 data objects (Customer, Machine) and their attributes
- `logical_data_objects.csv` - Logical layer with 1-to-1 mapping from business to technical
- `technical_data_objects.csv` - Technical layer with physical tables (customers, machines) and columns
- `relationships.csv` - Relationships mapping between layers and object-attribute hierarchies
- `domains.csv` - Domain definitions organizing the data objects

### Example Data Objects

**Customer** (Business → Logical → Technical):
- Business Attributes: Customer ID, Customer Name, Country
- Logical Attributes: customer_id, customer_name, country
- Technical Columns: customer_id (VARCHAR, PK), customer_name (VARCHAR), country (VARCHAR)

**Machine** (Business → Logical → Technical):
- Business Attributes: Machine Number, Customer, Machine Type, Model
- Logical Attributes: machine_nr, customer_id, machine_type, model
- Technical Columns: machine_nr (VARCHAR, PK), customer_id (VARCHAR, FK), machine_type (VARCHAR), model (VARCHAR)

## Response Format

All responses follow the Collibra API AssetImpl structure as documented in the [Collibra Core documentation](https://github.com/chorvathdev/collibra-core/blob/master/docs/AssetImpl.md).

Example asset response:
```json
{
  "id": "BDO-CUST-001",
  "name": "Customer",
  "displayName": "Customer",
  "type": {
    "id": "...",
    "name": "Business Data Object"
  },
  "domain": {
    "id": "DOM-BUSINESS-001",
    "name": "Customer Management"
  },
  "status": {
    "id": "...",
    "name": "Accepted"
  },
  "description": "Customer information including identification and location details",
  "createdBy": "...",
  "createdOn": 1234567890000,
  "lastModifiedBy": "...",
  "lastModifiedOn": 1234567890000,
  "resourceType": "Asset"
}
```

## Data Model Structure

The mock server demonstrates a three-layer data governance architecture:

### Layer Hierarchy
1. **Business Layer** (Top) - Business-friendly view
   - **Data Objects**: Customer, Machine
   - **Attributes**: Business definitions with stewardship and ownership information

2. **Logical Layer** (Middle) - Conceptual data model
   - **Data Objects**: Logical entities mapping business to technical
   - **Attributes**: Data types, nullability, primary keys

3. **Technical Layer** (Bottom) - Physical implementation
   - **Tables**: PostgreSQL database tables (customers, machines)
   - **Columns**: Physical columns with data types, lengths, and constraints

### Relationship Types
- **Maps To**: Business → Logical layer mappings
- **Implements**: Logical → Technical layer mappings
- **Has Attribute**: Object → Attribute relationships (shown with dashed lines)
- **Foreign Key**: Technical table relationships

## UI Features

### Relationship Visualization
The interactive hierarchical network diagram shows:
- **Top-down layout**: Business objects at top, Logical in middle, Technical at bottom
- **Shape distinction**: Boxes represent data objects/tables, Ellipses represent attributes/columns
- **Color coding**:
  - Blue (#2196F3) = Business objects, Light blue (#64B5F6) = Business attributes
  - Purple (#9C27B0) = Logical objects, Light purple (#BA68C8) = Logical attributes
  - Green (#4CAF50) = Technical tables, Light green (#81C784) = Technical columns
- **Relationship lines**: Solid for cross-layer mappings, Dashed for object-attribute relationships
- **Interactive controls**: Hover tooltips, zoom, pan, fit-to-screen
- **Click navigation**: Click nodes or edges to view details in console

### Assets Table View
- **Tabbed interface**: Separate tabs for All Assets, Business, Logical, and Technical layers
- **Collapsible groups**: Each data object is a collapsible card showing:
  - Object header with type badge, name, and metadata
  - Expandable/collapsible attribute table (click header to toggle)
  - Attribute count and additional metadata (owner, schema.table, etc.)
- **Hierarchical display**: Attributes shown with tree symbols (`└─`) under parent objects
- **Layer-specific columns**:
  - Business: Business Definition, Data Steward, Business Owner
  - Logical: Data Type, Nullable, Primary Key, Maps To
  - Technical: Data Type, Max Length, Nullable, Primary Key, Source System

### Relationships Table
- **Complete relationship listing** with filtering
- **Statistics dashboard**: Counts by relationship type (maps to, implements, foreign key)
- **Search functionality**: Filter across all fields
- **Visual relationship flow examples**: Shows common patterns like Business → Logical → Technical flows

## Development

This is a mock application for development and testing. It does not implement:
- Authentication/authorization
- Data persistence (changes are lost on restart)
- Full CRUD operations (POST, PUT, DELETE)
- Advanced data governance features like workflows, data quality rules, responsibilities, etc.

For production use, consider using a real data governance platform like Collibra, or build upon this foundation.

## Port Configuration

The server runs on port **35000** to avoid conflicts with other common services. You can change this in [app.py](app.py:405) if needed.

## References:
- Collibra Data Governance application API wrappre for Pyhton: https://github.com/chorvathdev/collibra-core
- Using
  - https://github.com/chorvathdev/collibra-core/blob/master/docs/AssetsApi.md#get_asset 
  - https://github.com/chorvathdev/collibra-core/blob/master/docs/AssetImpl.md 
  - to get an idea of API responses.
- Collibra API docs: https://developer.collibra.com/tutorials/getting-started-with-the-rest-api 
