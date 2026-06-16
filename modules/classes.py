from .prometheus import get_prometheus_metric

class Disk:
    def __init__(self, name, mountpoint):
        self.name = name
        self.mountpoint = mountpoint

    def space(self):
        free = get_prometheus_metric(f'node_filesystem_avail_bytes{{mountpoint="{self.mountpoint}"}}')
        total = get_prometheus_metric(f'node_filesystem_size_bytes{{mountpoint="{self.mountpoint}"}}')
        used = total - free if free and total else None
        return free, total, used

    def format_size(self, byte_values):
        if byte_values is None:
            return "нет данных"
            
        units = ['B', "KB", "MB", "GB", "TB"]
        for i in units:
            if byte_values < 1024:
                return f"{byte_values:.1f} {i}"
            byte_values /= 1024

    def format(self):
        free, total, used = self.space()
        free = self.format_size(free)
        total = self.format_size(total)
        used = self.format_size(used)

        return(f"<b>{self.name}</b>: использовано <b>{used}</b>, свободно <b>{free}</b>, всего <b>{total}</b>\n")



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


class UPS:
    def __init__(self, name):
        self.name = name

    def ups_status(self):
        self.status = get_prometheus_metric("ups_status")
        if self.status == 2:
            return "батареи"
        elif self.status == 1:
            return "сети"
        else:
            return "НЕТ ДАННЫХ"
        
    def ups_time(self):
        self.ups_time = get_prometheus_metric("ups_battery_runtime_seconds")
        if self.ups_time is None:
            return "нет данных"

        if self.ups_time < 60:
            return f"{self.ups_time:.1f} сек."
        elif self.ups_time < 3600:
            return f"{self.ups_time/60:.1f} мин."
        elif self.ups_time < 86400:
            return f"{self.ups_time/3600:.1f} ч."
        else:
            return f"{self.ups_time/86400:.1f} д."

    def ups_charge(self):
        self.ups_charge = get_prometheus_metric("ups_battery_charge_percent")
        if self.ups_charge is None:
            return "нет данных"
        else:
            return f"{self.ups_charge}"
        
    def ups_load(self):
        self.ups_load = get_prometheus_metric("ups_load_percent")
        if self.ups_load is None:
            return "нет данных"
        else:
            return f"{self.ups_load}"
        
    def format(self):
        status = self.ups_status()
        time = self.ups_time()
        charge = self.ups_charge()
        load = self.ups_load()

        return f"Статус ИБП <b>{self.name}</b>:\n\nИБП работает от {status}\nВремя от батареи: <b>{time}</b>\nЗаряд ИБП: <b>{charge} %</b>\nНагрузка: <b>{load}</b> %"
