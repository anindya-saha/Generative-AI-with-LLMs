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

### Test the Huggingface TGI Server from the command line
```
curl localhost:8080/generate \
    -X POST \
    -d '{"inputs":"What is Deep Learning?","parameters":{"max_new_tokens":20}}' \
    -H 'Content-Type: application/json'
```
### Test the Huggingface TGI Server from inside the Fast API container
```
docker ps | grep fastapi

docker exec -it <fastapi_container_id> /bin/bash

docker exec -it $(docker ps | grep 'fluentd' | awk '{print $1}') /bin/bash
docker exec -it $(docker ps | grep 'fastapi' | awk '{print $1}') /bin/bash
```

```
curl http://tgi:80/generate \
    -X POST \
    -d '{"inputs":"What is Deep Learning?","parameters":{"max_new_tokens":20}}' \
    -H 'Content-Type: application/json'
```

### Test the Fast API from local terminal
```
curl -X 'POST' \
  'http://localhost:8000/generate-text/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"prompt": "What is Machine Learning?"}'
```


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

```
# Start with the official Fluentd image
FROM fluent/fluentd:v1.12-debian-1

# Update and install dependencies for Ruby upgrade
USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        git \
        curl \
        build-essential \
        ruby-dev \
        make \
        nodejs \
        npm \
        autoconf \
        bison \
        libssl-dev \
        libyaml-dev \
        libreadline6-dev \
        zlib1g-dev \
        libncurses5-dev \
        libffi-dev \
        libgdbm6 \
        libgdbm-dev \
        libdb-dev \
     && rm -rf /var/lib/apt/lists/*

# Install rbenv and ruby-build
RUN git clone https://github.com/rbenv/rbenv.git ~/.rbenv \
    && git clone https://github.com/rbenv/ruby-build.git ~/.rbenv/plugins/ruby-build \
    && ~/.rbenv/bin/rbenv install 3.0.2 \
    && ~/.rbenv/bin/rbenv global 3.0.2

RUN gem uninstall yajl-ruby
RUN gem install yajl-ruby

# Update PATH
ENV PATH="/root/.rbenv/shims:/root/.rbenv/bin:${PATH}"

# Install fluent-plugin-elasticsearch
RUN gem install fluent-plugin-elasticsearch --no-document --version 5.3.0

USER fluent
```

```
docker compose up --build  --remove-orphans --force-recreate

docker compose down --rmi local --remove-orphans -v

```