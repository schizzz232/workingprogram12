#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Вкладка с информацией об оперативной памяти
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QFrame, QGridLayout, QSizePolicy, QProgressBar, QTableWidget,
                            QTableWidgetItem, QHeaderView)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from src.ui.widgets.performance_chart import PerformanceChart

class MemoryTab(QWidget):
    """Вкладка с информацией об оперативной памяти"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        main_layout = QVBoxLayout(self)
        
        # Заголовок
        header_label = QLabel("Информация об оперативной памяти")
        header_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        main_layout.addWidget(header_label)
        
        # Основная информация о памяти
        info_frame = QFrame()
        info_frame.setFrameShape(QFrame.StyledPanel)
        info_frame.setFrameShadow(QFrame.Raised)
        info_layout = QGridLayout(info_frame)
        
        # Метки для информации
        self.total_label = QLabel("Общий объем:")
        self.total_value = QLabel("Загрузка...")
        
        self.used_label = QLabel("Используется:")
        self.used_value = QLabel("Загрузка...")
        
        self.free_label = QLabel("Свободно:")
        self.free_value = QLabel("Загрузка...")
        
        self.type_label = QLabel("Тип памяти:")
        self.type_value = QLabel("Загрузка...")
        
        self.frequency_label = QLabel("Частота:")
        self.frequency_value = QLabel("Загрузка...")
        
        self.channels_label = QLabel("Каналы:")
        self.channels_value = QLabel("Загрузка...")
        
        # Добавление меток в сетку
        info_layout.addWidget(self.total_label, 0, 0)
        info_layout.addWidget(self.total_value, 0, 1)
        
        info_layout.addWidget(self.used_label, 1, 0)
        info_layout.addWidget(self.used_value, 1, 1)
        
        info_layout.addWidget(self.free_label, 2, 0)
        info_layout.addWidget(self.free_value, 2, 1)
        
        info_layout.addWidget(self.type_label, 0, 2)
        info_layout.addWidget(self.type_value, 0, 3)
        
        info_layout.addWidget(self.frequency_label, 1, 2)
        info_layout.addWidget(self.frequency_value, 1, 3)
        
        info_layout.addWidget(self.channels_label, 2, 2)
        info_layout.addWidget(self.channels_value, 2, 3)
        
        # Настройка сетки
        info_layout.setColumnStretch(1, 1)
        info_layout.setColumnStretch(3, 1)
        
        main_layout.addWidget(info_frame)
        
        # Использование памяти
        usage_layout = QHBoxLayout()
        
        # График использования памяти
        self.memory_chart = PerformanceChart("Использование памяти", "ГБ")
        usage_layout.addWidget(self.memory_chart)
        
        # Индикатор использования памяти
        usage_frame = QFrame()
        usage_frame.setFrameShape(QFrame.StyledPanel)
        usage_frame.setFrameShadow(QFrame.Raised)
        usage_frame_layout = QVBoxLayout(usage_frame)
        
        usage_header = QLabel("Использование памяти")
        usage_header.setFont(QFont("Segoe UI", 10, QFont.Bold))
        usage_header.setAlignment(Qt.AlignCenter)
        usage_frame_layout.addWidget(usage_header)
        
        self.memory_usage_bar = QProgressBar()
        self.memory_usage_bar.setRange(0, 100)
        self.memory_usage_bar.setValue(0)
        self.memory_usage_bar.setTextVisible(True)
        self.memory_usage_bar.setFormat("%v%")
        usage_frame_layout.addWidget(self.memory_usage_bar)
        
        # Информация о виртуальной памяти
        virtual_header = QLabel("Виртуальная память (файл подкачки)")
        virtual_header.setFont(QFont("Segoe UI", 10, QFont.Bold))
        virtual_header.setAlignment(Qt.AlignCenter)
        usage_frame_layout.addWidget(virtual_header)
        
        virtual_layout = QGridLayout()
        
        virtual_total_label = QLabel("Общий объем:")
        self.virtual_total_value = QLabel("Загрузка...")
        
        virtual_used_label = QLabel("Используется:")
        self.virtual_used_value = QLabel("Загрузка...")
        
        virtual_layout.addWidget(virtual_total_label, 0, 0)
        virtual_layout.addWidget(self.virtual_total_value, 0, 1)
        
        virtual_layout.addWidget(virtual_used_label, 1, 0)
        virtual_layout.addWidget(self.virtual_used_value, 1, 1)
        
        usage_frame_layout.addLayout(virtual_layout)
        
        usage_layout.addWidget(usage_frame)
        
        main_layout.addLayout(usage_layout)
        
        # Таблица с информацией о модулях памяти
        modules_frame = QFrame()
        modules_frame.setFrameShape(QFrame.StyledPanel)
        modules_frame.setFrameShadow(QFrame.Raised)
        modules_layout = QVBoxLayout(modules_frame)
        
        modules_header = QLabel("Модули памяти")
        modules_header.setFont(QFont("Segoe UI", 12, QFont.Bold))
        modules_layout.addWidget(modules_header)
        
        self.modules_table = QTableWidget()
        self.modules_table.setColumnCount(5)
        self.modules_table.setHorizontalHeaderLabels(["Слот", "Размер", "Тип", "Частота", "Производитель"])
        self.modules_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        modules_layout.addWidget(self.modules_table)
        
        main_layout.addWidget(modules_frame)
        
        # Диагностика памяти
        diagnostics_frame = QFrame()
        diagnostics_frame.setFrameShape(QFrame.StyledPanel)
        diagnostics_frame.setFrameShadow(QFrame.Raised)
        diagnostics_layout = QVBoxLayout(diagnostics_frame)
        
        diagnostics_header = QLabel("Диагностика памяти")
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
        
    def update_info(self, memory_info):
        """Обновление информации о памяти"""
        if not memory_info:
            return
            
        # Обновление основной информации
        self.total_value.setText(f"{memory_info.get('total', 'Н/Д')} ГБ")
        self.used_value.setText(f"{memory_info.get('used', 'Н/Д')} ГБ")
        self.free_value.setText(f"{memory_info.get('free', 'Н/Д')} ГБ")
        self.type_value.setText(memory_info.get('type', 'Неизвестно'))
        self.frequency_value.setText(f"{memory_info.get('frequency', 'Н/Д')} МГц")
        self.channels_value.setText(memory_info.get('channels', 'Неизвестно'))
        
        # Обновление графика использования памяти
        self.memory_chart.update_data(memory_info.get('usage_history', []))
        
        # Обновление индикатора использования памяти
        memory_usage = memory_info.get('usage_percent', 0)
        self.memory_usage_bar.setValue(int(memory_usage))
        
        # Цветовая индикация использования памяти
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
            
        # Обновление информации о виртуальной памяти
        self.virtual_total_value.setText(f"{memory_info.get('swap_total', 'Н/Д')} ГБ")
        self.virtual_used_value.setText(f"{memory_info.get('swap_used', 'Н/Д')} ГБ")
        
        # Обновление таблицы модулей памяти
        modules = memory_info.get('modules', [])
        self.modules_table.setRowCount(len(modules))
        
        for i, module in enumerate(modules):
            self.modules_table.setItem(i, 0, QTableWidgetItem(module.get('slot', 'Н/Д')))
            self.modules_table.setItem(i, 1, QTableWidgetItem(f"{module.get('size', 'Н/Д')} ГБ"))
            self.modules_table.setItem(i, 2, QTableWidgetItem(module.get('type', 'Н/Д')))
            self.modules_table.setItem(i, 3, QTableWidgetItem(f"{module.get('frequency', 'Н/Д')} МГц"))
            self.modules_table.setItem(i, 4, QTableWidgetItem(module.get('manufacturer', 'Н/Д')))
            
        # Обновление диагностики
        issues = memory_info.get('issues', [])
        if issues:
            issues_text = "<ul>"
            for issue in issues:
                issues_text += f"<li>{issue}</li>"
            issues_text += "</ul>"
            self.diagnostics_label.setText(issues_text)
        else:
            self.diagnostics_label.setText("Проблем с оперативной памятью не обнаружено.")