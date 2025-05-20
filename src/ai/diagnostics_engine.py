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
from datetime import datetime
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class DiagnosticsEngine:
    """Класс для диагностики системы с использованием ИИ"""
    
    def __init__(self):
        """Инициализация движка диагностики"""
        self.model_loaded = False
        self.load_model()
        
    def load_model(self):
        """Загрузка модели ИИ"""
        try:
            self.tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
            self.model = AutoModelForCausalLM.from_pretrained("distilgpt2")
            self.model_loaded = True
        except Exception as e:
            print(f"Ошибка загрузки модели: {str(e)}")
            self.model_loaded = False
        
    def analyze_with_ai(self, text):
        """Анализ текста с помощью DistilGPT-2"""
        try:
            inputs = self.tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
            outputs = self.model.generate(
                inputs["input_ids"],
                max_length=150,
                num_return_sequences=1,
                temperature=0.7,
                top_p=0.9,
                do_sample=True
            )
            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        except Exception as e:
            print(f"Ошибка анализа: {str(e)}")
            return "Не удалось выполнить анализ"
        
    def run_diagnostics(self, hardware_info):
        """Запуск диагностики системы"""
        if not self.model_loaded:
            self.load_model()
            
        # Создание результата диагностики
        diagnostics_result = {}
        
        # Оценка состояния компонентов
        component_scores = {
            'cpu': hardware_info.get('cpu', {}).get('health_score', 0),
            'gpu': hardware_info.get('gpu', {}).get('health_score', 0),
            'memory': hardware_info.get('memory', {}).get('health_score', 0),
            'storage': hardware_info.get('storage', {}).get('health_score', 0),
            'network': hardware_info.get('network', {}).get('health_score', 0)
        }
        
        # Общая оценка системы
        overall_score = self.calculate_overall_score(component_scores)
        
        # Анализ проблем с помощью ИИ
        issues = []
        
        # Анализ CPU
        cpu_info = hardware_info.get('cpu', {})
        cpu_prompt = f"Analyze CPU health: Temperature {cpu_info.get('temperature')}°C, Usage {cpu_info.get('usage')}%, Model {cpu_info.get('model')}"
        cpu_analysis = self.analyze_with_ai(cpu_prompt)
        if "problem" in cpu_analysis.lower() or "issue" in cpu_analysis.lower():
            issues.append({
                'component': 'cpu',
                'severity': 'warning',
                'message': cpu_analysis
            })
            
        # Анализ GPU
        gpu_info = hardware_info.get('gpu', {})
        gpu_prompt = f"Analyze GPU health: Temperature {gpu_info.get('temperature')}°C, Usage {gpu_info.get('usage')}%, Memory usage {gpu_info.get('memory_usage_percent')}%"
        gpu_analysis = self.analyze_with_ai(gpu_prompt)
        if "problem" in gpu_analysis.lower() or "issue" in gpu_analysis.lower():
            issues.append({
                'component': 'gpu',
                'severity': 'warning',
                'message': gpu_analysis
            })
            
        # Анализ памяти
        memory_info = hardware_info.get('memory', {})
        memory_prompt = f"Analyze memory health: Usage {memory_info.get('usage_percent')}%, Available {memory_info.get('free')} GB"
        memory_analysis = self.analyze_with_ai(memory_prompt)
        if "problem" in memory_analysis.lower() or "issue" in memory_analysis.lower():
            issues.append({
                'component': 'memory',
                'severity': 'warning',
                'message': memory_analysis
            })
            
        # Если проблем не обнаружено
        if not issues:
            issues.append({
                'component': 'system',
                'severity': 'info',
                'message': 'Система работает нормально.'
            })
            
        # Формирование рекомендаций с помощью ИИ
        system_status = f"CPU: {cpu_info.get('model')}, Temperature: {cpu_info.get('temperature')}°C\n"
        system_status += f"GPU: {gpu_info.get('model')}, Temperature: {gpu_info.get('temperature')}°C\n"
        system_status += f"Memory Usage: {memory_info.get('usage_percent')}%"
        
        recommendations_prompt = f"Based on system status:\n{system_status}\nProvide optimization recommendations:"
        recommendations = self.analyze_with_ai(recommendations_prompt).split('\n')
        
        # Формирование результата диагностики
        diagnostics_result['overall_score'] = overall_score
        diagnostics_result['component_scores'] = component_scores
        diagnostics_result['issues'] = issues
        diagnostics_result['recommendations'] = recommendations
        diagnostics_result['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return diagnostics_result
        
    def calculate_overall_score(self, component_scores):
        """Расчет общей оценки системы"""
        weights = {
            'cpu': 0.25,
            'gpu': 0.2,
            'memory': 0.2,
            'storage': 0.25,
            'network': 0.1
        }
        
        overall_score = 0
        for component, score in component_scores.items():
            overall_score += score * weights.get(component, 0)
            
        return round(overall_score)