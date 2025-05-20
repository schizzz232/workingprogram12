#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Вкладка обзора системы
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QFrame, QGridLayout, QSizePolicy)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt

from src.ui.widgets.system_info_card import SystemInfoCard
from src.ui.widgets.health_indicator import HealthIndicator
from src.ui.widgets.performance_chart import PerformanceChart

class DashboardTab(QWidget):
    """Вкладка с обзором системы"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        main_layout = QVBoxLayout(self)
        
        # Заголовок
        header_label = QLabel("Обзор системы")
        header_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        main_layout.addWidget(header_label)
        
        # Общая информация о системе
        self.system_info_card = SystemInfoCard()
        main_layout.addWidget(self.system_info_card)
        
        # Индикаторы состояния компонентов
        health_layout = QHBoxLayout()
        
        self.cpu_health = HealthIndicator("Процессор")
        self.gpu_health = HealthIndicator("Видеокарта")
        self.memory_health = HealthIndicator("Память")
        self.storage_health = HealthIndicator("Хранилище")
        self.network_health = HealthIndicator("Сеть")
        
        health_layout.addWidget(self.cpu_health)
        health_layout.addWidget(self.gpu_health)
        health_layout.addWidget(self.memory_health)
        health_layout.addWidget(self.storage_health)
        health_layout.addWidget(self.network_health)
        
        main_layout.addLayout(health_layout)
        
        # Графики производительности
        charts_layout = QHBoxLayout()
        
        self.cpu_chart = PerformanceChart("Загрузка ЦП", "%")
        self.memory_chart = PerformanceChart("Использование памяти", "ГБ")
        
        charts_layout.addWidget(self.cpu_chart)
        charts_layout.addWidget(self.memory_chart)
        
        main_layout.addLayout(charts_layout)
        
        # Рекомендации
        recommendations_frame = QFrame()
        recommendations_frame.setFrameShape(QFrame.StyledPanel)
        recommendations_frame.setFrameShadow(QFrame.Raised)
        recommendations_layout = QVBoxLayout(recommendations_frame)
        
        recommendations_header = QLabel("Рекомендации")
        recommendations_header.setFont(QFont("Segoe UI", 12, QFont.Bold))
        recommendations_layout.addWidget(recommendations_header)
        
        self.recommendations_label = QLabel("Выполните сканирование для получения рекомендаций")
        self.recommendations_label.setWordWrap(True)
        recommendations_layout.addWidget(self.recommendations_label)
        
        main_layout.addWidget(recommendations_frame)
        
        # Растягивающийся элемент для заполнения пространства
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(spacer)
        
    def update_info(self, hardware_info):
        """Обновление информации на вкладке"""
        if not hardware_info:
            return
            
        # Обновление общей информации о системе
        system_info = hardware_info.get('system', {})
        self.system_info_card.update_info(system_info)
        
        # Обновление индикаторов состояния
        cpu_info = hardware_info.get('cpu', {})
        gpu_info = hardware_info.get('gpu', {})
        memory_info = hardware_info.get('memory', {})
        storage_info = hardware_info.get('storage', {})
        network_info = hardware_info.get('network', {})
        
        self.cpu_health.update_health(cpu_info.get('health_score', 0))
        self.gpu_health.update_health(gpu_info.get('health_score', 0))
        self.memory_health.update_health(memory_info.get('health_score', 0))
        self.storage_health.update_health(storage_info.get('health_score', 0))
        self.network_health.update_health(network_info.get('health_score', 0))
        
        # Обновление графиков
        self.cpu_chart.update_data(cpu_info.get('usage_history', []))
        self.memory_chart.update_data(memory_info.get('usage_history', []))
        
        # Обновление рекомендаций
        recommendations = hardware_info.get('recommendations', [])
        if recommendations:
            recommendations_text = "<ul>"
            for rec in recommendations:
                recommendations_text += f"<li>{rec}</li>"
            recommendations_text += "</ul>"
            self.recommendations_label.setText(recommendations_text)
        else:
            self.recommendations_label.setText("Проблем не обнаружено. Система работает нормально.")