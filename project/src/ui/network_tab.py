#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Вкладка с информацией о сети
"""
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QFrame, QGridLayout, QSizePolicy, QTableWidget,
                            QTableWidgetItem, QHeaderView)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from src.ui.widgets.performance_chart import PerformanceChart

class NetworkTab(QWidget):
    """Вкладка с информацией о сети"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        main_layout = QVBoxLayout(self)
        
        # Заголовок
        header_label = QLabel("Информация о сети")
        header_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        main_layout.addWidget(header_label)
        
        # Таблица с информацией о сетевых интерфейсах
        interfaces_frame = QFrame()
        interfaces_frame.setFrameShape(QFrame.StyledPanel)
        interfaces_frame.setFrameShadow(QFrame.Raised)
        interfaces_layout = QVBoxLayout(interfaces_frame)
        
        interfaces_header = QLabel("Сетевые интерфейсы")
        interfaces_header.setFont(QFont("Segoe UI", 12, QFont.Bold))
        interfaces_layout.addWidget(interfaces_header)
        
        self.interfaces_table = QTableWidget()
        self.interfaces_table.setColumnCount(6)
        self.interfaces_table.setHorizontalHeaderLabels(["Интерфейс", "IP-адрес", "MAC-адрес", "Скорость", "Статус", "Тип"])
        self.interfaces_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        interfaces_layout.addWidget(self.interfaces_table)
        
        main_layout.addWidget(interfaces_frame)
        
        # Графики сетевой активности
        charts_layout = QHBoxLayout()
        
        # График входящего трафика
        self.download_chart = PerformanceChart("Входящий трафик", "МБ/с")
        charts_layout.addWidget(self.download_chart)
        
        # График исходящего трафика
        self.upload_chart = PerformanceChart("Исходящий трафик", "МБ/с")
        charts_layout.addWidget(self.upload_chart)
        
        main_layout.addLayout(charts_layout)
        
        # Информация о подключении
        connection_frame = QFrame()
        connection_frame.setFrameShape(QFrame.StyledPanel)
        connection_frame.setFrameShadow(QFrame.Raised)
        connection_layout = QVBoxLayout(connection_frame)
        
        connection_header = QLabel("Информация о подключении")
        connection_header.setFont(QFont("Segoe UI", 12, QFont.Bold))
        connection_layout.addWidget(connection_header)
        
        connection_grid = QGridLayout()
        
        # Метки для информации о подключении
        self.gateway_label = QLabel("Шлюз:")
        self.gateway_value = QLabel("Загрузка...")
        
        self.dns_label = QLabel("DNS-серверы:")
        self.dns_value = QLabel("Загрузка...")
        
        self.public_ip_label = QLabel("Внешний IP:")
        self.public_ip_value = QLabel("Загрузка...")
        
        self.ping_label = QLabel("Пинг:")
        self.ping_value = QLabel("Загрузка...")
        
        self.download_speed_label = QLabel("Скорость загрузки:")
        self.download_speed_value = QLabel("Загрузка...")
        
        self.upload_speed_label = QLabel("Скорость отдачи:")
        self.upload_speed_value = QLabel("Загрузка...")
        
        # Добавление меток в сетку
        connection_grid.addWidget(self.gateway_label, 0, 0)
        connection_grid.addWidget(self.gateway_value, 0, 1)
        
        connection_grid.addWidget(self.dns_label, 1, 0)
        connection_grid.addWidget(self.dns_value, 1, 1)
        
        connection_grid.addWidget(self.public_ip_label, 2, 0)
        connection_grid.addWidget(self.public_ip_value, 2, 1)
        
        connection_grid.addWidget(self.ping_label, 0, 2)
        connection_grid.addWidget(self.ping_value, 0, 3)
        
        connection_grid.addWidget(self.download_speed_label, 1, 2)
        connection_grid.addWidget(self.download_speed_value, 1, 3)
        
        connection_grid.addWidget(self.upload_speed_label, 2, 2)
        connection_grid.addWidget(self.upload_speed_value, 2, 3)
        
        # Настройка сетки
        connection_grid.setColumnStretch(1, 1)
        connection_grid.setColumnStretch(3, 1)
        
        connection_layout.addLayout(connection_grid)
        
        main_layout.addWidget(connection_frame)
        
        # Диагностика сети
        diagnostics_frame = QFrame()
        diagnostics_frame.setFrameShape(QFrame.StyledPanel)
        diagnostics_frame.setFrameShadow(QFrame.Raised)
        diagnostics_layout = QVBoxLayout(diagnostics_frame)
        
        diagnostics_header = QLabel("Диагностика сети")
        diagnostics_header.setFont(QFont("Segoe UI", 12, QFont.Bold))
        diagnostics_layout.addWidget(diagnostics_header)
        
        self.diagnostics_label = QLabel("Выполните сканирование для получения диагностики")
        self.diagnostics_label.setWordWrap(True)
        diagnostics_layout.addWidget(self.diagnostics_label)
        
        main_layout.addWidget(diagnostics_frame)
        
        # Растягивающийся элемент для заполнения пространства
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(spacer)
        
    def update_info(self, network_info):
        """Обновление информации о сети"""
        if not network_info:
            return
            
        # Обновление таблицы сетевых интерфейсов
        interfaces = network_info.get('interfaces', [])
        self.interfaces_table.setRowCount(len(interfaces))
        
        for i, interface in enumerate(interfaces):
            self.interfaces_table.setItem(i, 0, QTableWidgetItem(interface.get('name', 'Н/Д')))
            self.interfaces_table.setItem(i, 1, QTableWidgetItem(interface.get('ip', 'Н/Д')))
            self.interfaces_table.setItem(i, 2, QTableWidgetItem(interface.get('mac', 'Н/Д')))
            self.interfaces_table.setItem(i, 3, QTableWidgetItem(f"{interface.get('speed', 'Н/Д')} Мбит/с"))
            
            # Статус с цветовой индикацией
            status_item = QTableWidgetItem(interface.get('status', 'Н/Д'))
            if interface.get('status') == 'Подключено':
                status_item.setForeground(QColor('#4CAF50'))  # Зеленый
            elif interface.get('status') == 'Отключено':
                status_item.setForeground(QColor('#F44336'))  # Красный
            elif interface.get('status') == 'Ошибка':
                status_item.setForeground(QColor('#FF9800'))  # Оранжевый
                
            self.interfaces_table.setItem(i, 4, status_item)
            self.interfaces_table.setItem(i, 5, QTableWidgetItem(interface.get('type', 'Н/Д')))
            
        # Обновление графиков сетевой активности
        self.download_chart.update_data(network_info.get('download_history', []))
        self.upload_chart.update_data(network_info.get('upload_history', []))
        
        # Обновление информации о подключении
        self.gateway_value.setText(network_info.get('gateway', 'Н/Д'))
        self.dns_value.setText(', '.join(network_info.get('dns_servers', ['Н/Д'])))
        self.public_ip_value.setText(network_info.get('public_ip', 'Н/Д'))
        
        # Обновление пинга с цветовой индикацией
        ping = network_info.get('ping', 0)
        self.ping_value.setText(f"{ping} мс")
        
        if ping >= 100:
            self.ping_value.setStyleSheet("color: #F44336;")  # Красный
        elif ping >= 50:
            self.ping_value.setStyleSheet("color: #FF9800;")  # Оранжевый
        else:
            self.ping_value.setStyleSheet("color: #4CAF50;")  # Зеленый
            
        # Обновление скорости соединения
        self.download_speed_value.setText(f"{network_info.get('download_speed', 'Н/Д')} Мбит/с")
        self.upload_speed_value.setText(f"{network_info.get('upload_speed', 'Н/Д')} Мбит/с")
        
        # Обновление диагностики
        issues = network_info.get('issues', [])
        if issues:
            issues_text = "<ul>"
            for issue in issues:
                issues_text += f"<li>{issue}</li>"
            issues_text += "</ul>"
            self.diagnostics_label.setText(issues_text)
        else:
            self.diagnostics_label.setText("Проблем с сетью не обнаружено.")