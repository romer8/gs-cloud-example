import requests
import json

# Replace these values with those appropriate for your GeoServer (or GeoServer Cloud) instance
GEOSERVER_URL = "http://localhost:9090/geoserver/cloud"
USERNAME = "admin"
PASSWORD = "geoserver"

# 1) Create a new workspace named `test_view` with the namespace URI also called `test_view`
def create_workspace(workspace_name):
    url = f"{GEOSERVER_URL}/rest/workspaces"
    headers = {"Content-Type": "application/json"}
    
    # This JSON structure aligns with the GeoServer REST API for creating a workspace.
    # You can also specify a different namespace URI by adjusting the 'uri' field.
    payload = {
        "workspace": {
            "name": workspace_name
        }
    }
    response = requests.post(
        url,
        data=json.dumps(payload),
        headers=headers,
        auth=(USERNAME, PASSWORD)
    )
    
    if response.status_code in [200, 201]:
        print(f"Workspace '{workspace_name}' created successfully.")
    elif response.status_code == 401:
        print("Authentication failed. Check your credentials.")
    else:
        print(f"Failed to create workspace '{workspace_name}'. Status code: {response.status_code}")
        print("Response content:", response.text)


# 2) Create a PostGIS data store in the new workspace
def create_postgis_store(workspace_name, store_name, host, port, database, schema, user, passwd):
    url = f"{GEOSERVER_URL}/rest/workspaces/{workspace_name}/datastores"
    headers = {"Content-Type": "application/json"}
    
    # Connection parameters for a PostGIS store
    payload = {
        "dataStore": {
            "name": store_name,
            "type": "PostGIS",
            "connectionParameters": {
                "host": host,
                "port": port,
                "database": database,
                "schema": schema,
                "user": user,
                "passwd": passwd,
                # This is mandatory to specify that we are using a PostGIS database
                "dbtype": "postgis"
            }
        }
    }

    response = requests.post(
        url,
        data=json.dumps(payload),
        headers=headers,
        auth=(USERNAME, PASSWORD)
    )
    
    if response.status_code in [200, 201]:
        print(f"PostGIS store '{store_name}' created successfully in workspace '{workspace_name}'.")
    else:
        print(f"Failed to create store '{store_name}'. Status code: {response.status_code}")
        print("Response content:", response.text)


def create_sql_view_via_featuretype(workspace_name, datastore_name, view_name):
    """
    Creates a SQL Parametric View (Virtual Table) by defining a new FeatureType
    in GeoServer. Includes 'attributes' so the server knows the schema.
    """
    url = f"{GEOSERVER_URL}/rest/workspaces/{workspace_name}/datastores/{datastore_name}/featuretypes"
    headers = {"Content-Type": "application/json"}

    # Define the SQL, parameters, geometry, etc.
    sql_statement = """
SELECT
  id,
  name,
  geom
FROM
  cities
WHERE
  id = %id%
""".strip()

    payload = {
        "featureType": {
            "enabled": True,
            "store": {
                "@class": "dataStore",
                # Must be "<workspace>:<datastore_name>" 
                "name": f"{workspace_name}:{datastore_name}"
            },
            "name": view_name,
            "nativeName": view_name,
            "title": view_name,
            "srs": "EPSG:4326",
            "metadata": {
                "virtualTable": {
                    "name": view_name,
                    "sql": sql_statement,
                    "keyColumn": "id",
                    "geometry": {
                        "name": "geom",
                        "type": "Point",
                        "srid": 4326
                    },
                    "parameters": [
                        {
                            "name": "id",
                            "defaultValue": "1",
                            "regexpValidator": "^[0-9]+$"
                        }
                    ]
                }
            },
            # Explicitly declare your schema columns:
            "attributes": {
                "attribute": [
                    {
                        "name": "id",
                        "binding": "java.lang.Integer",
                        "minOccurs": 0,
                        "maxOccurs": 1,
                        "nillable": False
                    },
                    {
                        "name": "name",
                        "binding": "java.lang.String",
                        "minOccurs": 0,
                        "maxOccurs": 1,
                        "nillable": True
                    },
                    {
                        "name": "geom",
                        # For older versions of GeoServer (pre-2.16), use:
                        # "binding": "com.vividsolutions.jts.geom.Point"
                        "binding": "org.locationtech.jts.geom.Point",
                        "minOccurs": 0,
                        "maxOccurs": 1,
                        "nillable": True
                    }
                ]
            }
        }
    }

    response = requests.post(
        url,
        data=json.dumps(payload),
        headers=headers,
        auth=(USERNAME, PASSWORD)
    )

    if response.status_code in [200, 201]:
        print(f"SQL parametric view '{view_name}' created & published successfully (via FeatureType).")
    else:
        print(f"Failed to create SQL parametric view '{view_name}'. "
              f"Status code: {response.status_code}")
        print("Response content:", response.text)


if __name__ == "__main__":
    workspace_name = "test_view"
    store_name = "test_view_datastore"
    view_name = "cities_sql_view"

    # Database connection details
    host = "172.18.0.5"
    port = "5432"
    database = "postgis"
    schema = "public"
    user = "postgis"
    passwd = "postgis"
    
    # 1) Create the workspace
    create_workspace(workspace_name)
    
    # 2) Create the PostGIS data store
    create_postgis_store(workspace_name, store_name, host, port, database, schema, user, passwd)

    # 2) Create SQL view
    create_sql_view_via_featuretype(workspace_name, store_name, view_name)