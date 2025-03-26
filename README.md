# **Intrusion Detection System (IDS) with Prometheus and Grafana**

This project sets up an **Intrusion Detection System (IDS)** using **Docker, Prometheus, and Grafana**. The system collects network traffic data and visualizes it on a Grafana dashboard.

---

## **📌 Prerequisites**
Ensure you have the following installed:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## **🚀 Setup Instructions**

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/your-repo/ids-docker.git
cd ids-docker
```

### **2️⃣ Build and Start the Services**
```sh
sudo docker-compose up --build -d
```
- `--build`: Rebuilds images if necessary.
- `-d`: Runs the containers in detached mode.

### **3️⃣ Verify Running Containers**
```sh
sudo docker ps -a
```
You should see:
- Prometheus (port 9090)
- Grafana (port 3000)
- IDS Service (if included)

### **4️⃣ Access the Web Interfaces**
- Prometheus → [http://localhost:9090](http://localhost:9090)
- Grafana → [http://localhost:3000](http://localhost:3000)

### **5️⃣ Set Up Grafana Dashboard**
1. Log in to Grafana (default: `admin / admin` or your set credentials).
2. Navigate to **Configuration > Data Sources**.
3. Click **Add Data Source** → Select **Prometheus**.
4. Set the URL to: `http://prometheus:9090`.
5. Click **Save & Test**.
6. Import your dashboard:
    - Go to **Dashboards > Import**.
    - Upload your `.json` file.
    - Select **Prometheus** as the data source.

---

## **🐞 Troubleshooting Guide**

### **1️⃣ Error: "Post 'http://localhost:9090/api/v1/query': connect: connection refused"**
- **Cause**: Grafana cannot connect to Prometheus.
- **Fix**:
  1. Ensure Prometheus is running:
      ```sh
      sudo docker ps -a
      ```
  2. Try accessing Prometheus in your browser: [http://localhost:9090](http://localhost:9090).
  3. If not reachable, restart Prometheus:
      ```sh
      sudo docker-compose restart prometheus
      ```

### **2️⃣ Error: "prometheus: command not found" in logs**
- **Cause**: Prometheus may not be installed inside the container.
- **Fix**:
  1. Ensure `prometheus.yml` is correctly mapped in `docker-compose.yml`.
  2. Rebuild the container:
      ```sh
      sudo docker-compose down
      sudo docker-compose up --build -d
      ```

### **3️⃣ Error: "Unsupported config option for services.grafana: 'grafana'"**
- **Cause**: Incorrect `docker-compose.yml` formatting.
- **Fix**:
  Remove the extra `grafana:` line:
  ```yml
  grafana:
     image: grafana/grafana
  ```

### **4️⃣ Grafana Dashboard Not Loading**
- **Cause**: Grafana may not have permission to read the mounted dashboard files.
- **Fix**:
  1. Ensure correct volume mapping in `docker-compose.yml`:
      ```yml
      volumes:
         - ./grafana/dashboards:/var/lib/grafana/dashboards
      ```
  2. Restart Grafana:
      ```sh
      sudo docker-compose restart grafana
      ```

### **5️⃣ Docker Network Issues**
- **Cause**: Prometheus and Grafana are not communicating.
- **Fix**:
  1. Check the network:
      ```sh
      sudo docker network inspect monitoring
      ```
  2. If missing, create and connect:
      ```sh
      sudo docker network create monitoring
      sudo docker network connect monitoring prometheus
      sudo docker network connect monitoring grafana
      ```

---

## **🛑 Stopping the Services**
```sh
sudo docker-compose down
```

## **🔄 Restarting the Services**
```sh
sudo docker-compose restart
```

---

## **📌 Future Improvements**
- Automate IDS alerts in Grafana.
- Add support for additional attack detection models.
