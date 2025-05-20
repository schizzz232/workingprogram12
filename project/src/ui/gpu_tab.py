#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Вкладка с информацией о видеокарте
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QFrame, QGridLayout, QSizePolicy, QProgressBar)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from src.ui.widgets.performance_chart import PerformanceChart

class GPUTab(QWidget):
    """Вкладка с информацией о видеокарте"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        main_layout = QVBoxLayout(self)
        
        # Заголовок
        header_label = QLabel("Информация о видеокарте")
        header_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        main_layout.addWidget(header_label)
        
        # Основная информация о видеокарте
        info_frame = QFrame()
        info_frame.setFrameShape(QFrame.StyledPanel)
        info_frame.setFrameShadow(QFrame.Raised)
        info_layout = QGridLayout(info_frame)
        
        # Метки для информации
        self.model_label = QLabel("Модель:")
        self.model_value = QLabel("Загрузка...")
        
        self.memory_label = QLabel("Видеопамять:")
        self.memory_value = QLabel("Загрузка...")
        
        self.driver_label = QLabel("Версия драйвера:")
        self.driver_value = QLabel("Загрузка...")
        
        self.resolution_label = QLabel("Разрешение:")
        self.resolution_value = QLabel("Загрузка...")
        
        self.interface_label = QLabel("Интерфейс:")
        self.interface_value = QLabel("Загрузка...")
        
        self.temperature_label = QLabel("Температура:")
        self.temperature_value = QLabel("Загрузка...")
        
        # Добавление меток в сетку
        info_layout.addWidget(self.model_label, 0, 0)
        info_layout.addWidget(self.model_value, 0, 1)
        
        info_layout.addWidget(self.memory_label, 1, 0)
        info_layout.addWidget(self.memory_value, 1, 1)
        
        info_layout.addWidget(self.driver_label, 2, 0)
        info_layout.addWidget(self.driver_value, 2, 1)
        
        info_layout.addWidget(self.resolution_label, 0, 2)
        info_layout.addWidget(self.resolution_value, 0, 3)
        
        info_layout.addWidget(self.interface_label, 1, 2)
        info_layout.addWidget(self.interface_value, 1, 3)
        
        info_layout.addWidget(self.temperature_label, 2, 2)
        info_layout.addWidget(self.temperature_value, 2, 3)
        
        # Настройка сетки
        info_layout.setColumnStretch(1, 1)
        info_layout.setColumnStretch(3, 1)
        
        main_layout.addWidget(info_frame)
        
        # Использование видеокарты
        usage_layout = QHBoxLayout()
        
        # График загрузки GPU
        self.gpu_chart = PerformanceChart("Загрузка GPU", "%")
        usage_layout.addWidget(self.gpu_chart)
        
        # График использования видеопамяти
        self.memory_chart = PerformanceChart("Использование видеопамяти", "МБ")
        usage_layout.addWidget(self.memory_chart)
        
        main_layout.addLayout(usage_layout)
        
        # Индикаторы использования
        indicators_frame = QFrame()
        indicators_frame.setFrameShape(QFrame.StyledPanel)
        indicators_frame.setFrameShadow(QFrame.Raised)
        indicators_layout = QVBoxLayout(indicators_frame)
        
        # Загрузка GPU
        gpu_usage_layout = QHBoxLayout()
        gpu_usage_label = QLabel("Загрузка GPU:")
        self.gpu_usage_bar = QProgressBar()
        self.gpu_usage_bar.setRange(0, 100)
        self.gpu_usage_bar.setValue(0)
        self.gpu_usage_bar.setTextVisible(True)
        self.gpu_usage_bar.setFormat("%v%")
        
        gpu_usage_layout.addWidget(gpu_usage_label)
        gpu_usage_layout.addWidget(self.gpu_usage_bar)
        indicators_layout.addLayout(gpu_usage_layout)
        
        # Использование видеопамяти
        memory_usage_layout = QHBoxLayout()
        memory_usage_label = QLabel("Использование видеопамяти:")
        self.memory_usage_bar = QProgressBar()
        self.memory_usage_bar.setRange(0, 100)
        self.memory_usage_bar.setValue(0)
        self.memory_usage_bar.setTextVisible(True)
        self.memory_usage_bar.setFormat("%v%")
        
        memory_usage_layout.addWidget(memory_usage_label)
        memory_usage_layout.addWidget(self.memory_usage_bar)
        indicators_layout.addLayout(memory_usage_layout)
        
        main_layout.addWidget(indicators_frame)
        
        # Диагностика видеокарты
        diagnostics_frame = QFrame()
        diagnostics_frame.setFrameShape(QFrame.StyledPanel)
        diagnostics_frame.setFrameShadow(QFrame.Raised)
        diagnostics_layout = QVBoxLayout(diagnostics_frame)
        
        diagnostics_header = QLabel("Диагностика видеокарты")
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
        
    def update_info(self, gpu_info):
        """Обновление информации о видеокарте"""
        if not gpu_info:
            return
            
        # Обновление основной информации
        self.model_value.setText(gpu_info.get('model', 'Неизвестно'))
        self.memory_value.setText(f"{gpu_info.get('memory', 'Н/Д')} МБ")
        self.driver_value.setText(gpu_info.get('driver_version', 'Неизвестно'))
        self.resolution_value.setText(gpu_info.get('resolution', 'Неизвестно'))
        self.interface_value.setText(gpu_info.get('interface', 'Неизвестно'))
        
        # Обновление температуры с цветовой индикацией
        temp = gpu_info.get('temperature', 0)
        self.temperature_value.setText(f"{temp}°C")
        
        if temp >= 85:
            self.temperature_value.setStyleSheet("color: #F44336;")  # Красный
        elif temp >= 75:
            self.temperature_value.setStyleSheet("color: #FF9800;")  # Оранжевый
        elif temp >= 65:
            self.temperature_value.setStyleSheet("color: #FFC107;")  # Желтый
        else:
            self.temperature_value.setStyleSheet("color: #4CAF50;")  # Зеленый
            
        # Обновление графиков
        self.gpu_chart.update_data(gpu_info.get('usage_history', []))
        self.memory_chart.update_data(gpu_info.get('memory_usage_history', []))
        
        # Обновление индикаторов использования
        gpu_usage = gpu_info.get('usage', 0)
        self.gpu_usage_bar.setValue(gpu_usage)
        
        # Цветовая индикация загрузки GPU
        if gpu_usage >= 90:
            self.gpu_usage_bar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid #cccccc;
                    border-radius: 4px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #F44336;
                    border-radius: 3px;
                }
            """)
        elif gpu_usage >= 70:
            self.gpu_usage_bar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid #cccccc;
                    border-radius: 4px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #FF9800;
                    border-radius: 3px;
                }
            """)
        else:
            self.gpu_usage_bar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid #cccccc;
                    border-radius: 4px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #4CAF50;
                    border-radius: 3px;
                }
            """)
            
        # Обновление использования видеопамяти
        memory_usage = gpu_info.get('memory_usage_percent', 0)
        self.memory_usage_bar.setValue(memory_usage)
        
        # Цветовая индикация использования видеопамяти
        if memory_usage >= 90:
            self.memory_usage_bar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid #cccccc;
                    border-radius: 4px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #F44336;
                    border-radius: 3px;
                }
            """)
        elif memory_usage >= 70:
            self.memory_usage_bar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid #cccccc;
                    border-radius: 4px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #FF9800;
                    border-radius: 3px;
                }
            """)
        else:
            self.memory_usage_bar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid #cccccc;
                    border-radius: 4px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #4CAF50;
                    border-radius: 3px;
                }
            """)
            
        # Обновление диагностики
        issues = gpu_info.get('issues', [])
        if issues:
            issues_text = "<ul>"
            for issue in issues:
                issues_text += f"<li>{issue}</li>"
            issues_text += "</ul>"
            self.diagnostics_label.setText(issues_text)
        else:
            self.diagnostics_label.setText("Проблем с видеокартой не обнаружено.")