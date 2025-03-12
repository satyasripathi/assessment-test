from confluent_kafka import Consumer, Producer
import json
import time
from datetime import datetime

# Kafka Configurations
KAFKA_BROKER = "localhost:29092"
INPUT_TOPIC = "user-login"
OUTPUT_TOPIC = "processed-user-login"

# Kafka Consumer
consumer_conf = {
    "bootstrap.servers": KAFKA_BROKER,
    "group.id": "user-login-consumer-group",
    "auto.offset.reset": "earliest"
}
consumer = Consumer(consumer_conf)
consumer.subscribe([INPUT_TOPIC])

# Kafka Producer
producer_conf = {"bootstrap.servers": KAFKA_BROKER}
producer = Producer(producer_conf)

def process_message(message):
    """Process and transform Kafka messages"""
    try:
        data = json.loads(message)
        # Convert timestamp to human-readable format
        data["timestamp"] = datetime.utcfromtimestamp(int(data["timestamp"])).strftime('%Y-%m-%d %H:%M:%S')

        # Example Transformation: Flag outdated app versions
        if data.get("app_version") < "2.5.0":
            data["outdated_version"] = True
        else:
            data["outdated_version"] = False

        # Example Filtering: Only store Android users
        if data.get("device_type") == "android":
            return data
    except Exception as e:
        print(f"Error processing message: {e}")
    return None

print("Consuming messages...")

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print(f"Consumer error: {msg.error()}")
        continue

    processed_data = process_message(msg.value().decode("utf-8"))
    if processed_data:
        producer.produce(OUTPUT_TOPIC, json.dumps(processed_data))
        producer.flush()
        print(f"Processed Message: {processed_data}")

consumer.close()

