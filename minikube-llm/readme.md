# Creating and Scalable LLM deployment with Kubernetes
In this tutorial we will demonstrate how to setup a scalable deployment architecture for LLM on Kubernetes. I will be using a 8 GPU A100 40 GB Gpu machine to
demonstrate.

## Setup a Minikube K8s cluster
Minikube is a single-node Kubernetes cluster that can be installed on macOS, Linux and Windows.

By default, it starts with 2 CPUs and 2GB of memory, that may not be enough for experiments with some heavy projects.

### Install Minikube
Follow the steps in https://minikube.sigs.k8s.io/docs/start/ and bring up a basic minikube cluster.

### Add Nvidia GPU support to minikube
Follow the steps in https://minikube.sigs.k8s.io/docs/tutorials/nvidia/ to add the NVidia GPU support.

### Provision the minikube cluster
```bash
# start with 32 cpus and 80gb of memory
minikube start --driver docker --container-runtime docker --gpus all --memory 81920 --cpus 32
```

## Install Kubectl
If you do not have `kubectl`, then minikube can download the appropriate version of kubectl.
```bash
minikube kubectl -- get pods -A
```

You can check the resources of the running Minikube instance, using the kubectl:
```bash
kubectl get node minikube -o jsonpath='{.status.capacity}'
```

### Test GPU support
Apply the tes yaml to verify GPU support.
```bash
kubectl create -f cuda-test-pod.yaml
```

Check the status of the pod.
```bash
kubectl describe pod cuda-vector-add or kubectl get pod cuda-vector-add -o yaml

$ kubectl get pod cuda-vector-add
NAME              READY   STATUS    RESTARTS   AGE
cuda-vector-add   1/1     Running   0          23s

kubectl logs -f cuda-vector-ad

You should see the following lines in the log
cp vectorAdd ../../bin/x86_64/linux/release
[Vector addition of 50000 elements]
Copy input data from the host memory to the CUDA device
CUDA kernel launch with 196 blocks of 256 threads
Copy output data from the CUDA device to the host memory
Test PASSED
Done
```

The status shoudl be `Running`. If it fails with cannot provision pos due to Gpu unavailibility then you might have to restart the m/c. IN GCP you need to just Reset the m/c.


### Stop the cluster
```bash
minikube stop
```

### Destroy the cluster
```bash
minikube delete
```
### 

## Instal Helm
Helm is the package manager for Kubernetes.

Follow steps from https://helm.sh/docs/intro/install/ to install Helm.

## Install HuggingFace Helm Chart
https://huggingface.co/blog/voatsap/tgi-kubernetes-cluster-dev

deploy nvidia ndcg via helmdeploy prometheus via helmdeploy tgi via helm - provide model name, company and storage class as `standard` for gcp

check prometheus, grafana
kubectl port forwardaccess from local using 
ssh -i ~/.ssh/google_compute_engine -L 8080:localhost:8080 anindya@34.87.179.148
make curl request to tgi
add service monitor for tgi minor - tgi by default expose metricverify prometheus targets
add dashboard to grafana - there are two dashboards
Ref:https://huggingface.co/blog/voatsap/tgi-kubernetes-cluster-dev
https://github.com/shalb/charts/blob/main/huggingface-model/values.yaml
https://github.com/huggingface/text-generation-inference/discussions/1127
https://github.com/prometheus-operator/prometheus-operator/blob/main/Documentation/user-guides/getting-started.md
https://github.com/shalb/cdev-examples/blob/main/aws/eks-model/bootstrap.ipynb