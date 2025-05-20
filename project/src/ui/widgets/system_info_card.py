#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Виджет с информацией о системе
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QFrame, QGridLayout)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class SystemInfoCard(QFrame):
    """Карточка с общей информацией о системе"""
    
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.init_ui()
        
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        layout = QVBoxLayout(self)
        
        # Заголовок
        header_label = QLabel("Информация о системе")
        header_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        layout.addWidget(header_label)
        
        # Сетка с информацией
        grid_layout = QGridLayout()
        
        # Метки для информации
        self.os_label = QLabel("Операционная система:")
        self.os_value = QLabel("Загрузка...")
        
        self.cpu_label = QLabel("Процессор:")
        self.cpu_value = QLabel("Загрузка...")
        
        self.gpu_label = QLabel("Видеокарта:")
        self.gpu_value = QLabel("Загрузка...")
        
        self.ram_label = QLabel("Оперативная память:")
        self.ram_value = QLabel("Загрузка...")
        
        self.motherboard_label = QLabel("Материнская плата:")
        self.motherboard_value = QLabel("Загрузка...")
        
        # Добавление меток в сетку
        grid_layout.addWidget(self.os_label, 0, 0)
        grid_layout.addWidget(self.os_value, 0, 1)
        
        grid_layout.addWidget(self.cpu_label, 1, 0)
        grid_layout.addWidget(self.cpu_value, 1, 1)
        
        grid_layout.addWidget(self.gpu_label, 2, 0)
        grid_layout.addWidget(self.gpu_value, 2, 1)
        
        grid_layout.addWidget(self.ram_label, 3, 0)
        grid_layout.addWidget(self.ram_value, 3, 1)
        
        grid_layout.addWidget(self.motherboard_label, 4, 0)
        grid_layout.addWidget(self.motherboard_value, 4, 1)
        
        # Настройка сетки
        grid_layout.setColumnStretch(1, 1)
        
        layout.addLayout(grid_layout)
        
    def update_info(self, system_info):
        """Обновление информации о системе"""
        if not system_info:
            return
            
        self.os_value.setText(system_info.get('os_name', 'Неизвестно'))
        self.cpu_value.setText(system_info.get('cpu_name', 'Неизвестно'))
        self.gpu_value.setText(system_info.get('gpu_name', 'Неизвестно'))
        self.ram_value.setText(system_info.get('ram_info', 'Неизвестно'))
        self.motherboard_value.setText(system_info.get('motherboard', 'Неизвестно'))