# Real-Time Streaming Data Pipeline for Transport for London(TfL)

This project implements a real-time streaming data pipeline that fetches live transport arrival data from the Transport for London (TFL) API, processes it in a distributed manner, and stores it for analytics. The pipeline leverages the following data engineering tools - all orchestrated with Docker.

- **Apache Airflow**: Schedules and orchestrates the TfL API data ingestion pipeline.
- **Kafka**: Distributed messaging to stream data, buffers transport events (tubes and delays), decoupling data producers and consumers.  
- **Apache Spark**: Consumes from Kafka, parses, and transforms messages.
- **Apache Cassandra**: Stores the final processed data for low latency and higher scalability.
- **PostgreSQL**: Used by Airflow for backend metadata storage.
- **Docker Compose**: Orchestrates all the services on a containerised platform.

## System Architecture



## Project Structure

```text
stream-tfl-to-cassandra/
│
├── dags/
│   ├── kafka.py                 # Airflow DAG to fetch TfL data and push to Kafka
│   └── utils/
│       ├── kafka_utils.py       # Kafka producer utilities
│       └── tfl_api.py           # TfL API wrapper
│
├── spark/
│   ├── stream_to_cassandra.py   # Spark Streaming job to consume Kafka and write to Cassandra
│   └── cassandra_schema.py      # Cassandra schema/table creation script
│
├── docker-compose.yml           # Docker Compose configuration
├── Dockerfile                   
├── requirements.txt             # Python dependencies
├── README.md
└── LICENSE
```          

## Build and Start the Pipeline
docker-compose up -d --build

Docker launches Kafka, Zookeeper, Cassandra, Airflow, Spark master and other dependencies, manages everything in one place

<img width="661" alt="Docker services status" src="https://github.com/user-attachments/assets/191aa374-b30c-4494-9b97-5c9856b6c369" />


## Access Points

| Service              | URL                         | Port |
|----------------------|-----------------------------|------|
| Kafka Control Center | http://localhost:9021       | 9021 |
| Schema Registry      | http://localhost:8081       | 8081 |
| Airflow Web UI       | http://localhost:8080       | 8080 |
| Spark Master UI      | http://localhost:8085       | 8085 |

## Trigger the Airflow DAG
<img width="1530" alt="Airflow DAG" src="https://github.com/user-attachments/assets/d9b40bfc-43ad-4bbb-a1c8-5e5fa57eaa63" />

## Run Spark Job inside Docker
<pre lang="markdown"> docker exec -it tfl_app spark-submit \ 
                      --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,com.datastax.spark:spark-cassandra-connector_2.12:3.4.1 \ 
                      /app/spark/stream_to_cassandra.py </pre>


### Sample Outputs:

We can monitor tfl arrivals of the london's kings cross station being sent to kakfa topic using Control center.

<img width="1176" alt="Control center monitoring" src="https://github.com/user-attachments/assets/227242f0-64c9-4119-89d5-15fddb78c55a" />

Sample data store on cassandra:

<img width="920" alt="TfL_arrivals" src="https://github.com/user-attachments/assets/c894ddea-0b5d-4df4-b598-b3d85750a7f7" />



