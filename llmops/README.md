## Use an end-to-end model hosting solution to host code llama. 
+ Fast API for custom preprocessing and post processing
+ HF TGI (Text Generation Inference) server to host the model
+ Capture FAST API logs, HF TGI logs through Fluentd to ElasticSearch and visualize in Grafana
+ Capture Fast API metrics and TGI metrics in Prometheus + Grafana to visualize
+ Load test using Locust.

 Everything locally via Docker compose.

```bash
project-root/
│
├── docker-compose.yml
│
├── fastapi/
│   ├── Dockerfile
│   ├── app/
│   │   ├── main.py  # FastAPI application entry point
│   │   └── ...      # Other Python modules
│   └── requirements.txt
│
├── huggingface_tgi/
│   └── Dockerfile  # If custom setup is needed, otherwise use image directly in docker-compose.yml
│
├── fluentd/
│   ├── Dockerfile
│   └── conf/
│       └── fluent.conf  # Fluentd configuration
│
├── elasticsearch/
│   └── config/
│       └── elasticsearch.yml  # Elasticsearch configuration (if needed)
│
├── grafana/
│   ├── provisioning/
│   │   ├── dashboards/
│   │   │   └── dashboard.yml  # Dashboard configuration
│   │   └── datasources/
│   │       └── datasource.yml  # Datasource configuration
│   └── dashboards/
│       └── ...  # Dashboard JSON files
│
├── prometheus/
│   ├── prometheus.yml  # Prometheus configuration
│   └── rules/          # Alerting and recording rules
│
└── locust/
    ├── Dockerfile 
    ├── locustfile.py  # Locust test scripts
    └── requirements.txt
```
### Bring up all the components using CLI

```bash
docker compose up -d --build --remove-orphans --force-recreate

docker compose down --rmi local --remove-orphans -v

docker compose logs fluentd
```

### Test the Huggingface TGI Server from the command line

```bash
# Test text generation
curl localhost:8080/generate \
    -X POST \
    -d '{"inputs":"What is Deep Learning?","parameters":{"max_new_tokens":20}}' \
    -H 'Content-Type: application/json'
```

```bash
# Test TGI server metrics emitted
curl localhost:8080/metrics
```

### Test the Huggingface TGI Server from within the Fast API container

```bash
docker exec -it $(docker ps | grep 'fluentd' | awk '{print $1}') /bin/bash

docker exec -it $(docker ps | grep 'fastapi' | awk '{print $1}') /bin/bash
```

```bash
# Indie the Fast API container, test text generation from TGI server 
curl -X 'POST' \
  'http://tgi:80/generate' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"inputs":"What is Deep Learning?","parameters":{"max_new_tokens":256}}'
```

### Test the Fast API from the local mac/linux/windows terminal

Note: The port used is `8000` instead of `8080`. We use `8000` while calling `fastapi` but use `8080` when calling TGI. Also, the url is different, its `/generate-text` while usinf fastapi instead of `/generate` when using TGI.

```bash
curl -X 'POST' \
  'http://localhost:8000/generate-text' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"prompt": "What is Machine Learning?"}'
```
### Test Grafana from local terminal

Open up the Grafana dashboard at:
http://<machine_public_ip>:3000

username: admin  
password: admin  

Add a Prometheus data source. We have a default ./grafana/provisioning/datasources/datasource.yml for a local Prometheus instance.

[not Working]: Import the Huggingface TGI Server dashboard from https://grafana.com/grafana/dashboards/19831-text-generation-inference-dashboard/

Read this Tutorial for Prometheus + Grafana + Fast API
https://dev.to/ken_mwaura1/getting-started-monitoring-a-fastapi-app-with-grafana-and-prometheus-a-step-by-step-guide-3fbn



```bash
./launch.sh \
--model-id meta-llama/Llama-2-7b-chat-hf \
--num-shard 1 \
--max-concurrent-requests 4 \
--max-input-length 4000 \
--max-total-tokens 4096 \
--max-batch-prefill-tokens 4096


<label @FLUENT_LOG>
  <match *.**>
    @type copy
    <store>
      @type elasticsearch
      host elasticsearch
      port 9200
      logstash_format true
      logstash_prefix fluentd
      logstash_dateformat %Y%m%d
      include_tag_key true
      type_name access_log
      tag_key @log_name
      flush_interval 1s
    </store>
    <store>
      @type stdout
    </store>
  </match>
</label>
```
