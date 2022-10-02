#!/usr/bin/env bash

# list all brokers
./bin/zookeeper-shell.sh localhost:2181 ls /brokers/ids

# create topic
./bin/kafka-topics.sh --zookeeper localhost:2181 --topic bitcoin_transactions --create --partitions 3 --replication-factor 3