FROM bitnami/spark:3.5.0

USER root

# Install Python dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-pip \
    python3-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Install Airflow
WORKDIR /app

COPY dags /app/airflow/dags

#set up airflow environment
ENV AIRFLOW_HOME=/app/airflow
ENV PYTHONPATH="/app:${PYTHONPATH}"
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False

#USER 1001 # Revert to non-root user
