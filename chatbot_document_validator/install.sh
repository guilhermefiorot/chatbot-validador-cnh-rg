#!/bin/bash

# Script de instalação para o Chatbot Validador de Documentos

echo "🤖 Instalando Chatbot Validador de Documentos..."
echo "================================================"

# Verifica se Python 3.13+ está instalado
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.13"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Erro: Python 3.13+ é necessário. Versão atual: $python_version"
    exit 1
fi

echo "✅ Python $python_version detectado"

# Verifica se Poetry está instalado
if ! command -v poetry &> /dev/null; then
    echo "📦 Instalando Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    
    # Adiciona Poetry ao PATH
    export PATH="$HOME/.local/bin:$PATH"
    
    echo "✅ Poetry instalado!"
else
    echo "✅ Poetry já está instalado"
fi

# Instala dependências com Poetry
echo "📚 Instalando dependências com Poetry..."
poetry install

# Instala o projeto em modo desenvolvimento
echo "🔧 Instalando projeto em modo desenvolvimento..."
poetry install -e .

echo ""
echo "✅ Instalação concluída!"
echo ""
echo "🚀 Para executar a aplicação:"
echo "1. Execute: poetry run python run_app.py"
echo "2. Ou ative o shell: poetry shell"
echo "   E depois: python run_app.py"
echo ""
echo "📋 Próximos passos:"
echo "1. Configure suas API Keys do Mindee e Groq"
echo "2. Execute a aplicação"
echo "3. Acesse http://localhost:8501 no navegador"
echo ""
echo "📖 Para mais informações, consulte o README.md" 