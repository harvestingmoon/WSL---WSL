import ray
import time
import socket

# Try to initialize Ray locally
try:
    if ray.is_initialized():
        ray.shutdown()
    ray.init()
    print("Ray initialized successfully on this node!")

    @ray.remote
    def get_hostname_task():
        time.sleep(1) # Simulate a bit of work
        return socket.gethostname()

    # Run the task locally
    hostname_ref = get_hostname_task.remote()
    hostname = ray.get(hostname_ref)
    print(f"Local task executed on hostname: {hostname}")
    print(f"Matches current WSL2 hostname: {socket.gethostname() == hostname}")

except Exception as e:
    print(f"An error occurred during local Ray sanity check: {e}")
finally:
    if ray.is_initialized():
        ray.shutdown()
        print("Ray shut down.")