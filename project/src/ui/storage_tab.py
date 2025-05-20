#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Вкладка с информацией о хранилище
"""
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QFrame, QGridLayout, QSizePolicy, QProgressBar, QTableWidget,
                            QTableWidgetItem, QHeaderView)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from src.ui.widgets.performance_chart import PerformanceChart

class StorageTab(QWidget):
    """Вкладка с информацией о хранилище"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        main_layout = QVBoxLayout(self)
        
        # Заголовок
        header_label = QLabel("Информация о хранилище")
        header_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        main_layout.addWidget(header_label)
        
        # Таблица с информацией о дисках
        disks_frame = QFrame()
        disks_frame.setFrameShape(QFrame.StyledPanel)
        disks_frame.setFrameShadow(QFrame.Raised)
        disks_layout = QVBoxLayout(disks_frame)
        
        disks_header = QLabel("Диски")
        disks_header.setFont(QFont("Segoe UI", 12, QFont.Bold))
        disks_layout.addWidget(disks_header)
        
        self.disks_table = QTableWidget()
        self.disks_table.setColumnCount(6)
        self.disks_table.setHorizontalHeaderLabels(["Диск", "Тип", "Размер", "Модель", "Интерфейс", "Состояние"])
        self.disks_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        disks_layout.addWidget(self.disks_table)
        
        main_layout.addWidget(disks_frame)
        
        # Использование дисков
        usage_layout = QHBoxLayout()
        
        # График использования дисков
        self.disk_chart = PerformanceChart("Активность дисков", "МБ/с")
        usage_layout.addWidget(self.disk_chart)
        
        # Индикаторы использования дисков
        usage_frame = QFrame()
        usage_frame.setFrameShape(QFrame.StyledPanel)
        usage_frame.setFrameShadow(QFrame.Raised)
        usage_frame_layout = QVBoxLayout(usage_frame)
        
        usage_header = QLabel("Использование дисков")
        usage_header.setFont(QFont("Segoe UI", 10, QFont.Bold))
        usage_header.setAlignment(Qt.AlignCenter)
        usage_frame_layout.addWidget(usage_header)
        
        # Создаем динамические индикаторы для дисков
        self.disk_usage_widgets = {}
        
        # Добавим заглушку, которая будет заменена при обновлении
        placeholder = QLabel("Выполните сканирование для получения информации")
        usage_frame_layout.addWidget(placeholder)
        
        usage_layout.addWidget(usage_frame)
        
        main_layout.addLayout(usage_layout)
        
        # Таблица с информацией о разделах
        partitions_frame = QFrame()
        partitions_frame.setFrameShape(QFrame.StyledPanel)
        partitions_frame.setFrameShadow(QFrame.Raised)
        partitions_layout = QVBoxLayout(partitions_frame)
        
        partitions_header = QLabel("Разделы")
        partitions_header.setFont(QFont("Segoe UI", 12, QFont.Bold))
        partitions_layout.addWidget(partitions_header)
        
        self.partitions_table = QTableWidget()
        self.partitions_table.setColumnCount(5)
        self.partitions_table.setHorizontalHeaderLabels(["Раздел", "Точка монтирования", "Файловая система", "Размер", "Использовано"])
        self.partitions_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        partitions_layout.addWidget(self.partitions_table)
        
        main_layout.addWidget(partitions_frame)
        
        # Диагностика хранилища
        diagnostics_frame = QFrame()
        diagnostics_frame.setFrameShape(QFrame.StyledPanel)
        diagnostics_frame.setFrameShadow(QFrame.Raised)
        diagnostics_layout = QVBoxLayout(diagnostics_frame)
        
        diagnostics_header = QLabel("Диагностика хранилища")
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
        
    def update_info(self, storage_info):
        """Обновление информации о хранилище"""
        if not storage_info:
            return
            
        # Обновление таблицы дисков
        disks = storage_info.get('disks', [])
        self.disks_table.setRowCount(len(disks))
        
        for i, disk in enumerate(disks):
            self.disks_table.setItem(i, 0, QTableWidgetItem(disk.get('device', 'Н/Д')))
            self.disks_table.setItem(i, 1, QTableWidgetItem(disk.get('type', 'Н/Д')))
            self.disks_table.setItem(i, 2, QTableWidgetItem(f"{disk.get('size', 'Н/Д')} ГБ"))
            self.disks_table.setItem(i, 3, QTableWidgetItem(disk.get('model', 'Н/Д')))
            self.disks_table.setItem(i, 4, QTableWidgetItem(disk.get('interface', 'Н/Д')))
            
            # Статус диска с цветовой индикацией
            status_item = QTableWidgetItem(disk.get('status', 'Н/Д'))
            if disk.get('status') == 'Отлично':
                status_item.setForeground(QColor('#4CAF50'))  # Зеленый
            elif disk.get('status') == 'Хорошо':
                status_item.setForeground(QColor('#8BC34A'))  # Светло-зеленый
            elif disk.get('status') == 'Удовлетворительно':
                status_item.setForeground(QColor('#FFC107'))  # Желтый
            elif disk.get('status') == 'Внимание':
                status_item.setForeground(QColor('#FF9800'))  # Оранжевый
            elif disk.get('status') == 'Критично':
                status_item.setForeground(QColor('#F44336'))  # Красный
                
            self.disks_table.setItem(i, 5, status_item)
            
        # Обновление графика активности дисков
        self.disk_chart.update_data(storage_info.get('activity_history', []))
        
        # Обновление индикаторов использования дисков
        # Сначала очищаем существующие виджеты
        usage_frame = self.findChild(QFrame, "usage_frame")
        if usage_frame:
            layout = usage_frame.layout()
            # Удаляем все виджеты, кроме заголовка
            for i in reversed(range(1, layout.count())):
                layout.itemAt(i).widget().setParent(None)
                
            # Добавляем новые индикаторы для каждого диска
            for disk in disks:
                device = disk.get('device', 'Н/Д')
                
                # Создаем метку с названием диска
                disk_label = QLabel(f"{device} ({disk.get('model', 'Н/Д')})")
                layout.addWidget(disk_label)
                
                # Создаем индикатор использования
                usage_bar = QProgressBar()
                usage_bar.setRange(0, 100)
                usage_percent = disk.get('usage_percent', 0)
                usage_bar.setValue(usage_percent)
                usage_bar.setTextVisible(True)
                usage_bar.setFormat(f"{usage_percent}% ({disk.get('used', 'Н/Д')} / {disk.get('size', 'Н/Д')} ГБ)")
                
                # Цветовая индикация использования
                if usage_percent >= 90:
                    usage_bar.setStyleSheet("""
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
                elif usage_percent >= 70:
                    usage_bar.setStyleSheet("""
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
                    usage_bar.setStyleSheet("""
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
                    
                layout.addWidget(usage_bar)
                
                # Сохраняем виджеты для последующего обновления
                self.disk_usage_widgets[device] = usage_bar
        
        # Обновление таблицы разделов
        partitions = storage_info.get('partitions', [])
        self.partitions_table.setRowCount(len(partitions))
        
        for i, partition in enumerate(partitions):
            self.partitions_table.setItem(i, 0, QTableWidgetItem(partition.get('device', 'Н/Д')))
            self.partitions_table.setItem(i, 1, QTableWidgetItem(partition.get('mountpoint', 'Н/Д')))
            self.partitions_table.setItem(i, 2, QTableWidgetItem(partition.get('fstype', 'Н/Д')))
            self.partitions_table.setItem(i, 3, QTableWidgetItem(f"{partition.get('size', 'Н/Д')} ГБ"))
            
            # Использование с процентами
            usage = f"{partition.get('used', 'Н/Д')} ГБ ({partition.get('usage_percent', 'Н/Д')}%)"
            usage_item = QTableWidgetItem(usage)
            
            # Цветовая индикация использования
            usage_percent = partition.get('usage_percent', 0)
            if usage_percent >= 90:
                usage_item.setForeground(QColor('#F44336'))  # Красный
            elif usage_percent >= 70:
                usage_item.setForeground(QColor('#FF9800'))  # Оранжевый
            else:
                usage_item.setForeground(QColor('#4CAF50'))  # Зеленый
                
            self.partitions_table.setItem(i, 4, usage_item)
            
        # Обновление диагностики
        issues = storage_info.get('issues', [])
        if issues:
            issues_text = "<ul>"
            for issue in issues:
                issues_text += f"<li>{issue}</li>"
            issues_text += "</ul>"
            self.diagnostics_label.setText(issues_text)
        else:
            self.diagnostics_label.setText("Проблем с хранилищем не обнаружено.")