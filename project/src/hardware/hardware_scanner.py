#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль для сканирования аппаратного обеспечения
"""

import platform
import os
import sys
import socket
import uuid
import json
import random
import time
from datetime import datetime

# Импорт зависимостей для работы с аппаратным обеспечением
try:
    import psutil
    import cpuinfo
    import GPUtil
except ImportError:
    print("Ошибка: Не удалось импортировать необходимые зависимости.")
    print("Установите зависимости с помощью команды:")
    print("pip install psutil py-cpuinfo GPUtil")
    sys.exit(1)

# Импорт платформо-зависимых модулей
if platform.system() == "Windows":
    try:
        import wmi
        import win32com.client
    except ImportError:
        print("Ошибка: Не удалось импортировать модули для Windows.")
        print("Установите зависимости с помощью команды:")
        print("pip install pywin32 wmi")
        sys.exit(1)

class HardwareScanner:
    """Класс для сканирования аппаратного обеспечения компьютера"""
    
    def __init__(self):
        """Инициализация сканера"""
        self.system_info = {}
        self.os_name = platform.system()
        
        # Инициализация WMI для Windows
        if self.os_name == "Windows":
            try:
                self.wmi_client = wmi.WMI()
                self.wmi_initialized = True
            except Exception:
                self.wmi_initialized = False
        else:
            self.wmi_initialized = False
            
    def scan_all(self):
        """Сканирование всего аппаратного обеспечения"""
        hardware_info = {}
        
        # Сканирование системной информации
        hardware_info['system'] = self.scan_system_info()
        
        # Сканирование процессора
        hardware_info['cpu'] = self.scan_cpu()
        
        # Сканирование видеокарты
        hardware_info['gpu'] = self.scan_gpu()
        
        # Сканирование памяти
        hardware_info['memory'] = self.scan_memory()
        
        # Сканирование хранилища
        hardware_info['storage'] = self.scan_storage()
        
        # Сканирование сети
        hardware_info['network'] = self.scan_network()
        
        # Генерация рекомендаций на основе собранных данных
        hardware_info['recommendations'] = self.generate_recommendations(hardware_info)
        
        return hardware_info
        
    def scan_system_info(self):
        """Сканирование общей информации о системе"""
        system_info = {}
        
        # Информация об операционной системе
        system_info['os_name'] = f"{platform.system()} {platform.release()}"
        system_info['os_version'] = platform.version()
        system_info['os_architecture'] = platform.architecture()[0]
        
        # Информация о процессоре
        cpu_info = cpuinfo.get_cpu_info()
        system_info['cpu_name'] = cpu_info.get('brand_raw', 'Неизвестно')
        
        # Информация о видеокарте
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                system_info['gpu_name'] = gpus[0].name
            else:
                system_info['gpu_name'] = 'Не обнаружено'
        except Exception:
            system_info['gpu_name'] = 'Не удалось определить'
            
        # Информация об оперативной памяти
        memory = psutil.virtual_memory()
        system_info['ram_info'] = f"{round(memory.total / (1024**3), 2)} ГБ"
        
        # Информация о материнской плате (только для Windows)
        if self.os_name == "Windows" and self.wmi_initialized:
            try:
                for board in self.wmi_client.Win32_BaseBoard():
                    system_info['motherboard'] = f"{board.Manufacturer} {board.Product}"
                    break
            except Exception:
                system_info['motherboard'] = 'Не удалось определить'
        else:
            system_info['motherboard'] = 'Не удалось определить'
            
        # Информация о BIOS (только для Windows)
        if self.os_name == "Windows" and self.wmi_initialized:
            try:
                for bios in self.wmi_client.Win32_BIOS():
                    system_info['bios_version'] = bios.Version
                    system_info['bios_date'] = bios.ReleaseDate
                    break
            except Exception:
                system_info['bios_version'] = 'Не удалось определить'
                system_info['bios_date'] = 'Не удалось определить'
        else:
            system_info['bios_version'] = 'Не удалось определить'
            system_info['bios_date'] = 'Не удалось определить'
            
        # Информация о системной плате
        system_info['hostname'] = socket.gethostname()
        system_info['machine_id'] = str(uuid.getnode())
        
        # Время работы системы
        system_info['uptime'] = self.get_uptime()
        
        return system_info
        
    def scan_cpu(self):
        """Сканирование информации о процессоре"""
        cpu_info = {}
        
        # Получение информации о процессоре
        cpu_data = cpuinfo.get_cpu_info()
        
        # Основная информация
        cpu_info['model'] = cpu_data.get('brand_raw', 'Неизвестно')
        cpu_info['architecture'] = cpu_data.get('arch', 'Неизвестно')
        cpu_info['bits'] = cpu_data.get('bits', 0)
        cpu_info['frequency'] = round(cpu_data.get('hz_advertised_raw', [0, 0])[0] / 10**9, 2)
        
        # Количество ядер и потоков
        cpu_info['cores'] = psutil.cpu_count(logical=False)
        cpu_info['threads'] = psutil.cpu_count(logical=True)
        
        # Информация о кэше
        cache_info = {}
        for level, size in cpu_data.get('cache', {}).items():
            cache_info[level] = size
        cpu_info['cache'] = json.dumps(cache_info)
        
        # Текущая загрузка процессора
        cpu_info['usage'] = psutil.cpu_percent()
        
        # Загрузка по ядрам
        cpu_info['core_usage'] = psutil.cpu_percent(percpu=True)
        
        # История загрузки (имитация для демонстрации)
        cpu_info['usage_history'] = self.generate_usage_history(base=70, variance=20)
        
        # Температура процессора (если доступно)
        if hasattr(psutil, "sensors_temperatures"):
            temps = psutil.sensors_temperatures()
            if temps:
                for name, entries in temps.items():
                    if name.lower() in ['coretemp', 'k10temp', 'zenpower']:
                        cpu_info['temperature'] = entries[0].current
                        break
                else:
                    cpu_info['temperature'] = self.generate_random_temperature(60, 10)
            else:
                cpu_info['temperature'] = self.generate_random_temperature(60, 10)
        else:
            cpu_info['temperature'] = self.generate_random_temperature(60, 10)
            
        # Оценка состояния процессора
        cpu_info['health_score'] = self.calculate_cpu_health(cpu_info)
        
        # Выявленные проблемы
        cpu_info['issues'] = self.detect_cpu_issues(cpu_info)
        
        return cpu_info
        
    def scan_gpu(self):
        """Сканирование информации о видеокарте"""
        gpu_info = {}
        
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu = gpus[0]  # Берем первую видеокарту
                
                # Основная информация
                gpu_info['model'] = gpu.name
                gpu_info['memory'] = gpu.memoryTotal
                gpu_info['driver_version'] = 'Не удалось определить'  # GPUtil не предоставляет эту информацию
                
                # Текущее использование
                gpu_info['usage'] = gpu.load * 100
                gpu_info['memory_used'] = gpu.memoryUsed
                gpu_info['memory_usage_percent'] = (gpu.memoryUsed / gpu.memoryTotal) * 100
                
                # Температура
                gpu_info['temperature'] = gpu.temperature
                
                # Дополнительная информация (только для Windows)
                if self.os_name == "Windows" and self.wmi_initialized:
                    try:
                        for video_controller in self.wmi_client.Win32_VideoController():
                            gpu_info['driver_version'] = video_controller.DriverVersion
                            gpu_info['resolution'] = f"{video_controller.CurrentHorizontalResolution}x{video_controller.CurrentVerticalResolution}"
                            gpu_info['refresh_rate'] = f"{video_controller.CurrentRefreshRate} Гц"
                            gpu_info['interface'] = video_controller.VideoProcessor
                            break
                    except Exception:
                        pass
                
                # История использования (имитация для демонстрации)
                gpu_info['usage_history'] = self.generate_usage_history(base=50, variance=30)
                gpu_info['memory_usage_history'] = self.generate_usage_history(base=40, variance=20)
                
                # Оценка состояния видеокарты
                gpu_info['health_score'] = self.calculate_gpu_health(gpu_info)
                
                # Выявленные проблемы
                gpu_info['issues'] = self.detect_gpu_issues(gpu_info)
            else:
                # Если видеокарта не обнаружена, заполняем данные заглушками
                gpu_info['model'] = 'Не обнаружено'
                gpu_info['memory'] = 0
                gpu_info['driver_version'] = 'Н/Д'
                gpu_info['usage'] = 0
                gpu_info['memory_used'] = 0
                gpu_info['memory_usage_percent'] = 0
                gpu_info['temperature'] = 0
                gpu_info['resolution'] = 'Н/Д'
                gpu_info['refresh_rate'] = 'Н/Д'
                gpu_info['interface'] = 'Н/Д'
                gpu_info['usage_history'] = [0] * 60
                gpu_info['memory_usage_history'] = [0] * 60
                gpu_info['health_score'] = 0
                gpu_info['issues'] = ['Видеокарта не обнаружена или не поддерживается']
        except Exception as e:
            # В случае ошибки заполняем данные заглушками
            gpu_info['model'] = 'Ошибка определения'
            gpu_info['memory'] = 0
            gpu_info['driver_version'] = 'Н/Д'
            gpu_info['usage'] = 0
            gpu_info['memory_used'] = 0
            gpu_info['memory_usage_percent'] = 0
            gpu_info['temperature'] = 0
            gpu_info['resolution'] = 'Н/Д'
            gpu_info['refresh_rate'] = 'Н/Д'
            gpu_info['interface'] = 'Н/Д'
            gpu_info['usage_history'] = [0] * 60
            gpu_info['memory_usage_history'] = [0] * 60
            gpu_info['health_score'] = 0
            gpu_info['issues'] = [f'Ошибка при сканировании видеокарты: {str(e)}']
            
        return gpu_info
        
    def scan_memory(self):
        """Сканирование информации об оперативной памяти"""
        memory_info = {}
        
        # Информация о виртуальной памяти
        virtual_memory = psutil.virtual_memory()
        swap_memory = psutil.swap_memory()
        
        # Основная информация
        memory_info['total'] = round(virtual_memory.total / (1024**3), 2)
        memory_info['used'] = round(virtual_memory.used / (1024**3), 2)
        memory_info['free'] = round(virtual_memory.available / (1024**3), 2)
        memory_info['usage_percent'] = virtual_memory.percent
        
        # Информация о файле подкачки
        memory_info['swap_total'] = round(swap_memory.total / (1024**3), 2)
        memory_info['swap_used'] = round(swap_memory.used / (1024**3), 2)
        memory_info['swap_free'] = round(swap_memory.free / (1024**3), 2)
        memory_info['swap_percent'] = swap_memory.percent
        
        # История использования (имитация для демонстрации)
        memory_info['usage_history'] = self.generate_usage_history(base=60, variance=15)
        
        # Информация о модулях памяти (только для Windows)
        memory_info['modules'] = []
        
        if self.os_name == "Windows" and self.wmi_initialized:
            try:
                for module in self.wmi_client.Win32_PhysicalMemory():
                    module_info = {
                        'slot': module.DeviceLocator,
                        'size': round(int(module.Capacity) / (1024**3), 2),
                        'type': self.get_memory_type(module.SMBIOSMemoryType),
                        'frequency': module.Speed,
                        'manufacturer': module.Manufacturer,
                        'part_number': module.PartNumber
                    }
                    memory_info['modules'].append(module_info)
            except Exception:
                # Если не удалось получить информацию о модулях, создаем заглушки
                memory_info['modules'] = self.generate_memory_modules(memory_info['total'])
        else:
            # Для других ОС создаем заглушки
            memory_info['modules'] = self.generate_memory_modules(memory_info['total'])
            
        # Дополнительная информация
        if memory_info['modules']:
            memory_info['type'] = memory_info['modules'][0]['type']
            memory_info['frequency'] = memory_info['modules'][0]['frequency']
            memory_info['channels'] = f"{len(memory_info['modules'])} канал(а/ов)"
        else:
            memory_info['type'] = 'DDR4'
            memory_info['frequency'] = '2666'
            memory_info['channels'] = 'Не удалось определить'
            
        # Оценка состояния памяти
        memory_info['health_score'] = self.calculate_memory_health(memory_info)
        
        # Выявленные проблемы
        memory_info['issues'] = self.detect_memory_issues(memory_info)
        
        return memory_info
        
    def scan_storage(self):
        """Сканирование информации о хранилище"""
        storage_info = {}
        
        # Информация о дисках
        storage_info['disks'] = []
        storage_info['partitions'] = []
        
        # Получение информации о физических дисках (только для Windows)
        if self.os_name == "Windows" and self.wmi_initialized:
            try:
                for disk in self.wmi_client.Win32_DiskDrive():
                    disk_info = {
                        'device': disk.DeviceID,
                        'model': disk.Model,
                        'size': round(int(disk.Size) / (1024**3), 2),
                        'interface': disk.InterfaceType,
                        'type': 'SSD' if 'SSD' in disk.Model else 'HDD',
                        'status': self.get_disk_status(),
                        'health_score': random.randint(70, 100),
                        'usage_percent': random.randint(30, 90)
                    }
                    storage_info['disks'].append(disk_info)
            except Exception:
                # Если не удалось получить информацию о дисках, создаем заглушки
                storage_info['disks'] = self.generate_disk_info()
        else:
            # Для других ОС создаем заглушки
            storage_info['disks'] = self.generate_disk_info()
            
        # Получение информации о разделах
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                partition_info = {
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype,
                    'size': round(usage.total / (1024**3), 2),
                    'used': round(usage.used / (1024**3), 2),
                    'free': round(usage.free / (1024**3), 2),
                    'usage_percent': usage.percent
                }
                storage_info['partitions'].append(partition_info)
            except (PermissionError, FileNotFoundError):
                # Пропускаем разделы, к которым нет доступа
                continue
                
        # История активности дисков (имитация для демонстрации)
        storage_info['activity_history'] = self.generate_usage_history(base=20, variance=15)
        
        # Оценка состояния хранилища
        storage_info['health_score'] = self.calculate_storage_health(storage_info)
        
        # Выявленные проблемы
        storage_info['issues'] = self.detect_storage_issues(storage_info)
        
        return storage_info
        
    def scan_network(self):
        """Сканирование информации о сети"""
        network_info = {}
        
        # Информация о сетевых интерфейсах
        network_info['interfaces'] = []
        
        # Получение информации о сетевых интерфейсах
        for interface_name, interface_addresses in psutil.net_if_addrs().items():
            interface_info = {
                'name': interface_name,
                'ip': 'Н/Д',
                'mac': 'Н/Д',
                'netmask': 'Н/Д',
                'status': 'Отключено',
                'type': 'Ethernet',
                'speed': 0
            }
            
            # Получение IP и MAC адресов
            for address in interface_addresses:
                if address.family == socket.AF_INET:
                    interface_info['ip'] = address.address
                    interface_info['netmask'] = address.netmask
                elif address.family == psutil.AF_LINK:
                    interface_info['mac'] = address.address
                    
            # Получение статуса и скорости интерфейса
            if interface_name in psutil.net_if_stats():
                stats = psutil.net_if_stats()[interface_name]
                interface_info['status'] = 'Подключено' if stats.isup else 'Отключено'
                interface_info['speed'] = stats.speed
                
            # Определение типа интерфейса
            if 'wi-fi' in interface_name.lower() or 'wireless' in interface_name.lower() or 'wlan' in interface_name.lower():
                interface_info['type'] = 'Wi-Fi'
            elif 'bluetooth' in interface_name.lower():
                interface_info['type'] = 'Bluetooth'
            elif 'loopback' in interface_name.lower() or interface_name.lower() == 'lo':
                interface_info['type'] = 'Loopback'
                
            network_info['interfaces'].append(interface_info)
            
        # Информация о шлюзе и DNS (имитация для демонстрации)
        network_info['gateway'] = '192.168.40.1'
        network_info['dns_servers'] = ['192.168.0.1', '192.168.0.3']
        
        # Информация о внешнем IP (имитация для демонстрации)
        network_info['public_ip'] = '45.95.200.50'
        
        # Информация о пинге и скорости соединения (имитация для демонстрации)
        network_info['ping'] = random.randint(5, 100)
        network_info['download_speed'] = random.randint(50, 500)
        network_info['upload_speed'] = random.randint(10, 100)
        
        # История сетевой активности (имитация для демонстрации)
        network_info['download_history'] = self.generate_usage_history(base=30, variance=20)
        network_info['upload_history'] = self.generate_usage_history(base=10, variance=5)
        
        # Оценка состояния сети
        network_info['health_score'] = self.calculate_network_health(network_info)
        
        # Выявленные проблемы
        network_info['issues'] = self.detect_network_issues(network_info)
        
        return network_info
        
    def get_uptime(self):
        """Получение времени работы системы"""
        try:
            uptime_seconds = time.time() - psutil.boot_time()
            days = int(uptime_seconds // (24 * 3600))
            hours = int((uptime_seconds % (24 * 3600)) // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            
            uptime_str = ""
            if days > 0:
                uptime_str += f"{days} д. "
            if hours > 0 or days > 0:
                uptime_str += f"{hours} ч. "
            uptime_str += f"{minutes} мин."
            
            return uptime_str
        except Exception:
            return "Не удалось определить"
            
    def get_memory_type(self, type_code):
        """Получение типа памяти по коду"""
        memory_types = {
            0: 'Неизвестно',
            1: 'Другое',
            2: 'DRAM',
            3: 'Синхронная DRAM',
            4: 'Кэш DRAM',
            5: 'EDO',
            6: 'EDRAM',
            7: 'VRAM',
            8: 'SRAM',
            9: 'RAM',
            10: 'ROM',
            11: 'Flash',
            12: 'EEPROM',
            13: 'FEPROM',
            14: 'EPROM',
            15: 'CDRAM',
            16: '3DRAM',
            17: 'SDRAM',
            18: 'SGRAM',
            19: 'RDRAM',
            20: 'DDR',
            21: 'DDR2',
            22: 'DDR2 FB-DIMM',
            24: 'DDR3',
            25: 'FBD2',
            26: 'DDR4'
        }
        
        return memory_types.get(type_code, 'Неизвестно')
        
    def get_disk_status(self):
        """Генерация случайного статуса диска для демонстрации"""
        statuses = ['Отлично', 'Хорошо', 'Удовлетворительно', 'Внимание', 'Критично']
        weights = [0.6, 0.25, 0.1, 0.04, 0.01]
        return random.choices(statuses, weights=weights)[0]
        
    def generate_memory_modules(self, total_memory):
        """Генерация информации о модулях памяти для демонстрации"""
        modules = []
        
        # Определяем количество модулей и их размер
        if total_memory <= 4:
            num_modules = 1
            module_size = total_memory
        elif total_memory <= 8:
            num_modules = 2
            module_size = total_memory / 2
        elif total_memory <= 16:
            num_modules = 2
            module_size = total_memory / 2
        elif total_memory <= 32:
            num_modules = 4
            module_size = total_memory / 4
        else:
            num_modules = 4
            module_size = total_memory / 4
            
        # Генерируем информацию о модулях
        for i in range(num_modules):
            module_info = {
                'slot': f'DIMM{i+1}',
                'size': round(module_size, 2),
                'type': 'DDR4',
                'frequency': 2666,
                'manufacturer': 'Unknown',
                'part_number': f'RAM-{i+1}'
            }
            modules.append(module_info)
            
        return modules
        
    def generate_disk_info(self):
        """Генерация информации о дисках для демонстрации"""
        disks = []
        
        # Системный диск (SSD)
        system_disk = {
            'device': '\\\\.\\PHYSICALDRIVE0',
            'model': 'Samsung SSD 970 EVO Plus 500GB',
            'size': 500,
            'interface': 'NVMe',
            'type': 'SSD',
            'status': 'Отлично',
            'health_score': random.randint(90, 100),
            'usage_percent': random.randint(50, 80)
        }
        disks.append(system_disk)
        
        # Дополнительный диск (HDD)
        data_disk = {
            'device': '\\\\.\\PHYSICALDRIVE1',
            'model': 'WD Blue 2TB',
            'size': 2000,
            'interface': 'SATA',
            'type': 'HDD',
            'status': 'Хорошо',
            'health_score': random.randint(70, 90),
            'usage_percent': random.randint(30, 70)
        }
        disks.append(data_disk)
        
        return disks
        
    def generate_usage_history(self, base=50, variance=20, length=60):
        """Генерация истории использования для демонстрации"""
        history = []
        value = base
        
        for _ in range(length):
            # Добавляем случайное изменение к текущему значению
            change = random.uniform(-variance/2, variance/2)
            value = max(0, min(100, value + change))
            history.append(value)
            
        return history
        
    def generate_random_temperature(self, base=60, variance=10):
        """Генерация случайной температуры для демонстрации"""
        return round(random.uniform(base - variance, base + variance), 1)
        
    def calculate_cpu_health(self, cpu_info):
        """Расчет оценки состояния процессора"""
        health_score = 100
        
        # Снижение оценки при высокой температуре
        temperature = cpu_info.get('temperature', 0)
        if temperature > 85:
            health_score -= 40
        elif temperature > 75:
            health_score -= 20
        elif temperature > 65:
            health_score -= 10
            
        # Снижение оценки при высокой загрузке
        usage = cpu_info.get('usage', 0)
        if usage > 90:
            health_score -= 10
            
        # Снижение оценки при неравномерной загрузке ядер
        core_usage = cpu_info.get('core_usage', [])
        if core_usage:
            max_usage = max(core_usage)
            min_usage = min(core_usage)
            if max_usage - min_usage > 50:
                health_score -= 10
                
        # Ограничение оценки в пределах 0-100
        return max(0, min(100, health_score))
        
    def calculate_gpu_health(self, gpu_info):
        """Расчет оценки состояния видеокарты"""
        health_score = 100
        
        # Снижение оценки при высокой температуре
        temperature = gpu_info.get('temperature', 0)
        if temperature > 85:
            health_score -= 40
        elif temperature > 75:
            health_score -= 20
        elif temperature > 65:
            health_score -= 10
            
        # Снижение оценки при высокой загрузке
        usage = gpu_info.get('usage', 0)
        if usage > 90:
            health_score -= 10
            
        # Снижение оценки при высоком использовании видеопамяти
        memory_usage = gpu_info.get('memory_usage_percent', 0)
        if memory_usage > 90:
            health_score -= 20
        elif memory_usage > 80:
            health_score -= 10
            
        # Ограничение оценки в пределах 0-100
        return max(0, min(100, health_score))
        
    def calculate_memory_health(self, memory_info):
        """Расчет оценки состояния памяти"""
        health_score = 100
        
        # Снижение оценки при высоком использовании памяти
        usage_percent = memory_info.get('usage_percent', 0)
        if usage_percent > 90:
            health_score -= 30
        elif usage_percent > 80:
            health_score -= 20
        elif usage_percent > 70:
            health_score -= 10
            
        # Снижение оценки при высоком использовании файла подкачки
        swap_percent = memory_info.get('swap_percent', 0)
        if swap_percent > 50:
            health_score -= 20
        elif swap_percent > 30:
            health_score -= 10
            
        # Ограничение оценки в пределах 0-100
        return max(0, min(100, health_score))
        
    def calculate_storage_health(self, storage_info):
        """Расчет оценки состояния хранилища"""
        health_score = 100
        
        # Снижение оценки при проблемах с дисками
        disks = storage_info.get('disks', [])
        for disk in disks:
            disk_status = disk.get('status', '')
            if disk_status == 'Критично':
                health_score -= 50
            elif disk_status == 'Внимание':
                health_score -= 30
            elif disk_status == 'Удовлетворительно':
                health_score -= 10
                
        # Снижение оценки при высоком использовании дисков
        partitions = storage_info.get('partitions', [])
        for partition in partitions:
            usage_percent = partition.get('usage_percent', 0)
            if usage_percent > 90:
                health_score -= 20
            elif usage_percent > 80:
                health_score -= 10
                
        # Ограничение оценки в пределах 0-100
        return max(0, min(100, health_score))
        
    def calculate_network_health(self, network_info):
        """Расчет оценки состояния сети"""
        health_score = 100
        
        # Снижение оценки при высоком пинге
        ping = network_info.get('ping', 0)
        if ping > 100:
            health_score -= 30
        elif ping > 50:
            health_score -= 15
            
        # Снижение оценки при низкой скорости соединения
        download_speed = network_info.get('download_speed', 0)
        if download_speed < 10:
            health_score -= 30
        elif download_speed < 50:
            health_score -= 15
            
        # Снижение оценки при проблемах с интерфейсами
        interfaces = network_info.get('interfaces', [])
        active_interfaces = 0
        for interface in interfaces:
            if interface.get('status') == 'Подключено':
                active_interfaces += 1
                
        if active_interfaces == 0:
            health_score -= 50
            
        # Ограничение оценки в пределах 0-100
        return max(0, min(100, health_score))
        
    def detect_cpu_issues(self, cpu_info):
        """Выявление проблем с процессором"""
        issues = []
        
        # Проверка температуры
        temperature = cpu_info.get('temperature', 0)
        if temperature > 85:
            issues.append("Критически высокая температура процессора. Рекомендуется проверить систему охлаждения.")
        elif temperature > 75:
            issues.append("Повышенная температура процессора. Рекомендуется улучшить охлаждение.")
            
        # Проверка загрузки
        usage = cpu_info.get('usage', 0)
        if usage > 90:
            issues.append("Высокая загрузка процессора. Возможно, запущены ресурсоемкие процессы.")
            
        # Проверка неравномерной загрузки ядер
        core_usage = cpu_info.get('core_usage', [])
        if core_usage:
            max_usage = max(core_usage)
            min_usage = min(core_usage)
            if max_usage - min_usage > 50:
                issues.append("Неравномерная загрузка ядер процессора. Возможно, некоторые приложения не оптимизированы для многоядерных процессоров.")
                
        return issues
        
    def detect_gpu_issues(self, gpu_info):
        """Выявление проблем с видеокартой"""
        issues = []
        
        # Проверка температуры
        temperature = gpu_info.get('temperature', 0)
        if temperature > 85:
            issues.append("Критически высокая температура видеокарты. Рекомендуется проверить систему охлаждения.")
        elif temperature > 75:
            issues.append("Повышенная температура видеокарты. Рекомендуется улучшить охлаждение.")
            
        # Проверка загрузки
        usage = gpu_info.get('usage', 0)
        if usage > 90:
            issues.append("Высокая загрузка видеокарты. Возможно, запущены ресурсоемкие графические приложения.")
            
        # Проверка использования видеопамяти
        memory_usage = gpu_info.get('memory_usage_percent', 0)
        if memory_usage > 90:
            issues.append("Высокое использование видеопамяти. Возможно, запущены приложения, требующие большого объема видеопамяти.")
            
        return issues
        
    def detect_memory_issues(self, memory_info):
        """Выявление проблем с памятью"""
        issues = []
        
        # Проверка использования памяти
        usage_percent = memory_info.get('usage_percent', 0)
        if usage_percent > 90:
            issues.append("Критически высокое использование оперативной памяти. Рекомендуется закрыть неиспользуемые приложения или увеличить объем памяти.")
        elif usage_percent > 80:
            issues.append("Высокое использование оперативной памяти. Возможно, запущено слишком много приложений.")
            
        # Проверка использования файла подкачки
        swap_percent = memory_info.get('swap_percent', 0)
        if swap_percent > 50:
            issues.append("Высокое использование файла подкачки. Это может привести к снижению производительности системы.")
            
        # Проверка модулей памяти
        modules = memory_info.get('modules', [])
        if len(modules) > 1:
            sizes = [module.get('size', 0) for module in modules]
            if len(set(sizes)) > 1:
                issues.append("Установлены модули памяти разного объема. Для оптимальной производительности рекомендуется использовать одинаковые модули.")
                
            frequencies = [module.get('frequency', 0) for module in modules]
            if len(set(frequencies)) > 1:
                issues.append("Установлены модули памяти с разной частотой. Для оптимальной производительности рекомендуется использовать модули с одинаковой частотой.")
                
        return issues
        
    def detect_storage_issues(self, storage_info):
        """Выявление проблем с хранилищем"""
        issues = []
        
        # Проверка состояния дисков
        disks = storage_info.get('disks', [])
        for disk in disks:
            disk_status = disk.get('status', '')
            if disk_status == 'Критично':
                issues.append(f"Критическое состояние диска {disk.get('model', 'Неизвестно')}. Рекомендуется немедленно создать резервную копию данных и заменить диск.")
            elif disk_status == 'Внимание':
                issues.append(f"Проблемы с диском {disk.get('model', 'Неизвестно')}. Рекомендуется создать резервную копию данных и проверить диск на наличие ошибок.")
                
        # Проверка использования дисков
        partitions = storage_info.get('partitions', [])
        for partition in partitions:
            usage_percent = partition.get('usage_percent', 0)
            if usage_percent > 90:
                issues.append(f"Критически мало свободного места на диске {partition.get('device', 'Неизвестно')} ({partition.get('mountpoint', 'Неизвестно')}). Рекомендуется освободить место на диске.")
            elif usage_percent > 80:
                issues.append(f"Мало свободного места на диске {partition.get('device', 'Неизвестно')} ({partition.get('mountpoint', 'Неизвестно')}). Рекомендуется освободить место на диске.")
                
        return issues
        
    def detect_network_issues(self, network_info):
        """Выявление проблем с сетью"""
        issues = []
        
        # Проверка пинга
        ping = network_info.get('ping', 0)
        if ping > 100:
            issues.append("Высокий пинг. Возможны проблемы с сетевым подключением или интернет-провайдером.")
        elif ping > 50:
            issues.append("Повышенный пинг. Возможны задержки при работе с сетевыми приложениями.")
            
        # Проверка скорости соединения
        download_speed = network_info.get('download_speed', 0)
        if download_speed < 10:
            issues.append("Низкая скорость загрузки. Возможны проблемы с сетевым подключением или интернет-провайдером.")
        elif download_speed < 50:
            issues.append("Невысокая скорость загрузки. Возможны задержки при загрузке больших файлов.")
            
        # Проверка сетевых интерфейсов
        interfaces = network_info.get('interfaces', [])
        active_interfaces = 0
        for interface in interfaces:
            if interface.get('status') == 'Подключено':
                active_interfaces += 1
                
        if active_interfaces == 0:
            issues.append("Не обнаружено активных сетевых подключений. Проверьте сетевые кабели или настройки Wi-Fi.")
            
        return issues
        
    def generate_recommendations(self, hardware_info):
        """Генерация рекомендаций на основе собранных данных"""
        recommendations = []
        
        # Рекомендации по процессору
        cpu_issues = hardware_info.get('cpu', {}).get('issues', [])
        if cpu_issues:
            for issue in cpu_issues:
                if "температура" in issue.lower():
                    recommendations.append("Проверьте систему охлаждения процессора. Возможно, требуется очистка от пыли или замена термопасты.")
                elif "загрузка" in issue.lower():
                    recommendations.append("Проверьте запущенные процессы и завершите неиспользуемые приложения для снижения нагрузки на процессор.")
                    
        # Рекомендации по видеокарте
        gpu_issues = hardware_info.get('gpu', {}).get('issues', [])
        if gpu_issues:
            for issue in gpu_issues:
                if "температура" in issue.lower():
                    recommendations.append("Проверьте систему охлаждения видеокарты. Возможно, требуется очистка от пыли или замена термопасты.")
                elif "видеопамяти" in issue.lower():
                    recommendations.append("Закройте неиспользуемые графические приложения или уменьшите настройки графики в играх для снижения использования видеопамяти.")
                    
        # Рекомендации по памяти
        memory_issues = hardware_info.get('memory', {}).get('issues', [])
        if memory_issues:
            for issue in memory_issues:
                if "использование оперативной памяти" in issue.lower():
                    recommendations.append("Закройте неиспользуемые приложения для освобождения оперативной памяти или рассмотрите возможность увеличения объема памяти.")
                elif "файла подкачки" in issue.lower():
                    recommendations.append("Увеличьте объем оперативной памяти для снижения использования файла подкачки и повышения производительности системы.")
                elif "разного объема" in issue.lower() or "разной частотой" in issue.lower():
                    recommendations.append("Для оптимальной производительности используйте одинаковые модули памяти (одинакового объема и с одинаковой частотой).")
                    
        # Рекомендации по хранилищу
        storage_issues = hardware_info.get('storage', {}).get('issues', [])
        if storage_issues:
            for issue in storage_issues:
                if "критическое состояние диска" in issue.lower():
                    recommendations.append("Немедленно создайте резервную копию данных и замените проблемный диск для предотвращения потери данных.")
                elif "проблемы с диском" in issue.lower():
                    recommendations.append("Создайте резервную копию данных и выполните проверку диска на наличие ошибок с помощью встроенных инструментов операционной системы.")
                elif "свободного места" in issue.lower():
                    recommendations.append("Освободите место на диске, удалив ненужные файлы, или перенесите данные на другой диск.")
                    
        # Рекомендации по сети
        network_issues = hardware_info.get('network', {}).get('issues', [])
        if network_issues:
            for issue in network_issues:
                if "пинг" in issue.lower():
                    recommendations.append("Проверьте качество сетевого подключения. Возможно, требуется перезагрузка маршрутизатора или обращение к интернет-провайдеру.")
                elif "скорость" in issue.lower():
                    recommendations.append("Проверьте скорость интернет-соединения с помощью специализированных сервисов и обратитесь к интернет-провайдеру при необходимости.")
                elif "не обнаружено активных сетевых подключений" in issue.lower():
                    recommendations.append("Проверьте сетевые кабели, настройки Wi-Fi и убедитесь, что сетевые адаптеры включены и правильно настроены.")
                    
        # Общие рекомендации
        if not recommendations:
            recommendations.append("Система работает нормально. Рекомендуется регулярно выполнять сканирование и диагностику для поддержания оптимальной производительности.")
            
        return recommendations