# Makefile para Chatbot Validador de Documentos

.PHONY: help install install-dev run test test-cov lint clean

# Comando padrão
help:
	@echo "🤖 Chatbot Validador de Documentos - Comandos disponíveis:"
	@echo ""
	@echo "📦 Instalação:"
	@echo "  poetry install      - Instala dependências de produção"
	@echo ""
	@echo " Ambiente:"
	@echo " poetry shell         -Executa o ambiente venv do poetry"
	@echo ""
	@echo "🚀 Execução:"
	@echo "  streamlit run run_app.py - Executa a aplicação Streamlit"

install:
	@echo "📦 Instalando dependências..."
	poetry install

shell:
	@echo "🐚 Ativando shell do Poetry..."
	poetry shell

run:
	@echo "🚀 Executando aplicação Streamlit..."
	streamlit run run_app.py
