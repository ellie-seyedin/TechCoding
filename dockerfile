# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Install Java for PySpark
RUN apt-get update && apt-get install -y openjdk-11-jdk && apt-get clean

# Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# Install necessary Python packages
RUN pip install pyspark thefuzz pandas

# Copy the ETL pipeline code to the container
COPY . /app

# Set the working directory
WORKDIR /app

# Entry point for the Docker container
CMD ["python", "etl_pipeline.py"]
