Use an end-to-end model hosting solution to host code llama. Fast API for custom preprocessing and post processing + HF TGI (Text Generation Inference) server to host the model + Capture FAST API logs, HF TGI logs through Fluentd to ElasticSearch and visualize in Grafana, Capture Fast API metrics and TGI metrics in Prometheus + Grafana to visualize, Load test using Locust. - Everything locally via Docker compose.

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

```bash
./launch.sh \
--model-id meta-llama/Llama-2-7b-chat-hf \
--num-shard 1 \
--max-concurrent-requests 4 \
--max-input-length 4000 \
--max-total-tokens 4096 \
--max-batch-prefill-tokens 4096
```