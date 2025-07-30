import threading
import time

def worker(id):
    print(f"Thread {id} starting")
    time.sleep(1)
    print(f"Thread {id} finished")

# Create and start 5 threads
threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(i,))
    t.start()
    threads.append(t)

# Wait for all threads to finish
for t in threads:
    t.join()

print("All threads completed")