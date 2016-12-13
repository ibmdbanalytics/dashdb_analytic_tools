# IoT demo data producer docker container

This Kafka producer simulates IoT data from a wind turbine.

1. Build docker image:
  `docker build -t iotproducer .`

2. Run docker container:
  `docker run --net=host -d --name=iotproducer iotproducer`
  
This starts up Kafka, configures a topic and starts up a little IoT producer 
app that writes a mock IoT message to the topic every second. 

By default it writes 1000 messages and then it ends. You can change the number
of messages written by specifying an integer number as parameter to the 
container, like:
  `docker run --net=host -d --name=iotproducer iotproducer 5000`
  
You can observe the IoT messages running the following command:
  `docker exec -it iotproducer kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic iot4dashdb --from-beginning`
