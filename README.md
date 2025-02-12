# Some Steps

Some steps to reproduce the error


## Steps

#### Problem 1

1. Clone the GeoServer Cloud repository:
    ```bash
    git clone https://github.com/geoserver/geoserver-cloud.git
    ```
2. run the `pgconfig.sh` file:
    ```bash
    ./pgconfig up -d
    ```
3. Clone this repo:
    ```bash
    git clone https://github.com/romer8/gs-cloud-example.git
    ```

4. Run the `generate_data.sh` file. This will create a table on the `postgis` database called `cities`, and it will insert two records. It will use the `gscloud_dev_pgconfig-postgis-1` running image:

    ```bash
    ./generate_data.sh
    ```
5. Get the IP of the postgis container. We will be using the postgis container that was spin by the `pgconfig.sh` script :
    ```bash
    docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' gscloud_dev_pgconfig-postgis-1
    ```

6. Run the `first_problem.py` python file. This will create a workspace and a datastore:

    ```bash
    python first_problem.py --host <your_ip>  # Replace with your desired IP
    ```
7. You need to create the `SQL` view manually with the following:

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

 
    - SQL view parameters:
        - **name**: id
        - **Default value** : 1
        - **Validation regular expression** : ^[0-9]+$
        

    - Press **Guess geometry type and srid** for the Attributes.

8. Once saved, go to layer preview. You should be able to see the error about the special character: "%"
9. if you come back to the layer and edit the `sql view` and save it, the error will return after you do a new request.

#### Problem 2

1. Get the IP of the postgis container. We will be using the postgis container that was spin by the `pgconfig.sh` script :
    ```bash
    docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' gscloud_dev_pgconfig-postgis-1
    ```

2. Run the `second_problem.py` python file. This will create a workspace,a datastore, and a `sql` view:

    ```bash
    python second_problem.py --host <your_ip>  # Replace with your desired IP
    ```
3. Once saved, go to layer preview. Choose `GeoJSON` for the `WMF` service, You should be able to see that the layer has 0 feature. If you try a `WMS` service it will show an empty white square.