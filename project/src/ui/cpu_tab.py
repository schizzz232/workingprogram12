#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Вкладка с информацией о процессоре
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QFrame, QGridLayout, QSizePolicy, QProgressBar)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from src.ui.widgets.performance_chart import PerformanceChart

class CPUTab(QWidget):
    """Вкладка с информацией о процессоре"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        main_layout = QVBoxLayout(self)
        
        # Заголовок
        header_label = QLabel("Информация о процессоре")
        header_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        main_layout.addWidget(header_label)
        
        # Основная информация о процессоре
        info_frame = QFrame()
        info_frame.setFrameShape(QFrame.StyledPanel)
        info_frame.setFrameShadow(QFrame.Raised)
        info_layout = QGridLayout(info_frame)
        
        # Метки для информации
        self.model_label = QLabel("Модель:")
        self.model_value = QLabel("Загрузка...")
        
        self.cores_label = QLabel("Ядра/Потоки:")
        self.cores_value = QLabel("Загрузка...")
        
        self.frequency_label = QLabel("Частота:")
        self.frequency_value = QLabel("Загрузка...")
        
        self.cache_label = QLabel("Кэш:")
        self.cache_value = QLabel("Загрузка...")
        
        self.architecture_label = QLabel("Архитектура:")
        self.architecture_value = QLabel("Загрузка...")
        
        self.temperature_label = QLabel("Температура:")
        self.temperature_value = QLabel("Загрузка...")
        
        # Добавление меток в сетку
        info_layout.addWidget(self.model_label, 0, 0)
        info_layout.addWidget(self.model_value, 0, 1)
        
        info_layout.addWidget(self.cores_label, 1, 0)
        info_layout.addWidget(self.cores_value, 1, 1)
        
        info_layout.addWidget(self.frequency_label, 2, 0)
        info_layout.addWidget(self.frequency_value, 2, 1)
        
        info_layout.addWidget(self.cache_label, 0, 2)
        info_layout.addWidget(self.cache_value, 0, 3)
        
        info_layout.addWidget(self.architecture_label, 1, 2)
        info_layout.addWidget(self.architecture_value, 1, 3)
        
        info_layout.addWidget(self.temperature_label, 2, 2)
        info_layout.addWidget(self.temperature_value, 2, 3)
        
        # Настройка сетки
        info_layout.setColumnStretch(1, 1)
        info_layout.setColumnStretch(3, 1)
        
        main_layout.addWidget(info_frame)
        
        # Загрузка процессора
        usage_layout = QHBoxLayout()
        
        # График загрузки
        self.cpu_chart = PerformanceChart("Загрузка ЦП", "%")
        usage_layout.addWidget(self.cpu_chart)
        
        # Информация о загрузке ядер
        cores_frame = QFrame()
        cores_frame.setFrameShape(QFrame.StyledPanel)
        cores_frame.setFrameShadow(QFrame.Raised)
        cores_layout = QVBoxLayout(cores_frame)
        
        cores_header = QLabel("Загрузка ядер")
        cores_header.setFont(QFont("Segoe UI", 10, QFont.Bold))
        cores_header.setAlignment(Qt.AlignCenter)
        cores_layout.addWidget(cores_header)
        
        self.core_bars = []
        for i in range(8):  # Предполагаем максимум 8 ядер для отображения
            core_layout = QHBoxLayout()
            core_label = QLabel(f"Ядро {i+1}:")
            core_bar = QProgressBar()
            core_bar.setRange(0, 100)
            core_bar.setValue(0)
            core_bar.setTextVisible(True)
            core_bar.setFormat("%v%")
            
            core_layout.addWidget(core_label)
            core_layout.addWidget(core_bar)
            
            cores_layout.addLayout(core_layout)
            self.core_bars.append(core_bar)
            
        usage_layout.addWidget(cores_frame)
        
        main_layout.addLayout(usage_layout)
        
        # Диагностика процессора
        diagnostics_frame = QFrame()
        diagnostics_frame.setFrameShape(QFrame.StyledPanel)
        diagnostics_frame.setFrameShadow(QFrame.Raised)
        diagnostics_layout = QVBoxLayout(diagnostics_frame)
        
        diagnostics_header = QLabel("Диагностика процессора")
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
        
    def update_info(self, cpu_info):
        """Обновление информации о процессоре"""
        if not cpu_info:
            return
            
        # Обновление основной информации
        self.model_value.setText(cpu_info.get('model', 'Неизвестно'))
        self.cores_value.setText(f"{cpu_info.get('cores', 'Н/Д')} / {cpu_info.get('threads', 'Н/Д')}")
        self.frequency_value.setText(f"{cpu_info.get('frequency', 'Н/Д')} ГГц")
        self.cache_value.setText(cpu_info.get('cache', 'Неизвестно'))
        self.architecture_value.setText(cpu_info.get('architecture', 'Неизвестно'))
        
        # Обновление температуры с цветовой индикацией
        temp = cpu_info.get('temperature', 0)
        self.temperature_value.setText(f"{temp}°C")
        
        if temp >= 80:
            self.temperature_value.setStyleSheet("color: #F44336;")  # Красный
        elif temp >= 70:
            self.temperature_value.setStyleSheet("color: #FF9800;")  # Оранжевый
        elif temp >= 60:
            self.temperature_value.setStyleSheet("color: #FFC107;")  # Желтый
        else:
            self.temperature_value.setStyleSheet("color: #4CAF50;")  # Зеленый
            
        # Обновление графика загрузки
        self.cpu_chart.update_data(cpu_info.get('usage_history', []))
        
        # Обновление загрузки ядер
        core_usage = cpu_info.get('core_usage', [])
        for i, bar in enumerate(self.core_bars):
            if i < len(core_usage):
                bar.setValue(int(core_usage[i]))
                # Цветовая индикация загрузки
                if core_usage[i] >= 90:
                    bar.setStyleSheet("""
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
                elif core_usage[i] >= 70:
                    bar.setStyleSheet("""
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
                    bar.setStyleSheet("""
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
            else:
                bar.setValue(0)
                
        # Обновление диагностики
        issues = cpu_info.get('issues', [])
        if issues:
            issues_text = "<ul>"
            for issue in issues:
                issues_text += f"<li>{issue}</li>"
            issues_text += "</ul>"
            self.diagnostics_label.setText(issues_text)
        else:
            self.diagnostics_label.setText("Проблем с процессором не обнаружено.")