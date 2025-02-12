#!/bin/bash
# Description: A template for bash scripts
# Usage: ./generate_data.sh [options]

set -euo pipefail

###############
#  Functions  #
###############

usage() {
    cat <<EOF
Usage: $0 [OPTIONS]

Options:
  -h, --help    Show this help message and exit.
EOF
}

main() {
    echo "Creating Table Cities..."
    docker exec -it gscloud_dev_pgconfig-postgis-1 psql -U postgis -c "CREATE TABLE cities ( id int4 PRIMARY KEY, name varchar(50), geom geometry(POINT,4326) );"
    echo "Inserting Records...."
    docker exec -it gscloud_dev_pgconfig-postgis-1 psql -U postgis -c "INSERT INTO cities (id, geom, name) VALUES (1,ST_GeomFromText('POINT(-0.1257 51.508)',4326),'London_England');"
    docker exec -it gscloud_dev_pgconfig-postgis-1 psql -U postgis -c "INSERT INTO cities (id, geom, name) VALUES (2,ST_GeomFromText('POINT(-81.233 42.983)',4326),'London_Ontario');"
    echo "Finished Inserting Records..."
}

###############
#  Main Flow  #
###############

# Parse command-line arguments
if [[ $# -gt 0 ]]; then
    case "$1" in
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "Error: Unknown option: $1"
            usage
            exit 1
            ;;
    esac
fi

main "$@"