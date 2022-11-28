#!/bin/bash

# DOCKER BUILD -F means where the Dockerfile is and -t Gives a name and then specify from where the command runs
docker build -f dags/immo-eliza/scraper/Dockerfile -t airflow_tutorial_scraper:latest ./dags/immo-eliza;
docker build -f dags/immo-eliza/model_training/Dockerfile -t airflow_tutorial_training:latest ./dags/immo-eliza;

# INIT AIRFLOW
docker compose up airflow-init;

# RUN AIRFLOW
docker compose --env-file .env up;