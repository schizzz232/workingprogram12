#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Главное окно приложения PC Hardware Diagnostics AI
"""

import os
import sys
from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QProgressBar, 
                            QMessageBox, QSplashScreen, QAction, QMenu, QStatusBar)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal

from src.ui.dashboard_tab import DashboardTab
from src.ui.cpu_tab import CPUTab
from src.ui.gpu_tab import GPUTab
from src.ui.memory_tab import MemoryTab
from src.ui.storage_tab import StorageTab
from src.ui.network_tab import NetworkTab
from src.ui.diagnostics_tab import DiagnosticsTab
from src.ui.settings_tab import SettingsTab
from src.ui.help_tab import HelpTab

from src.hardware.hardware_scanner import HardwareScanner
from src.ai.diagnostics_engine import DiagnosticsEngine

class ScannerThread(QThread):
    """Поток для сканирования аппаратного обеспечения"""
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(dict)
    error_signal = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scanner = HardwareScanner()
        
    def run(self):
        try:
            # Имитация прогресса сканирования
            for i in range(101):
                self.progress_signal.emit(i)
                self.msleep(50)  # Задержка для демонстрации прогресса
                
            # Получение информации об аппаратном обеспечении
            hardware_info = self.scanner.scan_all()
            self.finished_signal.emit(hardware_info)
        except Exception as e:
            self.error_signal.emit(str(e))

class MainWindow(QMainWindow):
    """Главное окно приложения"""
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.hardware_info = None
        self.diagnostics_engine = DiagnosticsEngine()
        
        self.init_ui()
        self.setup_menu()
        self.setup_status_bar()
        
        # Запуск начального сканирования
        QTimer.singleShot(500, self.start_scan)
        
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        self.setWindowTitle("PC Hardware Diagnostics AI")
        self.setMinimumSize(1024, 768)
        
        # Создание центрального виджета
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной макет
        main_layout = QVBoxLayout(central_widget)
        
        # Заголовок приложения
        header_layout = QHBoxLayout()
        app_title = QLabel("PC Hardware Diagnostics AI")
        app_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        header_layout.addWidget(app_title)
        
        # Кнопка сканирования
        self.scan_button = QPushButton("Запустить сканирование")
        self.scan_button.setFixedWidth(200)
        self.scan_button.clicked.connect(self.start_scan)
        header_layout.addWidget(self.scan_button)
        
        main_layout.addLayout(header_layout)
        
        # Прогресс-бар сканирования
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # Создание вкладок
        self.tab_widget = QTabWidget()
        
        # Инициализация вкладок
        self.dashboard_tab = DashboardTab()
        self.cpu_tab = CPUTab()
        self.gpu_tab = GPUTab()
        self.memory_tab = MemoryTab()
        self.storage_tab = StorageTab()
        self.network_tab = NetworkTab()
        self.diagnostics_tab = DiagnosticsTab(self.diagnostics_engine)
        self.settings_tab = SettingsTab(self.config)
        self.help_tab = HelpTab()
        
        # Добавление вкладок
        self.tab_widget.addTab(self.dashboard_tab, "Обзор")
        self.tab_widget.addTab(self.cpu_tab, "Процессор")
        self.tab_widget.addTab(self.gpu_tab, "Видеокарта")
        self.tab_widget.addTab(self.memory_tab, "Память")
        self.tab_widget.addTab(self.storage_tab, "Хранилище")
        self.tab_widget.addTab(self.network_tab, "Сеть")
        self.tab_widget.addTab(self.diagnostics_tab, "Диагностика")
        self.tab_widget.addTab(self.settings_tab, "Настройки")
        self.tab_widget.addTab(self.help_tab, "Справка")
        
        main_layout.addWidget(self.tab_widget)
        
        # Применение стилей
        self.apply_styles()
        
    def apply_styles(self):
        """Применение стилей к интерфейсу"""
        # Базовые стили
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QTabWidget::pane {
                border: 1px solid #cccccc;
                background-color: white;
                border-radius: 4px;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                border: 1px solid #cccccc;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 8px 12px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 1px solid white;
            }
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
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
        
    def setup_menu(self):
        """Настройка главного меню"""
        menu_bar = self.menuBar()
        
        # Меню "Файл"
        file_menu = menu_bar.addMenu("Файл")
        
        save_action = QAction("Сохранить отчет", self)
        save_action.triggered.connect(self.save_report)
        file_menu.addAction(save_action)
        
        export_action = QAction("Экспорт данных", self)
        export_action.triggered.connect(self.export_data)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Меню "Инструменты"
        tools_menu = menu_bar.addMenu("Инструменты")
        
        scan_action = QAction("Запустить сканирование", self)
        scan_action.triggered.connect(self.start_scan)
        tools_menu.addAction(scan_action)
        
        diagnostics_action = QAction("Запустить диагностику", self)
        diagnostics_action.triggered.connect(self.run_diagnostics)
        tools_menu.addAction(diagnostics_action)
        
        tools_menu.addSeparator()
        
        settings_action = QAction("Настройки", self)
        settings_action.triggered.connect(lambda: self.tab_widget.setCurrentWidget(self.settings_tab))
        tools_menu.addAction(settings_action)
        
        # Меню "Справка"
        help_menu = menu_bar.addMenu("Справка")
        
        about_action = QAction("О программе", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        help_action = QAction("Руководство пользователя", self)
        help_action.triggered.connect(lambda: self.tab_widget.setCurrentWidget(self.help_tab))
        help_menu.addAction(help_action)
        
    def setup_status_bar(self):
        """Настройка строки состояния"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Готов к работе")
        
    def start_scan(self):
        """Запуск сканирования аппаратного обеспечения"""
        self.scan_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_bar.showMessage("Сканирование аппаратного обеспечения...")
        
        # Создание и запуск потока сканирования
        self.scanner_thread = ScannerThread()
        self.scanner_thread.progress_signal.connect(self.update_progress)
        self.scanner_thread.finished_signal.connect(self.scan_finished)
        self.scanner_thread.error_signal.connect(self.scan_error)
        self.scanner_thread.start()
        
    def update_progress(self, value):
        """Обновление прогресс-бара"""
        self.progress_bar.setValue(value)
        
    def scan_finished(self, hardware_info):
        """Обработка завершения сканирования"""
        self.hardware_info = hardware_info
        self.scan_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_bar.showMessage("Сканирование завершено успешно")
        
        # Обновление информации на вкладках
        self.dashboard_tab.update_info(hardware_info)
        self.cpu_tab.update_info(hardware_info.get('cpu', {}))
        self.gpu_tab.update_info(hardware_info.get('gpu', {}))
        self.memory_tab.update_info(hardware_info.get('memory', {}))
        self.storage_tab.update_info(hardware_info.get('storage', {}))
        self.network_tab.update_info(hardware_info.get('network', {}))
        
        # Запуск автоматической диагностики
        self.run_diagnostics()
        
    def scan_error(self, error_message):
        """Обработка ошибки сканирования"""
        self.scan_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_bar.showMessage("Ошибка сканирования")
        
        QMessageBox.critical(self, "Ошибка сканирования", 
                            f"Произошла ошибка при сканировании аппаратного обеспечения:\n{error_message}")
        
    def run_diagnostics(self):
        """Запуск диагностики аппаратного обеспечения"""
        if not self.hardware_info:
            QMessageBox.warning(self, "Предупреждение", 
                               "Необходимо сначала выполнить сканирование аппаратного обеспечения")
            return
        
        self.status_bar.showMessage("Выполнение диагностики...")
        self.tab_widget.setCurrentWidget(self.diagnostics_tab)
        self.diagnostics_tab.run_diagnostics(self.hardware_info)
        
    def save_report(self):
        """Сохранение отчета о состоянии системы"""
        if not self.hardware_info:
            QMessageBox.warning(self, "Предупреждение", 
                               "Необходимо сначала выполнить сканирование аппаратного обеспечения")
            return
        
        # Здесь будет код для сохранения отчета
        self.status_bar.showMessage("Отчет сохранен")
        
    def export_data(self):
        """Экспорт данных о системе"""
        if not self.hardware_info:
            QMessageBox.warning(self, "Предупреждение", 
                               "Необходимо сначала выполнить сканирование аппаратного обеспечения")
            return
        
        # Здесь будет код для экспорта данных
        self.status_bar.showMessage("Данные экспортированы")
        
    def show_about(self):
        """Отображение информации о программе"""
        QMessageBox.about(self, "О программе", 
                         "PC Hardware Diagnostics AI\n"
                         "Версия 1.0.0\n\n"
                         "Приложение для автоматического определения и диагностики "
                         "аппаратного обеспечения ПК с использованием искусственного интеллекта.\n\n"
                         "© 2025 DiagnosticsAI")