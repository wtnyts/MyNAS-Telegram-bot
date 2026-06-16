from ..prometheus import get_prometheus_metric

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
