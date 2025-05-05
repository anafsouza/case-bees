# Use the official Python 3.8 image as a base image
FROM python:3.8-slim

# Set environment variables to non-interactive to prevent tzdata prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies for Spark and Airflow
RUN apt-get update && apt-get install -y \
    curl \
    openjdk-8-jdk \
    bash \
    build-essential \
    libs3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Apache Spark
RUN curl -sL https://archive.apache.org/dist/spark/spark-3.1.2/spark-3.1.2-bin-hadoop3.2.tgz | tar -xz -C /opt \
    && mv /opt/spark-3.1.2-bin-hadoop3.2 /opt/spark

# Install Apache Airflow and other necessary Python libraries
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set environment variables for Spark
ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$PATH
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3

# Set the working directory inside the container
WORKDIR /usr/local/airflow

# Copy your DAGs and source code into the container
COPY ./dags /usr/local/airflow/dags
COPY ./src /usr/local/airflow/src

# Set up permissions for the Airflow user
RUN useradd -ms /bin/bash airflow && \
    chown -R airflow:airflow /usr/local/airflow && \
    chmod -R 755 /usr/local/airflow

USER airflow

# Expose Airflow UI port
EXPOSE 8080

# Start the Airflow scheduler and webserver in the background
CMD ["bash", "-c", "airflow db init && airflow scheduler & airflow webserver"]
