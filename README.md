# Real-Time Streaming Data Pipeline for Transport for London(Tfl)

stream-tfl-to-cassandra is an end-to-end real-time data streaming pipeline that ingests live arrivals data from the Transport for London (TfL) API. Built using popular technologies like Apache Airflow, Apache Kafka, Cassandra and Docker.

# Architecture Overview

- **Apache Airflow**: Schedules and orchestrates the TfL API data ingestion pipeline.
- **Kafka**: Broker for streaming data, Buffers real-time transport events (tubes and delays).  
- **Apache Spark**: Consumes from Kafka, parses, and transforms messages.
- **Apache Cassandra**: Stores the final processed data for low latency and higher scalability.
- **PostgreSQL**: Used by Airflow for backend metadata storage.
- **Docker Compose**: Orchestrates all services for local development.

# Project Structure

stream-tfl-to-cassandra/
│
├── dags/
│       └── kafka.py  # DAG to hit TFL API and push to Kafka
│       └── utils/
│                └── kafka_utils.py
│                └── tfl_api.py
│
├── spark/
│   ├── stream_to_cassandra.py        # Spark Streaming jobs
│   └── cassandra_schema.py           # creates Cassandra tables
│
├── docker-compose.yml                # Full pipeline with Airflow, Spark, Kafka, Cassandra
├── Dockerfile                        # Example env vars (like TFL API key, Kafka host)
├── requirements.txt                  # Python requirements
├── README.md                         # ← You’ll write this
└── LICENSE                           # (Optional) MIT/Apache license

# Build and Start the Pipeline
docker-compose up -d --build

Docker launches Kafka, Zookeeper, Cassandra, Airflow, Spark master and other dependencies, manages everything in one place

# Access points
Service	URL	Port
Kafka Control Center	http://localhost:9021	9021
Schema Registry	http://localhost:8081	8081
Airflow Web UI	http://localhost:8080	8080
Spark Master UI	http://localhost:8085	8085
# Trigger the Airflow DAG
<img width="1530" alt="Airflow DAG" src="https://github.com/user-attachments/assets/d9b40bfc-43ad-4bbb-a1c8-5e5fa57eaa63" />

# Run Spark Job
- docker exec -it tfl_app spark-submit \
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,com.datastax.spark:spark-cassandra-connector_2.12:3.4.1 \
/app/spark/stream_to_cassandra.py
# Sample Outputs:

We can monitor tfl arrivals of the london's kings cross station being sent to kakfa topic using Control center.

<img width="1176" alt="Control center monitoring" src="https://github.com/user-attachments/assets/227242f0-64c9-4119-89d5-15fddb78c55a" />

Data stored on cassandra:

<img width="920" alt="TfL_arrivals" src="https://github.com/user-attachments/assets/c894ddea-0b5d-4df4-b598-b3d85750a7f7" />



