#!/usr/bin/env bash
/app/wait-for-it.sh kafka:9092 -- sleep 15
python /app/kafka_script.py & python /app/kafka_2.py
