#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Вкладка с настройками приложения
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QFrame, QGridLayout, QSizePolicy, QPushButton,
                            QCheckBox, QComboBox, QSpinBox, QGroupBox,
                            QFileDialog, QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

import json
import os

class SettingsTab(QWidget):
    """Вкладка с настройками приложения"""
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.init_ui()
        
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        main_layout = QVBoxLayout(self)
        
        # Заголовок
        header_label = QLabel("Настройки")
        header_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        main_layout.addWidget(header_label)
        
        # Настройки сканирования
        scan_group = QGroupBox("Настройки сканирования")
        scan_layout = QVBoxLayout(scan_group)
        
        # Автоматическое сканирование при запуске
        self.auto_scan_checkbox = QCheckBox("Автоматическое сканирование при запуске")
        self.auto_scan_checkbox.setChecked(self.config.get('auto_scan_on_startup', True))
        scan_layout.addWidget(self.auto_scan_checkbox)
        
        # Интервал автоматического сканирования
        auto_scan_interval_layout = QHBoxLayout()
        auto_scan_interval_label = QLabel("Интервал автоматического сканирования (минуты):")
        self.auto_scan_interval_spinbox = QSpinBox()
        self.auto_scan_interval_spinbox.setRange(1, 60)
        self.auto_scan_interval_spinbox.setValue(self.config.get('auto_scan_interval', 5))
        auto_scan_interval_layout.addWidget(auto_scan_interval_label)
        auto_scan_interval_layout.addWidget(self.auto_scan_interval_spinbox)
        scan_layout.addLayout(auto_scan_interval_layout)
        
        main_layout.addWidget(scan_group)
        
        # Настройки диагностики
        diagnostics_group = QGroupBox("Настройки диагностики")
        diagnostics_layout = QVBoxLayout(diagnostics_group)
        
        # Уровень детализации диагностики
        detail_level_layout = QHBoxLayout()
        detail_level_label = QLabel("Уровень детализации диагностики:")
        self.detail_level_combo = QComboBox()
        self.detail_level_combo.addItem("Базовый")
        self.detail_level_combo.addItem("Стандартный")
        self.detail_level_combo.addItem("Расширенный")
        self.detail_level_combo.setCurrentText(self.config.get('diagnostics_detail_level', 'Стандартный'))
        detail_level_layout.addWidget(detail_level_label)
        detail_level_layout.addWidget(self.detail_level_combo)
        diagnostics_layout.addLayout(detail_level_layout)
        
        # Автоматическая диагностика после сканирования
        self.auto_diagnostics_checkbox = QCheckBox("Автоматическая диагностика после сканирования")
        self.auto_diagnostics_checkbox.setChecked(self.config.get('auto_diagnostics', True))
        diagnostics_layout.addWidget(self.auto_diagnostics_checkbox)
        
        main_layout.addWidget(diagnostics_group)
        
        # Настройки интерфейса
        ui_group = QGroupBox("Настройки интерфейса")
        ui_layout = QVBoxLayout(ui_group)
        
        # Тема интерфейса
        theme_layout = QHBoxLayout()
        theme_label = QLabel("Тема интерфейса:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItem("Светлая")
        self.theme_combo.addItem("Темная")
        self.theme_combo.addItem("Системная")
        self.theme_combo.setCurrentText(self.config.get('ui_theme', 'Светлая'))
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        ui_layout.addLayout(theme_layout)
        
        # Размер шрифта
        font_size_layout = QHBoxLayout()
        font_size_label = QLabel("Размер шрифта:")
        self.font_size_combo = QComboBox()
        self.font_size_combo.addItem("Маленький")
        self.font_size_combo.addItem("Средний")
        self.font_size_combo.addItem("Большой")
        self.font_size_combo.setCurrentText(self.config.get('font_size', 'Средний'))
        font_size_layout.addWidget(font_size_label)
        font_size_layout.addWidget(self.font_size_combo)
        ui_layout.addLayout(font_size_layout)
        
        main_layout.addWidget(ui_group)
        
        # Настройки отчетов
        reports_group = QGroupBox("Настройки отчетов")
        reports_layout = QVBoxLayout(reports_group)
        
        # Путь для сохранения отчетов
        reports_path_layout = QHBoxLayout()
        reports_path_label = QLabel("Путь для сохранения отчетов:")
        self.reports_path_label = QLabel(self.config.get('reports_path', os.path.expanduser('~/Documents')))
        self.reports_path_label.setStyleSheet("border: 1px solid #cccccc; padding: 2px;")
        self.browse_button = QPushButton("Обзор...")
        self.browse_button.clicked.connect(self.browse_reports_path)
        reports_path_layout.addWidget(reports_path_label)
        reports_path_layout.addWidget(self.reports_path_label)
        reports_path_layout.addWidget(self.browse_button)
        reports_layout.addLayout(reports_path_layout)
        
        # Формат отчетов
        report_format_layout = QHBoxLayout()
        report_format_label = QLabel("Формат отчетов:")
        self.report_format_combo = QComboBox()
        self.report_format_combo.addItem("HTML")
        self.report_format_combo.addItem("PDF")
        self.report_format_combo.addItem("TXT")
        self.report_format_combo.setCurrentText(self.config.get('report_format', 'HTML'))
        report_format_layout.addWidget(report_format_label)
        report_format_layout.addWidget(self.report_format_combo)
        reports_layout.addLayout(report_format_layout)
        
        # Автоматическое сохранение отчетов
        self.auto_save_reports_checkbox = QCheckBox("Автоматическое сохранение отчетов")
        self.auto_save_reports_checkbox.setChecked(self.config.get('auto_save_reports', False))
        reports_layout.addWidget(self.auto_save_reports_checkbox)
        
        main_layout.addWidget(reports_group)
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        
        self.save_button = QPushButton("Сохранить настройки")
        self.save_button.clicked.connect(self.save_settings)
        
        self.reset_button = QPushButton("Сбросить настройки")
        self.reset_button.clicked.connect(self.reset_settings)
        
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.reset_button)
        
        main_layout.addLayout(buttons_layout)
        
        # Растягивающийся элемент для заполнения пространства
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(spacer)
        
    def browse_reports_path(self):
        """Выбор пути для сохранения отчетов"""
        directory = QFileDialog.getExistingDirectory(self, "Выберите директорию для сохранения отчетов",
                                                   self.reports_path_label.text())
        if directory:
            self.reports_path_label.setText(directory)
            
    def save_settings(self):
        """Сохранение настроек"""
        # Обновление конфигурации
        self.config['auto_scan_on_startup'] = self.auto_scan_checkbox.isChecked()
        self.config['auto_scan_interval'] = self.auto_scan_interval_spinbox.value()
        self.config['diagnostics_detail_level'] = self.detail_level_combo.currentText()
        self.config['auto_diagnostics'] = self.auto_diagnostics_checkbox.isChecked()
        self.config['ui_theme'] = self.theme_combo.currentText()
        self.config['font_size'] = self.font_size_combo.currentText()
        self.config['reports_path'] = self.reports_path_label.text()
        self.config['report_format'] = self.report_format_combo.currentText()
        self.config['auto_save_reports'] = self.auto_save_reports_checkbox.isChecked()
        
        # Сохранение конфигурации в файл
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'config.json')
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=4)
            QMessageBox.information(self, "Сохранение настроек", "Настройки успешно сохранены")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить настройки: {str(e)}")
            
    def reset_settings(self):
        """Сброс настроек на значения по умолчанию"""
        # Запрос подтверждения
        reply = QMessageBox.question(self, "Сброс настроек", 
                                    "Вы уверены, что хотите сбросить все настройки на значения по умолчанию?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Значения по умолчанию
            self.auto_scan_checkbox.setChecked(True)
            self.auto_scan_interval_spinbox.setValue(5)
            self.detail_level_combo.setCurrentText("Стандартный")
            self.auto_diagnostics_checkbox.setChecked(True)
            self.theme_combo.setCurrentText("Светлая")
            self.font_size_combo.setCurrentText("Средний")
            self.reports_path_label.setText(os.path.expanduser('~/Documents'))
            self.report_format_combo.setCurrentText("HTML")
            self.auto_save_reports_checkbox.setChecked(False)
            
            # Сохранение настроек
            self.save_settings()