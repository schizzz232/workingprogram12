#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль для работы с конфигурацией приложения
"""

import os
import json
import logging

def load_config(config_path):
    """Загрузка конфигурации из файла"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        logging.warning(f"Файл конфигурации не найден: {config_path}")
        return {}
    except json.JSONDecodeError:
        logging.error(f"Ошибка при чтении файла конфигурации: {config_path}")
        return {}

def save_config(config, config_path):
    """Сохранение конфигурации в файл"""
    try:
        # Создание директории, если она не существует
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        logging.error(f"Ошибка при сохранении файла конфигурации: {str(e)}")
        return False

def create_default_config(config_path):
    """Создание конфигурации по умолчанию"""
    default_config = {
        "auto_scan_on_startup": True,
        "auto_scan_interval": 5,
        "diagnostics_detail_level": "Стандартный",
        "auto_diagnostics": True,
        "ui_theme": "Светлая",
        "font_size": "Средний",
        "reports_path": os.path.expanduser('~/Documents'),
        "report_format": "HTML",
        "auto_save_reports": False
    }
    
    return save_config(default_config, config_path)