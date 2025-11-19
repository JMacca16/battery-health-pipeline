#!/bin/bash

# Activate virtual environment
source .venv/bin/activate

# Start Docker containers
echo "Starting Docker containers..."
docker-compose -f docker/docker-compose.yml up -d

echo "Waiting for Kafka and Postgres to be ready..."
sleep 3  # wait 15 seconds

# Clear old data
echo "Clearing previous battery data..."
docker exec -i battery_postgres psql -U postgres -d battery_data -c "TRUNCATE TABLE battery_readings;"

# Open consumer in a new terminal tab
osascript <<EOD
tell application "Terminal"
    do script "source $PWD/.venv/bin/activate && python $PWD/src/consumer/consumer.py"
end tell
EOD

# Open producer in a new terminal tab
osascript <<EOD
tell application "Terminal"
    do script "source $PWD/.venv/bin/activate && python $PWD/src/producer/producer.py"
end tell
EOD

echo "Demo running..."
echo "When finished, run './stop_demo.sh' to stop containers."