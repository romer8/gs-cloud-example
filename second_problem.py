import argparse
import requests
import json

# Default credentials
USERNAME = "admin"
PASSWORD = "geoserver"

def create_workspace(geoserver_url, workspace_name):
    url = f"{geoserver_url}/rest/workspaces"
    headers = {"Content-Type": "application/json"}
    
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


def create_postgis_store(geoserver_url, workspace_name, store_name, host, port, database, schema, user, passwd):
    url = f"{geoserver_url}/rest/workspaces/{workspace_name}/datastores"
    headers = {"Content-Type": "application/json"}
    
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


def create_sql_view_via_featuretype(geoserver_url, workspace_name, datastore_name, view_name):
    """
    Creates a SQL Parametric View (Virtual Table) by defining a new FeatureType
    in GeoServer. Includes 'attributes' so the server knows the schema.
    """
    url = f"{geoserver_url}/rest/workspaces/{workspace_name}/datastores/{datastore_name}/featuretypes"
    headers = {"Content-Type": "application/json"}

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
    parser = argparse.ArgumentParser(description="GeoServer configuration script")

    # New argument for GeoServer URL
    parser.add_argument("--geoserver-url",
                        type=str,
                        default="http://localhost:9090/geoserver/cloud",
                        help="GeoServer base URL (default: http://localhost:9090/geoserver/cloud)")

    parser.add_argument("--host", 
                        type=str, 
                        default="172.18.0.5", 
                        help="PostGIS database host IP address (default: 172.18.0.5)")

    args = parser.parse_args()

    # Retrieve arguments
    geoserver_url = args.geoserver_url
    host = args.host

    # Fixed or hard-coded variables (adjust as needed)
    workspace_name = "test_view"
    store_name = "test_view_datastore"
    view_name = "cities_sql_view"

    port = "5432"
    database = "postgis"
    schema = "public"
    user = "postgis"
    passwd = "postgis"
    
    # Execution flow
    create_workspace(geoserver_url, workspace_name)
    create_postgis_store(geoserver_url, workspace_name, store_name, host, port, database, schema, user, passwd)
    create_sql_view_via_featuretype(geoserver_url, workspace_name, store_name, view_name)
