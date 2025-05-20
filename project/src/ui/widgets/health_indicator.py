#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Индикатор состояния компонента
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QProgressBar)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

class HealthIndicator(QWidget):
    """Индикатор состояния компонента системы"""
    
    def __init__(self, component_name):
        super().__init__()
        self.component_name = component_name
        self.init_ui()
        
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        layout = QVBoxLayout(self)
        
        # Название компонента
        self.name_label = QLabel(self.component_name)
        self.name_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.name_label)
        
        # Индикатор состояния
        self.health_bar = QProgressBar()
        self.health_bar.setRange(0, 100)
        self.health_bar.setValue(0)
        self.health_bar.setTextVisible(True)
        self.health_bar.setFormat("%v%")
        layout.addWidget(self.health_bar)
        
        # Статус
        self.status_label = QLabel("Ожидание сканирования")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Установка минимальной ширины
        self.setMinimumWidth(150)
        
    def update_health(self, health_score):
        """Обновление индикатора состояния"""
        self.health_bar.setValue(health_score)
        
        # Обновление цвета индикатора в зависимости от состояния
        if health_score >= 80:
            self.health_bar.setStyleSheet("""
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
            self.status_label.setText("Отлично")
        elif health_score >= 60:
            self.health_bar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid #cccccc;
                    border-radius: 4px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #8BC34A;
                    border-radius: 3px;
                }
            """)
            self.status_label.setText("Хорошо")
        elif health_score >= 40:
            self.health_bar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid #cccccc;
                    border-radius: 4px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #FFC107;
                    border-radius: 3px;
                }
            """)
            self.status_label.setText("Удовлетворительно")
        elif health_score >= 20:
            self.health_bar.setStyleSheet("""
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
            self.status_label.setText("Внимание")
        else:
            self.health_bar.setStyleSheet("""
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
            self.status_label.setText("Критично")