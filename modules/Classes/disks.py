from ..prometheus import get_prometheus_metric

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