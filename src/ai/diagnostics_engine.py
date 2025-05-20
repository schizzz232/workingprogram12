#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль для диагностики системы с использованием ИИ
"""

import os
import sys
import json
import random
import time
import logging
from datetime import datetime
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class DiagnosticsEngine:
    """Класс для диагностики системы с использованием ИИ"""
    
    def __init__(self):
        """Инициализация движка диагностики"""
        self.model_loaded = False
        self.logger = logging.getLogger('diagnostics_engine')
        self.setup_logging()
        self.load_model()
        
    def setup_logging(self):
        """Настройка логирования"""
        self.logger.setLevel(logging.DEBUG)
        
        # Создание форматтера для логов
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Хендлер для файла
        log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        file_handler = logging.FileHandler(os.path.join(log_dir, 'diagnostics_engine.log'))
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Хендлер для консоли
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
    def sanitize_text(self, text):
        """Очистка текста от некорректных символов"""
        try:
            # Проверка на None
            if text is None:
                self.logger.warning("Получен None вместо текста")
                return ""
                
            # Проверка типа
            if not isinstance(text, str):
                self.logger.warning(f"Неверный тип данных: {type(text)}")
                return str(text)
                
            # Удаление или замена некорректных символов
            cleaned_text = "".join(char for char in text if ord(char) < 65536)
            
            # Проверка на изменения
            if cleaned_text != text:
                self.logger.warning(f"Обнаружены и удалены некорректные символы в тексте")
                
            return cleaned_text
        except Exception as e:
            self.logger.error(f"Ошибка при очистке текста: {str(e)}")
            return ""
        
    def load_model(self):
        """Загрузка модели ИИ"""
        try:
            self.logger.info("Начало загрузки модели DistilGPT-2")
            self.tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
            self.model = AutoModelForCausalLM.from_pretrained("distilgpt2")
            self.model_loaded = True
            self.logger.info("Модель успешно загружена")
        except Exception as e:
            self.logger.error(f"Ошибка загрузки модели: {str(e)}")
            self.model_loaded = False
        
    def analyze_with_ai(self, text):
        """Анализ текста с помощью DistilGPT-2"""
        try:
            self.logger.debug(f"Начало анализа текста: {text[:100]}...")
            
            # Очистка входного текста
            cleaned_text = self.sanitize_text(text)
            if not cleaned_text:
                raise ValueError("Пустой текст после очистки")
                
            # Токенизация и проверка
            inputs = self.tokenizer(cleaned_text, return_tensors="pt", max_length=512, truncation=True)
            if inputs["input_ids"].shape[1] == 0:
                raise ValueError("Текст не содержит валидных токенов")
                
            # Генерация
            outputs = self.model.generate(
                inputs["input_ids"],
                max_length=150,
                num_return_sequences=1,
                temperature=0.7,
                top_p=0.9,
                do_sample=True
            )
            
            # Декодирование и очистка результата
            result = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            result = self.sanitize_text(result)
            
            self.logger.debug(f"Анализ успешно завершен")
            return result
        except Exception as e:
            self.logger.error(f"Ошибка анализа: {str(e)}")
            return "Не удалось выполнить анализ"
        
    def run_diagnostics(self, hardware_info):
        """Запуск диагностики системы"""
        try:
            self.logger.info("Начало диагностики системы")
            
            if not self.model_loaded:
                self.logger.warning("Модель не загружена, попытка повторной загрузки")
                self.load_model()
                
            if not isinstance(hardware_info, dict):
                raise TypeError(f"Неверный тип данных hardware_info: {type(hardware_info)}")
                
            # Создание результата диагностики
            diagnostics_result = {}
            
            # Оценка состояния компонентов
            component_scores = {}
            for component in ['cpu', 'gpu', 'memory', 'storage', 'network']:
                try:
                    score = hardware_info.get(component, {}).get('health_score', 0)
                    if not isinstance(score, (int, float)):
                        self.logger.warning(f"Некорректная оценка для {component}: {score}")
                        score = 0
                    component_scores[component] = score
                except Exception as e:
                    self.logger.error(f"Ошибка при обработке {component}: {str(e)}")
                    component_scores[component] = 0
                    
            # Общая оценка системы
            overall_score = self.calculate_overall_score(component_scores)
            
            # Анализ проблем с помощью ИИ
            issues = []
            
            # Анализ CPU
            try:
                cpu_info = hardware_info.get('cpu', {})
                cpu_prompt = self.sanitize_text(
                    f"Analyze CPU health: Temperature {cpu_info.get('temperature')}°C, "
                    f"Usage {cpu_info.get('usage')}%, Model {cpu_info.get('model')}"
                )
                cpu_analysis = self.analyze_with_ai(cpu_prompt)
                if "problem" in cpu_analysis.lower() or "issue" in cpu_analysis.lower():
                    issues.append({
                        'component': 'cpu',
                        'severity': 'warning',
                        'message': cpu_analysis
                    })
            except Exception as e:
                self.logger.error(f"Ошибка при анализе CPU: {str(e)}")
                
            # Анализ GPU
            try:
                gpu_info = hardware_info.get('gpu', {})
                gpu_prompt = self.sanitize_text(
                    f"Analyze GPU health: Temperature {gpu_info.get('temperature')}°C, "
                    f"Usage {gpu_info.get('usage')}%, Memory usage {gpu_info.get('memory_usage_percent')}%"
                )
                gpu_analysis = self.analyze_with_ai(gpu_prompt)
                if "problem" in gpu_analysis.lower() or "issue" in gpu_analysis.lower():
                    issues.append({
                        'component': 'gpu',
                        'severity': 'warning',
                        'message': gpu_analysis
                    })
            except Exception as e:
                self.logger.error(f"Ошибка при анализе GPU: {str(e)}")
                
            # Анализ памяти
            try:
                memory_info = hardware_info.get('memory', {})
                memory_prompt = self.sanitize_text(
                    f"Analyze memory health: Usage {memory_info.get('usage_percent')}%, "
                    f"Available {memory_info.get('free')} GB"
                )
                memory_analysis = self.analyze_with_ai(memory_prompt)
                if "problem" in memory_analysis.lower() or "issue" in memory_analysis.lower():
                    issues.append({
                        'component': 'memory',
                        'severity': 'warning',
                        'message': memory_analysis
                    })
            except Exception as e:
                self.logger.error(f"Ошибка при анализе памяти: {str(e)}")
                
            # Если проблем не обнаружено
            if not issues:
                issues.append({
                    'component': 'system',
                    'severity': 'info',
                    'message': 'Система работает нормально.'
                })
                
            # Формирование рекомендаций с помощью ИИ
            try:
                system_status = self.sanitize_text(
                    f"CPU: {cpu_info.get('model')}, Temperature: {cpu_info.get('temperature')}°C\n"
                    f"GPU: {gpu_info.get('model')}, Temperature: {gpu_info.get('temperature')}°C\n"
                    f"Memory Usage: {memory_info.get('usage_percent')}%"
                )
                
                recommendations_prompt = f"Based on system status:\n{system_status}\nProvide optimization recommendations:"
                recommendations = self.analyze_with_ai(recommendations_prompt).split('\n')
            except Exception as e:
                self.logger.error(f"Ошибка при генерации рекомендаций: {str(e)}")
                recommendations = ["Не удалось сгенерировать рекомендации"]
                
            # Формирование результата диагностики
            diagnostics_result['overall_score'] = overall_score
            diagnostics_result['component_scores'] = component_scores
            diagnostics_result['issues'] = issues
            diagnostics_result['recommendations'] = recommendations
            diagnostics_result['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            self.logger.info("Диагностика успешно завершена")
            return diagnostics_result
            
        except Exception as e:
            self.logger.error(f"Критическая ошибка при выполнении диагностики: {str(e)}")
            return {
                'overall_score': 0,
                'component_scores': {},
                'issues': [{
                    'component': 'system',
                    'severity': 'critical',
                    'message': f'Ошибка при выполнении диагностики: {str(e)}'
                }],
                'recommendations': ['Попробуйте перезапустить диагностику'],
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        
    def calculate_overall_score(self, component_scores):
        """Расчет общей оценки системы"""
        try:
            weights = {
                'cpu': 0.25,
                'gpu': 0.2,
                'memory': 0.2,
                'storage': 0.25,
                'network': 0.1
            }
            
            overall_score = 0
            for component, score in component_scores.items():
                weight = weights.get(component, 0)
                if not isinstance(score, (int, float)):
                    self.logger.warning(f"Некорректная оценка для {component}: {score}")
                    score = 0
                overall_score += score * weight
                
            return round(overall_score)
        except Exception as e:
            self.logger.error(f"Ошибка при расчете общей оценки: {str(e)}")
            return 0