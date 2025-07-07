# Makefile para Chatbot Validador de Documentos

.PHONY: help install install-dev run test test-cov lint clean

# Comando padrão
help:
	@echo "🤖 Chatbot Validador de Documentos - Comandos disponíveis:"
	@echo ""
	@echo "📦 Instalação:"
	@echo "  install      - Instala dependências de produção"
	@echo "  install-dev  - Instala dependências de desenvolvimento"
	@echo ""
	@echo "🚀 Execução:"
	@echo "  run          - Executa a aplicação Streamlit"
	@echo "  run-app      - Executa usando o script principal"
	@echo ""
	@echo "🧪 Testes:"
	@echo "  test         - Executa todos os testes"
	@echo "  test-cov     - Executa testes com cobertura"
	@echo "  test-mapping - Executa testes de mapeamento"
	@echo ""
	@echo "🔧 Desenvolvimento:"
	@echo "  lint         - Executa linting"
	@echo "  clean        - Remove arquivos temporários"
	@echo "  shell        - Ativa shell do Poetry"

# Instalação
install:
	@echo "📦 Instalando dependências..."
	poetry install --only main

install-dev:
	@echo "📦 Instalando dependências de desenvolvimento..."
	poetry install

# Execução
run:
	@echo "🚀 Executando aplicação Streamlit..."
	poetry run streamlit run src/chatbot_document_validator/app.py

run-app:
	@echo "🚀 Executando aplicação..."
	poetry run python run_app.py

# Testes
test:
	@echo "🧪 Executando testes..."
	poetry run pytest tests/ -v

test-cov:
	@echo "🧪 Executando testes com cobertura..."
	poetry run pytest tests/ --cov=src/chatbot_document_validator --cov-report=html --cov-report=term

test-mapping:
	@echo "🧪 Executando testes de mapeamento..."
	poetry run pytest tests/test_mindee_mapping.py -v

# Desenvolvimento
lint:
	@echo "🔧 Executando linting..."
	poetry run flake8 src/ tests/ examples/
	poetry run black --check src/ tests/ examples/

format:
	@echo "🔧 Formatando código..."
	poetry run black src/ tests/ examples/

clean:
	@echo "🧹 Limpando arquivos temporários..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage

shell:
	@echo "🐚 Ativando shell do Poetry..."
	poetry shell

# Exemplos
example-basic:
	@echo "📝 Executando exemplo básico..."
	poetry run python examples/basic_usage.py

example-data:
	@echo "📝 Executando exemplo de dados..."
	poetry run python examples/sample_data.py

# Verificação de ambiente
check-env:
	@echo "🔍 Verificando ambiente..."
	@echo "Python: $(shell poetry run python --version)"
	@echo "Poetry: $(shell poetry --version)"
	@echo "Streamlit: $(shell poetry run streamlit --version)"
	@echo "Pytest: $(shell poetry run pytest --version)" 