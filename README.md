# Requirements

 - Python3: to ensure you can execute problems scripts.

# Some Steps

Some steps to reproduce the errors.


## Steps

#### Problem 1

1. Clone the GeoServer Cloud repository:
    ```bash
    git clone --recurse-submodules https://github.com/geoserver/geoserver-cloud.git
    git checkout v2.26.2.0
    ```
2. run the `pgconfig` file:
    ```bash
    cd ./geoserver-cloud/compose/
    ./pgconfig up -d
    ```
3. Now clone this repo:
    ```bash
    git clone https://github.com/romer8/gs-cloud-example.git
    ```

4. Run the `generate_data.sh` file. This will create a table on the `postgis` database called `cities`, and it will insert two records. It will use the `gscloud_dev_pgconfig-postgis-1` running image:

    ```bash
    cd ./gs-cloud-example/
    ./generate_data.sh
    ```
5. Get the IP of the postgis container. We will be using the postgis container that was spin by the `pgconfig.sh` script :
    ```bash
    docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' gscloud_dev_pgconfig-postgis-1
    ```

6. Run the `first_problem.py` python file. This will create a workspace and a datastore:

    ```bash
    python3 first_problem.py --host <your_ip>  # Replace with your desired IP
    ```
7. Access the webui (http://localhost:9090/geoserver/cloud/web/ user:admin, pass:geoserver). 
   Then create a layer based on the created datastore (test_view_datastore1), based on the table cities.
   You need to create the `SQL` view manually with the following:

    - sql statement:
        ```sql
            SELECT 
                id,
            name,
                geom 
            FROM 
                cities
            WHERE 
                id = %id%
        ```

 
    - Click on **Guess parameters from SQL** and complete the SQL view parameters as follows:
        - **name**: id
        - **Default value** : 1
        - **Validation regular expression** : ^[0-9]+$
        

    - Click on **Guess geometry type and srid** for the Attributes, and click on Refresh (you will see the list of attributes listed)

8. Once you save the layer, go to layer preview. You should be able to see the error about the special character: "%"
9. if you come back to the layer and edit the `sql view` and save it, the error will return after you do a new request.

#### Problem 2

1. Get the IP of the postgis container. We will be using the postgis container that was spin by the `pgconfig` script :
    ```bash
    docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' gscloud_dev_pgconfig-postgis-1
    ```

2. Run the `second_problem.py` python file. This will create a workspace,a datastore, and a `sql` view:

    ```bash
    python3 second_problem.py --host <your_ip>  # Replace with your desired IP
    ```
3. Once saved, go to layer preview. Choose `GeoJSON` for the `WFS` service, You should be able to see that the layer has 0 feature. If you try a `WMS` service it will show an empty white square.
