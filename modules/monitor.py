import time
import threading
from .prometheus import get_prometheus_metric

main_check = None
def check_metric(name, query, check_type, treshold = None)
    current = get_prometheus_metric(query)
    if check_type == "change":
        if current != None and current != main_check:
            
                    





















