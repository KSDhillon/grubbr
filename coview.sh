#!/usr/bin/env bash
docker exec -it spark-master bash -c "/tmp/data/setup.sh"
docker exec -it spark-worker bash -c "/tmp/data/setup.sh"

while [[ true ]]; do
    docker exec -it spark-master bin/spark-submit --master spark://spark-master:7077 --total-executor-cores 2 --executor-memory 512m /tmp/data/coview.py
    sleep 120    
done
