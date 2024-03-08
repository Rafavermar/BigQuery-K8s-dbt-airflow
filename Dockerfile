FROM python:3.9.13

# Update and install system packages
RUN apt-get update -y && \
    apt-get install --no-install-recommends -y -q git libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set working directory
WORKDIR /dbt_bigquery_main

# Copy requirements and install DBT
COPY requirements.txt .
RUN pip install -U pip && \
    pip install -r requirements.txt

# Add your dbt project to the Docker image
COPY dbt_bigquery_main .

# Run dbt clean and dbt deps
RUN dbt clean && \
    dbt deps --project-dir .

