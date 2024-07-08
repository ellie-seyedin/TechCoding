# ETL Pipeline Project

## Overview

This project is an ETL (Extract, Transform, Load) pipeline designed to process and integrate data from multiple sources. The goal is to create a unified database of companies, their assets, and associated indicators that can be easily queried and maintained in a PostgreSQL data warehouse.

## Table of Contents

- [Project Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
- [Running the Pipeline](#running-the-pipeline)
- [Scheduling](#scheduling)
- [Monitoring and Alerting](#monitoring-and-alerting)
- [CI/CD Pipeline](#ci-cd-pipeline)
- [Data Quality and Traceability](#data-quality-and-traceability)
- [Contributing](#contributing)


## Features

- Extract data from CSV and XLSX files.
- Clean and normalize data, handling inconsistencies.
- Fuzzy matching for reconciling company names.
- Load data into a PostgreSQL database.
- Track metadata for each data point.
- Scheduled runs with Airflow.
- Monitoring and alerting with Prometheus and Grafana.

## Technology Stack

- **Python**: Core programming language.
- **PySpark**: For scalable data processing.
- **PostgreSQL**: Data warehouse.
- **Pandas**: For initial data ingestion if necessary.
- **GitHub**: Version control for code and configurations.
- **CLI Tools and CI/CD Integration**: For automation and deployment (e.g., using Jenkins or GitHub Actions).
- **Apache Airflow**: Scheduling.
- **Prometheus**: Monitoring.
- **Grafana**: Alerting.

## Getting Started

### Prerequisites

- Python 3.9 or later
- Docker
- Git
- PostgreSQL

### Installation

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/yourusername/etl-pipeline-project.git
    cd etl-pipeline-project
    ```

2. **Set Up Environment Variables**:
    Create a `.env` file in the project root with the following content:
    ```dotenv
    DATABASE_URL=your_database_url
    DB_USER=your_database_user
    DB_PASSWORD=your_database_password
    ```

3. **Build Docker Image**:
    ```sh
    docker build -t etl-pipeline:latest .
    ```

## Running the Pipeline

### Using Docker

1. **Run the ETL Pipeline**:
    ```sh
    docker run --env-file .env etl-pipeline:latest
    ```

### Local Development

1. **Install Dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

2. **Run the Pipeline**:
    ```sh
    python etl_pipeline.py
    ```

## Scheduling

1. **Install Airflow**:
    ```sh
    pip install apache-airflow
    pip install apache-airflow-providers-docker
    ```

2. **Initialize Airflow**:
    ```sh
    export AIRFLOW_HOME=~/airflow
    airflow db init
    ```

3. **Create DAG**:
    Create a file named `etl_dag.py` in the `~/airflow/dags` directory:
    ```python
    from airflow import DAG
    from airflow.providers.docker.operators.docker import DockerOperator
    from airflow.utils.dates import days_ago
    from datetime import timedelta

    default_args = {
        'owner': 'airflow',
        'depends_on_past': False,
        'email_on_failure': True,
        'email_on_retry': False,
        'email': 'your-email@example.com',
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    }

    dag = DAG(
        'etl_pipeline',
        default_args=default_args,
        description='An ETL pipeline DAG',
        schedule_interval=timedelta(days=1),
        start_date=days_ago(1),
        tags=['etl'],
    )

    etl_task = DockerOperator(
        task_id='run_etl_pipeline',
        image='etl-pipeline:latest',
        auto_remove=True,
        command='python etl_pipeline.py',
        docker_url='unix://var/run/docker.sock',
        network_mode='bridge',
        dag=dag,
    )

    etl_task
    ```

4. **Start Airflow Scheduler and Web Server**:
    ```sh
    airflow scheduler &
    airflow webserver &
    ```

5. **Access Airflow Web Interface**:
    Open your browser and go to `http://localhost:8080` to manage and monitor your DAGs.

## Monitoring and Alerting

1. **Install Prometheus**:
    ```sh
    docker run -d --name=prometheus -p 9090:9090 prom/prometheus
    ```

2. **Configure Prometheus**:
    Create a `prometheus.yml` configuration file:
    ```yaml
    global:
      scrape_interval: 15s

    scrape_configs:
      - job_name: 'airflow'
        static_configs:
          - targets: ['localhost:8080']
    ```

3. **Mount Configuration and Restart Prometheus**:
    ```sh
    docker run -d --name=prometheus -p 9090:9090 -v /path/to/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus
    ```

4. **Install Grafana**:
    ```sh
    docker run -d --name=grafana -p 3000:3000 grafana/grafana
    ```

5. **Access Grafana**:
    Open your browser and go to `http://localhost:3000`. Default login is `admin/admin`.

6. **Add Prometheus as Data Source**:
    - Go to Grafana, navigate to Configuration > Data Sources > Add Data Source.
    - Select Prometheus and configure the URL as `http://localhost:9090`.

7. **Create Dashboards**:
    - Create dashboards to visualize ETL metrics, such as job success rate, duration, and error rates.

8. **Setup Alerts**:
    - Configure alerts in Grafana based on your metrics.
    - Use email or other notification channels to receive alerts.

## CI/CD Pipeline

This project uses GitHub Actions for continuous integration and deployment.

### Workflow

1. **Build and Test**:
    - On every push to the `main` branch, the workflow builds the Docker image and runs tests.

2. **Deployment**:
    - After successful tests, the workflow deploys the ETL pipeline.

### Configuration

- GitHub Secrets:
    - `DATABASE_URL`
    - `DB_USER`
    - `DB_PASSWORD`

## Data Quality and Traceability

- **Data Quality**:
    - Use PySpark for data cleaning and validation.
    - Regularly monitor data quality metrics.

- **Data Traceability**:
    - Maintain detailed metadata in PostgreSQL.
    - Track source file, load timestamp, and transformation history.
    - Implement logging in the ETL process.

- **Error Correction**:
    - Implement automated error detection and reporting.
    - Allow manual intervention for detected errors.

## Data Integration

- **Data Ingestion**:
    - Load CSV and XLSX files using PySpark.

- **Data Cleaning and Standardization**:
    - Clean and normalize data using PySpark.

- **Data Transformation**:
    - Use fuzzy matching to reconcile company names.
    - Generate unique IDs for companies and assets.

- **Unified Schema**:
    - Define a unified schema in PostgreSQL.

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**:
    - Click the "Fork" button at the top right of this page.

2. **Clone Your Fork**:
    ```sh
    git clone https://github.com/yourusername/etl-pipeline-project.git
    ```

3. **Create a Branch**:
    ```sh
    git checkout -b feature/your-feature-name
    ```

4. **Make Your Changes** and **Commit**:
    ```sh
    git commit -m "Add some feature"
    ```

5. **Push to Your Branch**:
    ```sh
    git push origin feature/your-feature-name
    ```

6. **Create a Pull Request**.

