# Use a lightweight Python image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Add this before CMD in Dockerfile
RUN apt-get update && apt-get install -y prometheus

# Copy project files into the container
COPY ids_script.py .
COPY start.sh .
COPY prometheus.yml /etc/prometheus/prometheus.yml

# Install dependencies
RUN pip install prometheus_client scapy

# Give execute permission to start script
RUN chmod +x start.sh

# Expose ports for Prometheus & IDS metrics
EXPOSE 9200

# Start IDS & Prometheus
CMD ["./start.sh"]
