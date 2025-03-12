# Real-Time Kafka Data Pipeline

## 🚀 Overview
This project sets up a real-time streaming pipeline** using Kafka & Docker to process user login data.

🛠️ Tech Stack
Kafka (Data streaming)
Docker (Containerization)
Python (Consumer & Producer)

## 📦 Setup

1. git clone on your os terminal using command --> git clone https://github.com/satyasripathi/assessment_test.git
2. Run command to get current working directory on terminal--> pwd
3. Navigate to git project root directory --> cd (project location)
4.python -m venv kafka_env (create python virtual env to install modules)
5.source kafka_env/bin/activate (activate virtual env)

Docker installation:
Mac: 
brew install --cask docker 
Windows:
Go to Docker’s official website and download Docker Desktop for Windows.
Install Docker Desktop
Run the downloaded installer and follow the installation steps.


Execution steps:
1. docker-compose up -d (starts Kafka and zookeeper using Docker)
Note: the above command runs based on docker-compose.yml file.
2. docker ps (Check if the containers are running)

Note: user-login topic is created and data is generated from docker image mpradeep954/fetch-de-data-gen 

3.Run Python script (consumer.py) that consumes data from user-login topic, processes it, and publishes to new topic processed-user-login topic


Note: Processed-user-logic topic has some etl logic where timestamp field is converted to yyyy-mm-dd . Also filtered only android type devices by flagging out latest app versions.

Topic data should look like below:
original msg data:
Produced message: {"user_id": "4a381a71-5a66-4288-b2f8-7935c19aa7f3", "app_version": "2.3.0", "ip": "80.222.149.199", "locale": "CO", "device_id": "798f2ad2-d955-4152-adef-e6e54a979b63", "timestamp": 1741724761, "device_type": "android"}

transformed data (Processed-user-logic topic):
{'user_id': 'd7bcc71e-a4f3-4c4f-8afd-85a6a7dc59ae', 'app_version': '2.3.0', 'ip': '65.43.155.15', 'locale': 'AR', 'device_id': 'd03b36c2-bc44-4826-aa58-8120e0b6834b', 'timestamp': '2025-03-11 20:14:16', 'device_type': 'android', 'outdated_version': True}

post validation steps:
To list kafka topics created,
1. docker exec -it kafka kafka-topics --list --bootstrap-server localhost:29092 (to see topics created in kafka)
output should be generated as : user-login, processed-user-login

2.To view streaming data in the topic, run the command,
docker exec -it kafka kafka-console-consumer --bootstrap-server localhost:29092 --topic processed-user-login --from-beginning

Note: The above commands can also be executed in docker desktop but intalling docker desktop app for respective OS. All logs can be viewed in desktop app.



Production Readiness:

1.How to deploy it to production?
option1 :Self-Managed Deployment (Kubernetes)
Kafka,Zookeeper, and your producer/consumer applications can be deployed using Kubernetes.

option2:
Using cloud technologies like AWS MSK (Managed Streaming for Apache Kafka) or Azure Event Hubs instead of self-managing Kafka.Azure Event Hubs provides a Kafka-compatible endpoint, allowing applications using Apache Kafka to seamlessly interact with Event Hubs without needing to run a self-managed Kafka cluster.

Example if using Azure event hub:

1.Create an Azure Event Hub Namespace
Go to the Azure Portal → Azure Event Hubs
Click Create a resource → Search for Event Hubs
Click Create, then:
Subscription: Select your Azure subscription.
Resource Group: Create a resource group.
Namespace Name: Choose a unique name.
Click Review + Create → Create.

2. Create an Event Hub (Kafka Topic)
Open your Event Hub Namespace.
Go to Event Hubs → 
Enter a name for your Event Hub (e.g., user-login).
Click Create.

3.Get the Kafka Connection String
Go to Event Hub Namespace → Shared Access Policies.
Click on RootManageSharedAccessKey.
Copy the Connection String - Primary Key (needed for Kafka clients).

4.Update Your Docker Compose to Use Azure Event Hub
Modify your docker-compose.yml file to use Azure Event Hubs instead of a local Kafka broker.

5. Update Kafka Consumer Code
Modify your Kafka consumer (e.g., consumer.py) to connect to Azure Event Hubs.

Next Steps
Connect Event Hub to Azure Data Lake or Azure Functions for further processing.
Deploy the Kafka producer in Docker as well.

6.Deploy the Kafka Containers

2.What other components would you want to add to make this production ready?
Add Schema Validation with Confluent Schema Registry: Enforce data schema validation to avoid bad or missing data with Avro/JSON Schema.
Store Processed Data in a Data Lake (S3, Snowflake, ADLS).
Implement Authentication (SASL, TLS) for security.
Use Role-Based Access Control (RBAC): Restrict who can produce/consume messages.
CI/CD & Infrastructure Automation:
Use GitHub Actions or Jenkins/Teamscity for automated builds & deployments.

3.How can this application scale with a growing dataset?

Kafka-Level Scaling:
Increase Kafka Partitions, allowing multiple consumers to process data in parallel.
Consumer Scaling:
Increase Consumer Instances:
Kafka uses Consumer Groups to distribute workload across multiple consumers. Run multiple consumer instances for load balancing.
Use multi-threading for faster execution.
There are many more optimzation techniques for handling large data sets enabling faster and efficient processing.
