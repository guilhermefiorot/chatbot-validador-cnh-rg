#!/usr/bin/env python3
"""
Script wrapper para executar a aplicação Streamlit.

NOTA: Para desenvolvimento, é recomendado usar diretamente:
    streamlit run src/chatbot_document_validator/app.py

Este script é uma alternativa que importa e executa a aplicação.
"""
import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from chatbot_document_validator.app import main

if __name__ == "__main__":
    print("🚀 Iniciando Chatbot Validador de Documentos...")
    print("💡 Dica: Para desenvolvimento, use: streamlit run src/chatbot_document_validator/app.py")
    main() 