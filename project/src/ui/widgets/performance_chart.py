#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Виджет для отображения графиков производительности
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

class PerformanceChart(QFrame):
    """График производительности компонента"""
    
    def __init__(self, title, unit):
        super().__init__()
        self.title = title
        self.unit = unit
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.init_ui()
        
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        layout = QVBoxLayout(self)
        
        # Заголовок
        title_label = QLabel(self.title)
        title_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Создание графика
        self.figure = Figure(figsize=(5, 3), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        # Инициализация графика
        self.ax = self.figure.add_subplot(111)
        self.ax.set_ylabel(self.unit)
        self.ax.set_xlabel("Время")
        self.ax.grid(True, linestyle='--', alpha=0.7)
        
        # Начальные данные
        self.x_data = list(range(60))
        self.y_data = [0] * 60
        self.line, = self.ax.plot(self.x_data, self.y_data, 'b-')
        
        # Настройка осей
        self.ax.set_xlim(0, 59)
        self.ax.set_ylim(0, 100)
        
        # Удаление меток на оси X
        self.ax.set_xticks([])
        
        # Настройка стиля
        self.figure.tight_layout()
        
    def update_data(self, data):
        """Обновление данных графика"""
        if not data:
            return
            
        # Обновление данных
        self.y_data = data[-60:] if len(data) > 60 else data + [0] * (60 - len(data))
        self.line.set_ydata(self.y_data)
        
        # Обновление пределов оси Y
        max_value = max(self.y_data) * 1.1
        self.ax.set_ylim(0, max(100, max_value))
        
        # Перерисовка графика
        self.canvas.draw()