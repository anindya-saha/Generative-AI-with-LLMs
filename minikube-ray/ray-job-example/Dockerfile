# Dockerfile

# Base image
FROM dockerhub.docker.zooxlabs.com/rayproject/ray:2.0.0

# Set the working directory
WORKDIR /home/ray/samples

# Copy the sample_code.py into the container
COPY sample_code.py /home/ray/samples/sample_code.py

# Install required Python packages
RUN pip install requests==2.26.0 pendulum==2.1.2

# Entry point to run the sample code
ENTRYPOINT ["python", "/home/ray/samples/sample_code.py"]