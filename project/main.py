#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PC Hardware Diagnostics AI - Главный модуль приложения
Автоматическое определение и диагностика аппаратного обеспечения ПК с использованием ИИ
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QIcon, QFont

# Импорт модулей приложения
from src.ui.main_window import MainWindow
from src.utils.logger import setup_logger
from src.utils.config import load_config, create_default_config

def main():
    """Основная функция запуска приложения"""
    # Настройка логирования
    logger = setup_logger()
    logger.info("Запуск приложения PC Hardware Diagnostics AI")
    
    # Загрузка конфигурации
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
    if not os.path.exists(config_path):
        create_default_config(config_path)
    config = load_config(config_path)
    
    # Настройка приложения Qt
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QCoreApplication.setApplicationName("PC Hardware Diagnostics AI")
    QCoreApplication.setOrganizationName("DiagnosticsAI")
    QCoreApplication.setApplicationVersion("1.0.0")
    
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Использование стиля Fusion для кроссплатформенности
    
    # Установка шрифта по умолчанию
    font = QFont("Segoe UI", 9)
    app.setFont(font)
    
    # Создание и отображение главного окна
    main_window = MainWindow(config)
    main_window.show()
    
    # Запуск цикла обработки событий
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()