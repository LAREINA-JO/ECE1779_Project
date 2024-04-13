from kubernetes import client, config
import time
import numpy as np

# 加载Kubernetes配置
config.load_kube_config() 
# config.load_incluster_config()

namespace = 'default'
deployment_name = 'your-deployment'
check_interval = 60 
decision_interval = 300  
cpu_usage_history = []
memory_usage_history = []

def get_current_usage():
    return np.random.random(), np.random.random() 

def scale_deployment(api, deployment_name, namespace, replicas):
    pass

def main():
    last_decision_time = time.time()
    
    while True:
        current_cpu_usage, current_memory_usage = get_current_usage()
        
        cpu_usage_history.append(current_cpu_usage)
        memory_usage_history.append(current_memory_usage)
        
        current_time = time.time()
        if current_time - last_decision_time > decision_interval:
            avg_cpu_usage = np.mean(cpu_usage_history)
            avg_memory_usage = np.mean(memory_usage_history)
            
            cpu_usage_history.clear()
            memory_usage_history.clear()
            
            if avg_cpu_usage > 0.75:
                scale_deployment(client.AppsV1Api(), deployment_name, namespace, 2) 
            
            last_decision_time = current_time
        
        time.sleep(check_interval)

if __name__ == "__main__":
    main()
