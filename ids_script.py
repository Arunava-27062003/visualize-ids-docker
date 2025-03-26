from prometheus_client import start_http_server, Counter, Gauge
from scapy.all import sniff, IP, TCP, UDP
import time
from collections import defaultdict
import threading

# 🟢 Prometheus Metrics
packets_analyzed = Counter("ids_packets_analyzed", "Total packets analyzed")
alerts_total = Counter("ids_alerts_total", "Total IDS alerts", ['type'])

current_active_connections = Gauge('current_active_connections', 'Number of active connections')
total_detected_ddos_attacks = Counter('total_detected_ddos_attacks', 'Total detected DDoS attacks')
total_tcp_syn_flood_attacks = Counter('total_tcp_syn_flood_attacks', 'Total detected TCP SYN flood attacks')
total_udp_flood_attacks = Counter('total_udp_flood_attacks', 'Total detected UDP flood attacks')

unique_ips = Gauge("ids_unique_ips", "Number of unique source IPs")
total_bytes = Counter("ids_total_bytes", "Total bytes processed")

# 🔵 Track packet statistics
packet_counts = defaultdict(int)
port_scan_tracker = defaultdict(set)
ip_byte_count = defaultdict(int)
syn_counts = defaultdict(int)
udp_counts = defaultdict(int)

# 🛑 Detection Thresholds
DOS_THRESHOLD = 100   # Packets per second from a single IP
SCAN_THRESHOLD = 20   # Unique ports accessed
DDoS_IP_THRESHOLD = 5 # Multiple IPs sending excessive packets
SYN_FLOOD_THRESHOLD = 50 # High number of TCP SYN packets from one IP
UDP_FLOOD_THRESHOLD = 75 # High number of UDP packets from one IP

# 🔐 Thread Lock to prevent concurrency issues
metric_lock = threading.Lock()

def analyze_packet(packet):
    """Analyze network packets for malicious behavior."""
    if IP in packet:
        src_ip = packet[IP].src
        packets_analyzed.inc()

        with metric_lock:
            packet_counts[src_ip] += 1
            ip_byte_count[src_ip] += len(packet)
            total_bytes.inc(len(packet))

        if TCP in packet:
            dst_port = packet[TCP].dport
            port_scan_tracker[src_ip].add(dst_port)

            # ✅ SYN Flood Detection
            if packet[TCP].flags == 2:  # SYN flag set
                with metric_lock:
                    syn_counts[src_ip] += 1
                    if syn_counts[src_ip] > SYN_FLOOD_THRESHOLD:
                        total_tcp_syn_flood_attacks.inc()
                        alerts_total.labels(type="SYN_Flood").inc()
                        print(f"[ALERT] TCP SYN Flood detected from {src_ip}")

        elif UDP in packet:
            dst_port = packet[UDP].dport
            with metric_lock:
                udp_counts[src_ip] += 1
                if udp_counts[src_ip] > UDP_FLOOD_THRESHOLD:
                    total_udp_flood_attacks.inc()
                    alerts_total.labels(type="UDP_Flood").inc()
                    print(f"[ALERT] UDP Flood detected from {src_ip}")

        # ✅ Port Scan Detection
        if len(port_scan_tracker[src_ip]) > SCAN_THRESHOLD:
            with metric_lock:
                alerts_total.labels(type="PortScan").inc()
            print(f"[ALERT] Port Scan from {src_ip}")

def detect_attacks():
    """Monitor and detect various network attacks."""
    while True:
        with metric_lock:
            total_ips = len(packet_counts)
            unique_ips.set(total_ips)

            dos_ips = 0
            for ip, count in packet_counts.items():
                if count > DOS_THRESHOLD:
                    dos_ips += 1
                    alerts_total.labels(type="DoS").inc()
                    print(f"[ALERT] DoS Attack from {ip}")

            # ✅ DDoS Detection
            if dos_ips >= DDoS_IP_THRESHOLD:
                total_detected_ddos_attacks.inc()
                alerts_total.labels(type="DDoS").inc()
                print(f"[ALERT] DDoS Attack detected! {dos_ips} IPs involved.")

            # Reset counters every second
            packet_counts.clear()
            syn_counts.clear()
            udp_counts.clear()
            ip_byte_count.clear()

        time.sleep(1)

def update_metrics():
    """Simulate active connections and attack detections for Prometheus."""
    while True:
        with metric_lock:
            current_active_connections.set(10)  # Replace with actual active connections

        time.sleep(5)

# 🚀 Start IDS
if __name__ == "__main__":
    start_http_server(9200)  # Expose Prometheus metrics
    print("Custom IDS running, exposing metrics on port 9200...")

    # Start attack detection thread
    threading.Thread(target=detect_attacks, daemon=True).start()

    # Start metric update thread
    threading.Thread(target=update_metrics, daemon=True).start()

    # Start packet sniffing
    sniff(iface="enp2s0", prn=analyze_packet, store=False)
