#!/bin/bash

# Script de instalação para o Chatbot Validador de Documentos

echo "🤖 Instalando Validador de Documentos..."
echo "================================================"

# Instala dependências com Poetry
echo "📚 Instalando dependências com Poetry..."
poetry install

echo ""
echo "✅ Instalação concluída!"
echo ""
echo "🚀 Para executar a aplicação:"
echo "1. Execute: poetry shell"
echo "2. Execute: streamlit run run_app.py"
echo ""
echo "📋 Próximos passos:"
echo "1. Configure suas API Keys do Mindee e Groq"
echo "2. Execute a aplicação"
echo "3. Acesse http://localhost:8501 no navegador"