#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль для настройки логирования
"""

import os
import logging
from datetime import datetime

def setup_logger():
    """Настройка логирования"""
    # Создание директории для логов, если она не существует
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
        
    # Имя файла лога с датой и временем
    log_file = os.path.join(logs_dir, f"app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
    # Настройка логирования
    logger = logging.getLogger('pc_hardware_diagnostics')
    logger.setLevel(logging.INFO)
    
    # Обработчик для записи в файл
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    
    # Обработчик для вывода в консоль
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Формат сообщений
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Добавление обработчиков
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger