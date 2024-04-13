import requests
import time

PROMETHEUS_URL = 'http://prometheus-server.default.svc.cluster.local' 
DEPLOYMENT_NAME = 'your-deployment'
NAMESPACE = 'default'

def get_prometheus_query(query):
    response = requests.get(f"{PROMETHEUS_URL}/api/v1/query", params={'query': query})
    if response.status_code == 200:
        return response.json()['data']['result']
    else:
        raise Exception(f"Error querying Prometheus API: {response.content}")

def get_average_cpu_memory_usage():
    cpu_query = f'avg(rate(container_cpu_usage_seconds_total{{namespace="{NAMESPACE}", pod=~"{DEPLOYMENT_NAME}-.+"}}[5m]))'
    memory_query = f'avg(container_memory_usage_bytes{{namespace="{NAMESPACE}", pod=~"{DEPLOYMENT_NAME}-.+"}})'

    cpu_usage = get_prometheus_query(cpu_query)
    memory_usage = get_prometheus_query(memory_query)

    # Assuming single result and converting memory from bytes to MiB
    avg_cpu_usage = float(cpu_usage[0]['value'][1]) if cpu_usage else 0
    avg_memory_usage = float(memory_usage[0]['value'][1]) / 1024**2 if memory_usage else 0

    return avg_cpu_usage, avg_memory_usage
