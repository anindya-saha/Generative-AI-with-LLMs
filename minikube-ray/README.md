python3.10 --version
sudo apt-get install python3.10-venv

python3.10 -m venv minikube-ray
source ~/minikube-ray/bin/activate

pip3 install --upgrade pip
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip3 install numpy scikit-learn scipy datasets "torchmetrics>=0.9" "transformers>=4.19.1" "pytorch_lightning>=1.6.5" evaluate
pip3 install -U "ray[default,data,train,tune,serve]==2.34.0"


ssh -L 8265:localhost:8265 -N user@remote-host