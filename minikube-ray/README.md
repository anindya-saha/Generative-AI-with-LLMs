pip3 install --upgrade pip
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip3 install "torchmetrics>=0.9" "pytorch_lightning>=1.6" 
pip3 install -U "ray[default,data,train,tune,serve]"
pip3 install numpy scikit-learn scipy datasets "transformers>=4.19.1" "pytorch_lightning>=1.6.5" evaluate