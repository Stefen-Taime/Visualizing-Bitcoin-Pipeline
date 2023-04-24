
## Visualizing Bitcoin to USD Exchange Rates using FastAPI, Prometheus, Grafana, Deploy with jenkins On Localhost Ubuntu Server 20.04

In this article, we’ll explore how to visualize the exchange rate of Bitcoin to USD using FastAPI, Prometheus, Grafana, and Docker. We will create a simple FastAPI application to import exchange rate data from an API, store it in a database, and expose it as metrics using Prometheus. Then, we’ll use Grafana to create dashboards that visualize the data, and deploy the whole setup using Docker and Jenkins. Inspired by the article of [amlanscloud](https://amlanscloud.com/kubechallenge/)

[Setup Jenkins Agent/Slave Using SSH [Password & SSH Key]](https://devopscube.com/setup-slaves-on-jenkins-2/)

## Overview

![](https://cdn-images-1.medium.com/max/3816/1*oc4RMB_AVLUm0MPzM0tGnA.png)

Here’s an outline of our plan:

 1. Data Source: The process commences by acquiring data from a public data source. In this case, we’ll use an API that offers free exchange rates for Bitcoin to USD. The API delivers the exchange rate between Bitcoin and USD at the moment the API is called. By invoking the API multiple times, we can obtain time series data for the fluctuations in the exchange rate.

 2. Data Importer App: An importer app reads the data from the data source API mentioned above. This app operates daily, invoking the data source API to acquire the exchange rate. Subsequently, the importer app stores this rate in a database. Each day’s exchange rate is represented by a row of items in the database.

 3. Prometheus Data Scraper: This component is a data scraper job defined within Prometheus. The Prometheus data scraper fetches data from an API endpoint and incorporates it as a metric in Prometheus. A custom API has been developed for this purpose, which, upon invocation, retrieves the day’s exchange rate from the database and returns the data in a format that can be easily read and imported as a metric in Prometheus.

 4. Visualize Data: Prometheus stores the data scraped as a distinct metric. This metric serves as a data source for creating visualization dashboards on Grafana. These dashboards display various trends in the exchange rate fluctuations as documented by the metrics.

 5. Deployment: We will deploy the entire setup using Jenkins, Docker, and Docker Compose.

  
    

FastAPI application that fetches the Bitcoin to USD exchange rate from an external API and stores the data in a Redis database. It also exposes the exchange rate data as Prometheus metrics. Let’s break down the code:

 1. Import necessary modules: The code starts by importing the required modules such as FastAPI, uvicorn, dotenv, os, requests, json, prometheus_client, datetime, and redis.

 2. Load environment variables: The load_dotenv() function is called to load the environment variables from the .env file.

 3. Scrape exchange rate data: The scrape_data() function fetches the exchange rate data by making a GET request to the external API using the requests library. It then extracts the exchange rate and formats it as a float with two decimal places.

 4. Initialize Prometheus Gauge: A Prometheus Gauge named exchange_rate_btc_usd is initialized to store the exchange rate data.

 5. Create FastAPI app: A FastAPI application named app is created.

 6. Define endpoints:

* GET /: A simple Hello World endpoint that returns a JSON response.

* GET /exchangemetrics: This endpoint fetches the exchange rate data for the current day from the Redis database and sets the value of the Prometheus Gauge exchange_rate_btc_usd. It then returns the Prometheus metrics as a plain text response.

* GET /getexchangedata: This endpoint fetches the exchange rate data by calling the scrape_data() function, stores the data in the Redis database, and returns a plain text response indicating whether the operation was successful.

7. Run FastAPI app: The FastAPI app is run using uvicorn with the host set to “0.0.0.0” and port 5000. The reload=True parameter enables hot-reloading during development.

## Prometheus

It sets up Prometheus to scrape metrics from two different sources: Prometheus itself and a FastAPI application. Let’s break down the configuration:

 1. Global settings: The global settings apply to all the scrape jobs defined in the configuration.

* scrape_interval: The interval at which Prometheus scrapes metrics from the targets. In this case, it's set to 15 seconds.

2. Scrape configs: The scrape_configs section defines the jobs that Prometheus will use to scrape metrics from different sources.

* job_name: 'prometheus': The first job is named 'prometheus' and is configured to scrape metrics from the Prometheus server itself.

* static_configs: This section specifies the target for this job. In this case, it's set to scrape metrics from the Prometheus server running on 'localhost:9090'.

* job_name: 'fastapi_app': The second job is named 'fastapi_app' and is configured to scrape metrics from the FastAPI application.

* metrics_path: The path to the metrics endpoint in the FastAPI application, which is '/exchangemetrics' in this case.

* static_configs: This section specifies the target for this job. In this case, it's set to scrape metrics from the FastAPI application running on 'fastapi_app:5000' (the application's hostname and port).

   
## Jenkins

which defines a Jenkins pipeline for building and deploying a project. The pipeline consists of four stages, and there’s a post section to execute actions after all stages have completed. Let's break down the pipeline:

 1. Agent: Specifies that the pipeline will run on a Jenkins agent with the label ‘ubuntu’.

 2. Stages: Contains the sequential stages to be executed in the pipeline.

* Stage 1: Build and Deploy prometheus, grafana, and redis:

* This stage changes the working directory to /home/stefen/deploy/adminer.

* It prints the current working directory and its contents.

* Then, it runs the docker-compose up -d command to deploy Prometheus, Grafana, and Redis using Docker Compose.

* Stage 2: Build and Deploy API:

* This stage waits for 30 seconds before proceeding.

* It changes the working directory to /home/stefen/deploy/api.

* It prints the current working directory and its contents.

* Then, it runs the docker-compose up --build -d command to build and deploy the FastAPI application using Docker Compose.

* Stage 3: Fetch and Print getexchangedata:

* This stage makes an HTTP request to the FastAPI application’s /getexchangedata endpoint.

* It prints the response received from the API.

* Stage 4: Fetch and Print Exchangemetrics:

* This stage makes an HTTP request to the FastAPI application’s /exchangemetrics endpoint.

* It prints the response received from the API.

 1. Post: Specifies actions to be executed after all the stages have completed, regardless of their success or failure.

* In this case, it prints the URLs for Prometheus, Grafana, Redis, and the FastAPI application.

### Grafana Dashboard:

![](https://cdn-images-1.medium.com/max/3834/1*hqkhn_cI3UNKGa__tSkg5g.png)

## Conclusion:

In conclusion, the provided code snippets and configurations showcase an end-to-end deployment process of a monitoring and data visualization system using Jenkins, Docker, Prometheus, Grafana, and FastAPI. The pipeline defined in the Jenkinsfile automates the build and deployment process, ensuring a smooth and streamlined workflow for the project. This setup allows developers to efficiently monitor and visualize Bitcoin to USD exchange rate data, making it easier to identify trends and understand the data’s behavior over time. The use of FastAPI, Redis, and the provided API ensures a robust and efficient architecture for the system, while Docker and Jenkins enable seamless deployment and automation. Overall, this project demonstrates a practical application of modern technologies to create an effective and reliable monitoring and data visualization system.

[Medium Article]((https://medium.com/@stefentaime_10958/visualizing-bitcoin-to-usd-exchange-rates-using-fastapi-prometheus-grafana-deploy-on-jenkins-76c7e3aa30e1))
