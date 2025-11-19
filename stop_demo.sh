#!/bin/bash

echo "Stopping and removing Docker containers..."
docker-compose -f docker/docker-compose.yml down
echo "Containers stopped."