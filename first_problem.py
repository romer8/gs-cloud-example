import argparse
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



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create GeoServer workspace and PostGIS store.")
    parser.add_argument("--host", type=str, default="172.18.0.5", help="PostGIS database host IP")
    args = parser.parse_args()

    workspace_name = "test_view1"
    store_name = "test_view_datastore1"

    # Database connection details
    host = args.host  # Get host from command line
    port = "5432"
    database = "postgis"
    schema = "public"
    user = "postgis"
    passwd = "postgis"
    
    create_workspace(workspace_name)
    create_postgis_store(workspace_name, store_name, host, port, database, schema, user, passwd)
