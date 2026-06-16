import time
import threading
from .prometheus import get_prometheus_metric

last = None

while True:
    current = get_prometheus_metric("cpu_status")
    if current != last and last != None:
        return f
        last = current
    time.sleep(5)