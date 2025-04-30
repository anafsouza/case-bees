# Base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYSPARK_PYTHON=python3 \
    JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# Install Java and other dependencies
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    curl \
    git \
    wget \
    software-properties-common \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Set Spark and Hadoop versions
ENV SPARK_VERSION=3.5.0 \
    HADOOP_VERSION=3

# Install Spark
RUN wget https://downloads.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    tar -xvzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz -C /opt/ && \
    mv /opt/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /opt/spark && \
    rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

# Set Spark environment variables
ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$PATH

# Configure AWS support (Hadoop AWS lib)
RUN mkdir -p $SPARK_HOME/jars && \
    wget -q https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar -P $SPARK_HOME/jars && \
    wget -q https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.11.1026/aws-java-sdk-bundle-1.11.1026.jar -P $SPARK_HOME/jars

# Set working directory
WORKDIR /app
COPY . /app

# Default command
CMD ["python", "main.py"]
