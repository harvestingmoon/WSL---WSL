import ray
import time
import socket
import os
import platform # Import platform to get hostname reliably

# It's good practice to ensure Ray is initialized before running tasks.
# When running on the head node, "auto" will connect to the local cluster.

try:
    if ray.is_initialized():
        ray.shutdown() # Ensure a clean state if re-running in the same interpreter session


    ray.init(address="auto", ignore_reinit_error=True)
    print(f"Successfully connected to Ray cluster.")
    print(f"Cluster resources: {ray.cluster_resources()}")

 
    @ray.remote(num_cpus=1)
    def get_node_info_and_sleep(task_id):
        # Simulate some work and ensure the task takes a moment
        time.sleep(1) 

        # Get information about the node where this task is executing
        current_node_id = ray.get_runtime_context().get_node_id()
        current_hostname = socket.gethostname()
        current_pid = os.getpid()

        return {
            "task_id": task_id,
            "hostname": current_hostname,
            "pid": current_pid,
            "ray_node_id": str(current_node_id)
        }

    total_cpus = ray.cluster_resources().get("CPU", 0)
    num_tasks_to_launch = int(total_cpus * 2) if total_cpus > 0 else 16 # Launch 2x total CPUs, or default to 16

    print(f"\nLaunching {num_tasks_to_launch} remote tasks to distribute across nodes...")
    futures = [get_node_info_and_sleep.remote(i) for i in range(num_tasks_to_launch)]

    # Retrieve and print results
    print("\nRetrieving results:")
    for i, future in enumerate(futures):
        node_info = ray.get(future)
        print(f"Task {node_info['task_id']} executed on: Hostname={node_info['hostname']}, PID={node_info['pid']}, NodeID={node_info['ray_node_id']}")

    print("\nAll tasks completed.")

except Exception as e:
    print(f"\nAn error occurred: {e}")
    import traceback
    traceback.print_exc()
finally:
    # Always shut down Ray to release resources
    if ray.is_initialized():
        ray.shutdown()
        print("\nRay script finished and shut down connection.")