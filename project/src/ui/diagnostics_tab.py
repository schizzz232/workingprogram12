#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Вкладка с диагностикой системы
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QFrame, QGridLayout, QSizePolicy, QPushButton,
                            QTextEdit, QProgressBar, QComboBox)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QThread, pyqtSignal

from src.ai.diagnostics_engine import DiagnosticsEngine

class DiagnosticsThread(QThread):
    """Поток для выполнения диагностики"""
    progress_signal = pyqtSignal(int)
    result_signal = pyqtSignal(dict)
    error_signal = pyqtSignal(str)
    
    def __init__(self, diagnostics_engine, hardware_info, parent=None):
        super().__init__(parent)
        self.diagnostics_engine = diagnostics_engine
        self.hardware_info = hardware_info
        
    def run(self):
        try:
            # Имитация прогресса диагностики
            for i in range(101):
                self.progress_signal.emit(i)
                self.msleep(50)  # Задержка для демонстрации прогресса
                
            # Выполнение диагностики
            diagnostics_result = self.diagnostics_engine.run_diagnostics(self.hardware_info)
            self.result_signal.emit(diagnostics_result)
        except Exception as e:
            self.error_signal.emit(str(e))

class DiagnosticsTab(QWidget):
    """Вкладка с диагностикой системы"""
    
    def __init__(self, diagnostics_engine):
        super().__init__()
        self.diagnostics_engine = diagnostics_engine
        self.init_ui()
        
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        main_layout = QVBoxLayout(self)
        
        # Заголовок
        header_label = QLabel("Диагностика системы")
        header_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        main_layout.addWidget(header_label)
        
        # Панель управления диагностикой
        control_layout = QHBoxLayout()
        
        # Выбор типа диагностики
        self.diagnostics_type_combo = QComboBox()
        self.diagnostics_type_combo.addItem("Полная диагностика")
        self.diagnostics_type_combo.addItem("Диагностика процессора")
        self.diagnostics_type_combo.addItem("Диагностика видеокарты")
        self.diagnostics_type_combo.addItem("Диагностика памяти")
        self.diagnostics_type_combo.addItem("Диагностика хранилища")
        self.diagnostics_type_combo.addItem("Диагностика сети")
        control_layout.addWidget(self.diagnostics_type_combo)
        
        # Кнопка запуска диагностики
        self.run_button = QPushButton("Запустить диагностику")
        self.run_button.clicked.connect(self.start_diagnostics)
        control_layout.addWidget(self.run_button)
        
        main_layout.addLayout(control_layout)
        
        # Прогресс-бар диагностики
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # Результаты диагностики
        results_frame = QFrame()
        results_frame.setFrameShape(QFrame.StyledPanel)
        results_frame.setFrameShadow(QFrame.Raised)
        results_layout = QVBoxLayout(results_frame)
        
        results_header = QLabel("Результаты диагностики")
        results_header.setFont(QFont("Segoe UI", 12, QFont.Bold))
        results_layout.addWidget(results_header)
        
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setMinimumHeight(300)
        results_layout.addWidget(self.results_text)
        
        main_layout.addWidget(results_frame)
        
        # Рекомендации
        recommendations_frame = QFrame()
        recommendations_frame.setFrameShape(QFrame.StyledPanel)
        recommendations_frame.setFrameShadow(QFrame.Raised)
        recommendations_layout = QVBoxLayout(recommendations_frame)
        
        recommendations_header = QLabel("Рекомендации")
        recommendations_header.setFont(QFont("Segoe UI", 12, QFont.Bold))
        recommendations_layout.addWidget(recommendations_header)
        
        self.recommendations_text = QTextEdit()
        self.recommendations_text.setReadOnly(True)
        self.recommendations_text.setMinimumHeight(150)
        recommendations_layout.addWidget(self.recommendations_text)
        
        main_layout.addWidget(recommendations_frame)
        
        # Растягивающийся элемент для заполнения пространства
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(spacer)
        
    def start_diagnostics(self):
        """Запуск диагностики вручную"""
        if not hasattr(self, 'hardware_info') or not self.hardware_info:
            self.results_text.setHtml("<p style='color: #F44336;'>Ошибка: Необходимо сначала выполнить сканирование аппаратного обеспечения</p>")
            return
            
        self.run_diagnostics(self.hardware_info)
        
    def run_diagnostics(self, hardware_info):
        """Запуск диагностики системы"""
        self.hardware_info = hardware_info
        self.run_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Очистка предыдущих результатов
        self.results_text.clear()
        self.recommendations_text.clear()
        
        # Создание и запуск потока диагностики
        self.diagnostics_thread = DiagnosticsThread(self.diagnostics_engine, hardware_info)
        self.diagnostics_thread.progress_signal.connect(self.update_progress)
        self.diagnostics_thread.result_signal.connect(self.diagnostics_finished)
        self.diagnostics_thread.error_signal.connect(self.diagnostics_error)
        self.diagnostics_thread.start()
        
    def update_progress(self, value):
        """Обновление прогресс-бара"""
        self.progress_bar.setValue(value)
        
    def diagnostics_finished(self, diagnostics_result):
        """Обработка завершения диагностики"""
        self.run_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        # Обработка результатов диагностики
        self.display_diagnostics_results(diagnostics_result)
        
    def diagnostics_error(self, error_message):
        """Обработка ошибки диагностики"""
        self.run_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        self.results_text.setHtml(f"<p style='color: #F44336;'>Ошибка при выполнении диагностики: {error_message}</p>")
        
    def display_diagnostics_results(self, diagnostics_result):
        """Отображение результатов диагностики"""
        if not diagnostics_result:
            self.results_text.setHtml("<p>Нет данных для отображения</p>")
            return
            
        # Формирование HTML для результатов
        html_result = "<h3>Общая оценка системы</h3>"
        
        # Общая оценка системы
        overall_score = diagnostics_result.get('overall_score', 0)
        score_color = self.get_score_color(overall_score)
        html_result += f"<p>Общая оценка: <span style='color: {score_color}; font-weight: bold;'>{overall_score}/100</span></p>"
        
        # Оценки по компонентам
        html_result += "<h3>Оценки по компонентам</h3>"
        html_result += "<ul>"
        
        component_scores = diagnostics_result.get('component_scores', {})
        for component, score in component_scores.items():
            component_name = {
                'cpu': 'Процессор',
                'gpu': 'Видеокарта',
                'memory': 'Оперативная память',
                'storage': 'Хранилище',
                'network': 'Сеть'
            }.get(component, component)
            
            score_color = self.get_score_color(score)
            html_result += f"<li>{component_name}: <span style='color: {score_color}; font-weight: bold;'>{score}/100</span></li>"
            
        html_result += "</ul>"
        
        # Выявленные проблемы
        issues = diagnostics_result.get('issues', [])
        if issues:
            html_result += "<h3>Выявленные проблемы</h3>"
            html_result += "<ul>"
            
            for issue in issues:
                severity = issue.get('severity', 'info')
                severity_color = {
                    'critical': '#F44336',  # Красный
                    'warning': '#FF9800',   # Оранжевый
                    'info': '#2196F3'       # Синий
                }.get(severity, '#2196F3')
                
                severity_text = {
                    'critical': 'Критическая',
                    'warning': 'Предупреждение',
                    'info': 'Информация'
                }.get(severity, 'Информация')
                
                html_result += f"<li><span style='color: {severity_color}; font-weight: bold;'>[{severity_text}]</span> {issue.get('message', '')}</li>"
                
            html_result += "</ul>"
        else:
            html_result += "<p style='color: #4CAF50;'>Проблем не обнаружено. Система работает нормально.</p>"
            
        # Детальная информация
        html_result += "<h3>Детальная информация</h3>"
        details = diagnostics_result.get('details', {})
        
        for component, component_details in details.items():
            component_name = {
                'cpu': 'Процессор',
                'gpu': 'Видеокарта',
                'memory': 'Оперативная память',
                'storage': 'Хранилище',
                'network': 'Сеть'
            }.get(component, component)
            
            html_result += f"<h4>{component_name}</h4>"
            
            if isinstance(component_details, dict):
                html_result += "<ul>"
                for key, value in component_details.items():
                    html_result += f"<li><b>{key}:</b> {value}</li>"
                html_result += "</ul>"
            elif isinstance(component_details, list):
                html_result += "<ul>"
                for item in component_details:
                    html_result += f"<li>{item}</li>"
                html_result += "</ul>"
            else:
                html_result += f"<p>{component_details}</p>"
                
        # Отображение результатов
        self.results_text.setHtml(html_result)
        
        # Отображение рекомендаций
        recommendations = diagnostics_result.get('recommendations', [])
        if recommendations:
            html_recommendations = "<ul>"
            for rec in recommendations:
                html_recommendations += f"<li>{rec}</li>"
            html_recommendations += "</ul>"
            self.recommendations_text.setHtml(html_recommendations)
        else:
            self.recommendations_text.setHtml("<p>Рекомендации отсутствуют.</p>")
            
    def get_score_color(self, score):
        """Получение цвета в зависимости от оценки"""
        if score >= 80:
            return '#4CAF50'  # Зеленый
        elif score >= 60:
            return '#8BC34A'  # Светло-зеленый
        elif score >= 40:
            return '#FFC107'  # Желтый
        elif score >= 20:
            return '#FF9800'  # Оранжевый
        else:
            return '#F44336'  # Красный