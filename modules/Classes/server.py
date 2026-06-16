from ..prometheus import get_prometheus_metric

class Server:
    def __init__(self, name):
        self.name = name
    
    def get_cpu_query(self):
        cpu_query = get_prometheus_metric('100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)')
        if cpu_query is not None:
            return f"{cpu_query:.1f}"
        else:
            return "нет данных"
    
    def get_cpu_temp(self):
        cpu_temp = get_prometheus_metric(
        'node_hwmon_temp_celsius{chip="platform_coretemp_0", sensor="temp1"}'
        )
        if cpu_temp is not None:
            return f"{cpu_temp:.1f}"
        else:
            return "нет данных"

    def get_ram(self):
        ram = get_prometheus_metric("(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100")
        if ram is not None:
            return f"{ram:.1f}"
        else:
            return "нет данных"
    
    def format(self):

        cpu_query = self.get_cpu_query()
        cpu_temp = self.get_cpu_temp()
        ram = self.get_ram()

        return f"Статус сервера <b>{self.name}</b>:\n\nНагрузка на CPU: <b>{cpu_query} %</b>\nТемпература CPU: <b>{cpu_temp}</b> °C\nЗагрузка RAM: <b>{ram}</b> %"