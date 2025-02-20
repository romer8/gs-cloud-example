import argparse
import requests
import json

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create GeoServer workspace and PostGIS store.")
    parser.add_argument("--geoserver-url", type=str, default="http://localhost:9090/geoserver/cloud",
                        help="Base URL for the GeoServer instance")
    parser.add_argument("--host", type=str, default="172.18.0.5", help="PostGIS database host IP")
    
    args = parser.parse_args()
    
    geoserver_url = args.geoserver_url
    host = args.host
    
    # Modify these as needed
    workspace_name = "test_view1"
    store_name = "test_view_datastore1"
    
    # Database connection details
    port = "5432"
    database = "postgis"
    schema = "public"
    user = "postgis"
    passwd = "postgis"
    
    create_workspace(geoserver_url, workspace_name)
    create_postgis_store(geoserver_url, workspace_name, store_name, host, port, database, schema, user, passwd)
