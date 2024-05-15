#!/usr/bin/env bash
function showhelp () {
    # Display Help
    echo
    echo "Usage: $0 [option...]"
    echo "options:"
    echo "  -h, --help                             Print this help."
    echo "  -d, --detach                           Start in detached mode."
    echo "  -b, --build                 Rebuild the docker container image."
    echo "  --model-id                   value     Set model name with model prefix."
    echo "  --num-gpus | --num-shard     value     Set number of gpus (shards) for the model."
    echo "  --max-concurrent-requests    value     Set max concurrent request."
    echo "  --max-input-length           value     Set max input length."
    echo "  --max-total-tokens           value     Set max total tokens."
    echo "  --max-batch-prefill-tokens   value     Set max batch prefill tokens."
    echo "  --quantize                   value     Set the quantization option, e.g., 'eetq', 'bitsandbytes'"
    echo "  --hf-token                   value     Set huggingface token."
    echo
}

options=""
NUM_SHARD=1
DOCKER_VOLUME_DIRECTORY=$HOME
MAX_CONCURRENT_REQUESTS=4
MAX_INPUT_LENGTH=4000
MAX_TOTAL_TOKENS=4096
MAX_BATCH_TOTAL_TOKENS=4096
QUANTIZE=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    echo "Processing argument: $1"
    case $1 in
        -h|--help)
            showhelp
            exit
            ;;
        -d|--detach)
            options+=" --detach"
            shift
            ;;
        -b|--build)
            options+=" --build"
            shift
            ;;
        --model-id)
            MODEL=$2
            shift 2
            ;;
        --num-gpus|--num-shard)
            NUM_SHARD=$2
            shift 2
            ;;
        --max-concurrent-requests)
            MAX_CONCURRENT_REQUESTS=$2
            shift 2
            ;;
        --max-input-length)
            MAX_INPUT_LENGTH=$2
            shift 2
            ;;
        --max-total-tokens)
            MAX_TOTAL_TOKENS=$2
            shift 2
            ;;
        --max-batch-prefill-tokens)
            MAX_BATCH_PREFILL_TOKENS=$2
            shift 2
            ;;
        --quantize)
            QUANTIZE=$2
            shift 2
            ;;
        --hf-token)
            HF_TOKEN=$2
            shift 2
            ;;
        *)
            echo "Error: Invalid argument $1"
            exit 1
            ;;
    esac
done

INFERENCE_COMMAND="--model-id ${MODEL} \
--num-shard ${NUM_SHARD} \
--max-concurrent-requests ${MAX_CONCURRENT_REQUESTS} \
--max-input-length ${MAX_INPUT_LENGTH} \
--max-total-tokens ${MAX_TOTAL_TOKENS} \
--max-stop-sequences 20 \
--trust-remote-code"

if [[ -n "${MAX_BATCH_PREFILL_TOKENS}" ]]; then
    INFERENCE_COMMAND+=" --max-batch-prefill-tokens ${MAX_BATCH_PREFILL_TOKENS}"
fi

# Append quantize option if it's set
if [[ -n "${QUANTIZE}" ]]; then
    INFERENCE_COMMAND+=" --quantize ${QUANTIZE}"
fi


# Append dtype option if it's set and quantize is not set
if [[ -n "${DTYPE}" && -z "${QUANTIZE}" ]]; then
    INFERENCE_COMMAND+=" --dtype ${DTYPE}"
fi


# Create env file if it does not exist
ENV_FILE=".env"

# if .env file exists, remove it
if [ -f ${ENV_FILE} ]; then
    rm ${ENV_FILE}
fi

echo "Creating ${ENV_FILE} file"
echo "INFERENCE_COMMAND=\"${INFERENCE_COMMAND}\"" >> ${ENV_FILE}
echo "VOLUME=${DOCKER_VOLUME_DIRECTORY}/llmops/data" >> ${ENV_FILE}
echo "PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:64" >> ".env"

source ${ENV_FILE}

docker compose up $options --remove-orphans --force-recreate
