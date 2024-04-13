import yaml
from kubernetes import client, config
import requests
import time
import usage_collection

def load_config():
    with open("config.yaml", "r") as file:
        return yaml.safe_load(file)

config.load_kube_config()
apps_v1_api = client.AppsV1Api()   

cfg = load_config()

def autoscale():
    avg_cpu_usage, avg_memory_usage = usage_collection.get_average_cpu_memory_usage()
    deployment = apps_v1_api.read_namespaced_deployment(cfg['autoscale']['deployment_name'], cfg['autoscale']['namespace'])
    
    current_replicas = deployment.spec.replicas
    target_replicas = current_replicas

    if avg_cpu_usage > cfg['autoscale']['cpu_threshold']:
        target_replicas = int(current_replicas * cfg['autoscale']['scale_up_multiplier'])
    elif avg_cpu_usage < cfg['autoscale']['cpu_threshold'] * cfg['autoscale']['scale_down_multiplier']:
        target_replicas = int(current_replicas * cfg['autoscale']['scale_down_multiplier'])

    if target_replicas != current_replicas:
        print(f"Scaling deployment from {current_replicas} to {target_replicas} replicas.")
        deployment.spec.replicas = target_replicas
        apps_v1_api.replace_namespaced_deployment(cfg['autoscale']['deployment_name'], cfg['autoscale']['namespace'], deployment)