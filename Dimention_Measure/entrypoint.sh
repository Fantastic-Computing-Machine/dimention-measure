
# #!/usr/bin/env bash

# echo "Waiting for MySQL..."

# while ! nc -z sql_database 3306; do
#   sleep 0.5
# done

# echo "MySQL started"

# flask sql_database init
# flask sql_database migrate
# flask sql_database upgrade

# cd /FantasticComputingMachine
# python app.py