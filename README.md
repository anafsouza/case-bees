# Brewery Medallion Pipeline

This repository contains the solution for a data pipeline that ingests, processes, and aggregates brewery data using a **medallion architecture**. The pipeline follows a **three-layer structure**: **Bronze** (raw data ingestion), **Silver** (data transformation), and **Gold** (data aggregation). The goal of this project is to demonstrate an efficient, scalable, and well-monitored data processing pipeline.

## Architecture Overview

The pipeline consists of three layers:

### 1. **Bronze Layer** (Raw Data Ingestion)

In this layer, we fetch brewery data from an external API and store it in its raw form (JSON) in a cloud storage bucket. The `BreweryAPIClient` handles the fetching of the brewery data, which is then written to a cloud storage bucket by the `BronzeLayerWriter`.

### 2. **Silver Layer** (Data Transformation)

In the Silver layer, the raw data is transformed into a more usable format. The `SilverLayerTransformer` processes and cleans the raw data, preparing it for aggregation in the Gold layer. This process may include removing unnecessary fields, filling missing values, and applying any business logic necessary for transformation.

### 3. **Gold Layer** (Data Aggregation)

The final layer performs data aggregation. The `GoldLayerAggregator` processes the data and computes key metrics or statistics needed for downstream consumption. The transformed data is stored back in cloud storage for use by other applications or services.

---

## Setup Instructions

### Prerequisites

* **Airflow**: This pipeline uses Apache Airflow for task orchestration.
* **Python**: Ensure you have Python 3.x installed.
* **Cloud Storage**: A AWS S3 bucket is required for storing the data. The bucket used in this project is named `case-bees`.

### Install Dependencies

Create a virtual environment and install the required dependencies:

```bash
python -m venv venv
source venv/bin/activate  # For Unix/Linux
# OR
venv\Scripts\activate  # For Windows

pip install -r requirements.txt
```

### Running Airflow Locally

To run the pipeline locally, you need to set up Airflow. Follow the steps below:

1. Initialize the Airflow database:

   ```bash
   airflow db init
   ```

2. Start the Airflow webserver and scheduler:

   ```bash
   airflow webserver -p 8080
   airflow scheduler
   ```

3. Open the Airflow UI by visiting `http://localhost:8080` in your browser and trigger the `brewery_medallion_pipeline` DAG.

---

Claro! Aqui está a seção adicional que você pode incluir no seu README, logo após a parte sobre Cloud Services ou em uma seção separada de "Additional Setup":

---

### PySpark Configuration

This project uses **PySpark** as the primary processing engine. In most environments, the pipeline will run without additional setup, assuming you have a working local Spark installation and the necessary dependencies installed via `requirements.txt`.

However, if you encounter any issues running PySpark—such as environment path errors, missing dependencies, or Spark session misconfiguration—you can refer to the setup guide provided in the repository.

📄 **How-To Guide**:
A complete tutorial for setting up PySpark on your machine is available in the `howto/` directory:

```
howto/how_to_setup_pyspark_locally.md
```

This document walks you through:

* Installing Spark locally
* Setting environment variables
* Configuring your Python environment to work with Spark
* Validating your setup with a simple Spark job

Please consult this guide before opening an issue or reaching out for support.

---

## Monitoring and Alerting

To ensure the pipeline operates smoothly, it’s essential to implement monitoring and alerting mechanisms. Below are some steps for achieving this:

### Monitoring

1. **Data Quality Checks**:

   * Perform validation checks after each layer (Bronze, Silver, Gold) to ensure data quality. For example:

     * Check for missing fields or invalid data types.
     * Validate if the expected number of records is present.

2. **Pipeline Failures**:

   * Airflow provides built-in logging that tracks task execution status. Task failure logs should be monitored.
   * Configure retries in case of transient errors, and add custom error handling where needed.

3. **Performance Monitoring**:

   * Monitor Airflow task duration to identify bottlenecks in the pipeline.
   * Use Airflow's monitoring features (e.g., task duration, retries, logs) for tracking performance.

### Alerting

* Use **Airflow's email alerting** to notify the team of task failures or other critical issues.

* Define failure notifications in the DAG configuration:

  ```python
  default_args = {
      "owner": "airflow",
      "retries": 3,
      "retry_delay": timedelta(minutes=5),
      "email_on_failure": True,
      "email_on_retry": False,
      "email": ["team@example.com"]
  }
  ```

* In addition to Airflow alerts, set up monitoring on your cloud storage bucket for failed uploads or access issues.

---

## Repository

This repository includes the following:

* **`DAG Configuration`**: The core logic for orchestrating the brewery pipeline.
* **`API Client`**: A Python class for interacting with the brewery data API.
* **`Processing Modules`**: Separate classes for handling each pipeline layer: Bronze (ingestion), Silver (transformation), and Gold (aggregation).
* **`Dockerfile`**: A Docker configuration for creating an isolated environment for running the pipeline.
* **`requirements.txt`**: List of Python dependencies required for the project.


---

## Cloud Services

This solution requires cloud services for storing the raw and transformed data.


### Testing the Pipeline

For evaluators who prefer not to set up their own cloud storage, I've provided a set of **credentials** that can be used to test the pipeline. These credentials are pre-configured to access the necessary storage resources. Please check the **credentials file** included in the repository for access details.

If you encounter any issues or prefer not to work with cloud storage directly, I've also made the **results of the pipeline available for download** on a static webpage. You can access the data at:

[**Pipeline Results Download Page**](http://case-bees.s3-website-us-east-1.amazonaws.com/)

This page will have all the raw, transformed, and aggregated data available for you to download and review.


## Future Improvements

Here are some potential future improvements for this pipeline:

1. **Real-time Data Ingestion**:

   * Implement real-time streaming for data ingestion using technologies like **Apache Kafka** or **Google Pub/Sub**.

2. **Data Versioning**:

   * Implement version control for the data in the Bronze layer to handle evolving data structures.

3. **Pipeline Optimization**:

   * Improve the performance of data transformation by using **Apache Spark** or **Dask** for parallel processing.

4. **Scalability**:

   * Enhance scalability by running the pipeline on a managed service like **Google Dataflow** or **AWS Glue**.

5. **Data Visualization**:

   * Add dashboards using **Power BI**, **Tableau**, or **Looker** to visualize the aggregated brewery data.

---


