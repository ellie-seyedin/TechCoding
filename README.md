# ETL Pipeline Project

## Overview

This project is an ETL (Extract, Transform, Load) pipeline designed to process and integrate data from multiple sources. The goal is to create a unified database of companies, their assets, and associated indicators that can be easily queried and maintained in a PostgreSQL data warehouse.

## Table of Contents

- [Project Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
- [Running the Pipeline](#running-the-pipeline)
- [CI/CD Pipeline](#ci-cd-pipeline)
- [Data Quality and Traceability](#data-quality-and-traceability)
- [Contributing](#contributing)

## Features

- Extract data from CSV and XLSX files.
- Clean and normalize data, handling inconsistencies.
- Fuzzy matching for reconciling company names.
- Load data into a PostgreSQL database.
- Track metadata for each data point.

## Technology Stack

- **Python**: Core programming language.
- **PySpark**: Data processing.
- **PostgreSQL**: Data warehouse.
- **Pandas**: Initial data ingestion.
- **GitHub Actions**: CI/CD pipeline.

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

- **Data Cleaning**: Uses PySpark for data cleaning and normalization.
- **Fuzzy Matching**: Reconciles company names using fuzzy matching.
- **Metadata Tracking**: Maintains metadata in PostgreSQL for traceability.
- **Error Handling**: Implements automated error detection and manual correction mechanisms.

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
