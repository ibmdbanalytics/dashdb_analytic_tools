#!/bin/bash
# (c) Copyright IBM Corporation 2016
# LICENSE: BSD-3, https://opensource.org/licenses/BSD-3-Clause

# A little script that starts up the Kafka environment, creates a topic 'iot4dashdb'
# and feeds some randomly generated sample data into the topic using the Kafka
# command-line producer scipt

if [ "$#" -ne 1 ] && [ "$#" -ne 5 ]; then
    echo "Illegal number of parameters"
    echo "Usage: $0 <counter> [<ID> <POWER_LVL> <NOISE> <TEMP_MIN>]"
    exit 1
fi

#Start servers

zookeeper/bin/zkServer.sh start

kafka/bin/kafka-server-start.sh -daemon kafka/config/server.properties

sleep 5
echo Create Topic
kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic iot4dashdb

echo LIST of TOPICS:
kafka/bin/kafka-topics.sh --list --zookeeper localhost:2181


#Start producer

TEMP_MIN=30
TEMP_OUT=18
TEMP_RANGE=9
ID=2700
COUNTER=3
SLEEPS=0.05
POWER_LVL=1827
DEV_TYPE="windGen"
NOISE=82

COUNTER="$1"

if [ "$#" -ge 2 ]; then
    ID="$2"
    POWER_LVL="$3"
    NOISE="$4"
    TEMP_MIN="$5"
fi

while [  $COUNTER -ge 1 ]; do

    COUNTER=COUNTER-1
    DEV_ID=$ID+$RANDOM%10
    TS=`date +"%F %T"`
    TEMP=$TEMP_MIN+$RANDOM%$TEMP_RANGE
    POWER=$POWER_LVL+$RANDOM%10

    JSON="{\"payload\": {\"temperature\": $TEMP,\"tempOutside\": $TEMP_OUT,\"powerProd\": $POWER,\"noiseLevel1\": $NOISE,\"time\":\"$TS\"},\"deviceId\": \"$DEV_ID\",\"deviceType\": \"$DEV_TYPE\",\"eventType\": \"status\"}"
    echo $JSON | kafka/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic iot4dashdb

    sleep $SLEEPS
done
