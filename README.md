# 🤖 Chatbot Validador de Documentos

Um chatbot inteligente para validação de documentos brasileiros (CNH e RG) usando **Mindee** para extração de dados e **Groq LLM** para validação inteligente.

## 🚀 Funcionalidades

- **Extração de dados**: Usa Mindee para extrair informações de CNH e RG
- **Validação inteligente**: Utiliza Groq LLM para validar documentos com prompts específicos
- **Interface moderna**: Interface web responsiva com Streamlit
- **Suporte múltiplo**: PDF, JPG, PNG, BMP, TIFF
- **Análise detalhada**: Relatórios completos com métricas de confiança
- **Download de resultados**: Exporta resultados em JSON

## 🛠️ Tecnologias

- **Streamlit**: Interface web
- **Mindee**: API para extração de dados de documentos
- **Groq**: LLM para validação inteligente
- **Python-doctr**: OCR e processamento de documentos
- **Pydantic**: Validação de dados
- **Pillow**: Processamento de imagens

## 📋 Pré-requisitos

- Python 3.13+
- Poetry (será instalado automaticamente pelo script)
- Conta no [Mindee](https://mindee.com/) (API Key)
- Conta no [Groq](https://groq.com/) (API Key)

## 🔧 Instalação

1. **Clone o repositório**:
```bash
git clone <repository-url>
cd chatbot-document-validator
```

2. **Instale as dependências**:
```bash
# Opção 1: Script de instalação automática (recomendado)
./install.sh

# Opção 2: Instalação manual com Poetry
poetry install
```

3. **Configure as API Keys**:
   - Obtenha sua API Key do Mindee
   - Obtenha sua API Key do Groq
   - Configure-as na aplicação (ver seção de uso)

## 📦 Gerenciamento de Dependências

Este projeto usa **Poetry** para gerenciamento de dependências. Comandos úteis:

```bash
# Instalar dependências
poetry install

# Adicionar nova dependência
poetry add nome-do-pacote

# Adicionar dependência de desenvolvimento
poetry add --group dev nome-do-pacote

# Atualizar dependências
poetry update

# Ver dependências instaladas
poetry show

# Executar comando no ambiente virtual
poetry run python script.py

# Ativar shell do Poetry
poetry shell
```

### 🛠️ Comandos Rápidos (Makefile)

Para facilitar o desenvolvimento, use o Makefile:

```bash
# Ver todos os comandos disponíveis
make help

# Instalar dependências
make install-dev

# Executar aplicação
make run

# Executar testes
make test

# Executar testes com cobertura
make test-cov

# Limpar arquivos temporários
make clean

# Verificar ambiente
make check-env
```

## 🚀 Como usar

### Executando a aplicação

```bash
# Opção 1: Usando Streamlit diretamente (RECOMENDADO)
poetry run streamlit run src/chatbot_document_validator/app.py

# Opção 2: Usando Makefile
make run

# Opção 3: Usando script wrapper
poetry run python run_app.py

# Opção 4: Ativando o shell do Poetry
poetry shell
streamlit run src/chatbot_document_validator/app.py
```

### Configuração

1. **Abra a aplicação** no navegador (geralmente `http://localhost:8501`)

2. **Configure as API Keys** no sidebar:
   - **Mindee API Key**: Para extração de dados dos documentos
   - **Groq API Key**: Para validação inteligente

3. **Configure as opções de processamento**:
   - **Detectar tipo automaticamente**: Detecta se é CNH ou RG
   - **Tipo específico**: Escolha manualmente o tipo de documento

### Upload e processamento

1. **Faça upload** de um documento (PDF, JPG, PNG, etc.)
2. **Clique em "Processar Documento"**
3. **Aguarde** o processamento (extração + validação)
4. **Visualize** os resultados detalhados
5. **Baixe** o resultado em JSON se necessário

## 📊 Resultados

A aplicação fornece:

### Dados Extraídos

#### CNH:
- Nome, CPF
- Categoria (A, B, C, D, E, AB, AC, AD, AE)
- Data de emissão, validade e primeira habilitação
- Data de nascimento
- Número de registro
- Órgão emissor

#### RG:
- Nome, CPF, número do RG
- Data de emissão e nascimento
- Nomes dos pais
- Local de nascimento
- Órgão emissor

### Validação
- **Status geral**: Válido, Inválido, Aviso
- **Análise detalhada**: Explicação da validação
- **Erros encontrados**: Lista de problemas
- **Avisos**: Possíveis inconsistências
- **Recomendações**: Sugestões de validação adicional

### Métricas
- **Confiança da extração**: Qualidade dos dados extraídos
- **Confiança da validação**: Confiança da análise do LLM
- **Tempo de processamento**: Performance do sistema

## 🔍 Prompts de Validação

### CNH
O sistema usa prompts específicos para validar CNH, verificando:
- Consistência dos dados
- Formato de CPF e datas
- Lógica temporal (nascimento vs validade)
- Campos obrigatórios
- Possíveis fraudes

### RG
Para RG, valida:
- Consistência dos dados
- Formato de CPF e RG
- Lógica temporal
- Órgão emissor válido
- Campos obrigatórios

## 🏗️ Arquitetura

```
chatbot_document_validator/
├── src/
│   └── chatbot_document_validator/
│       ├── services/
│       │   ├── mindee_service.py      # Integração com Mindee
│       │   ├── validation_service.py  # Validação com Groq
│       │   └── document_processor.py  # Orquestrador principal
│       ├── models/
│       │   └── document_models.py     # Modelos de dados
│       ├── utils/
│       │   └── file_utils.py          # Utilitários de arquivo
│       └── app.py                     # Interface Streamlit
├── tests/                             # Testes
├── pyproject.toml                     # Dependências
├── run_app.py                         # Script de execução
└── README.md                          # Este arquivo
```

## 🔧 Configuração Avançada

### Modelos do Mindee
Você pode configurar diferentes modelos para diferentes tipos de documento:

```python
# Em mindee_service.py
self.model_ids = {
    "cnh": "seu_modelo_cnh",
    "rg": "seu_modelo_rg"
}
```

### Modelos do Groq
Configure diferentes modelos LLM:

```python
# Em validation_service.py
self.model = "llama3-8b-8192"  # ou outro modelo
```

### Prompts Personalizados
Você pode personalizar os prompts de validação editando os métodos:
- `_create_cnh_validation_prompt()`
- `_create_rg_validation_prompt()`

## 🧪 Testes

```bash
# Executar testes
poetry run pytest tests/

# Com cobertura
poetry run pytest --cov=src/chatbot_document_validator tests/

# Executar testes específicos
poetry run pytest tests/test_mindee_mapping.py
```

## 📝 Exemplo de Uso

```python
from chatbot_document_validator.services.document_processor import DocumentProcessor

# Inicializar processador
processor = DocumentProcessor(
    mindee_api_key="sua_mindee_key",
    groq_api_key="sua_groq_key"
)

# Processar documento
result = processor.process_document(
    file_path="documento.pdf",
    document_type="cnh",
    auto_detect=True
)

# Verificar resultado
print(f"Status: {result.overall_status}")
print(f"Válido: {result.validation_result.is_valid}")
print(f"Erros: {result.all_errors}")
```

### Executar exemplo

```bash
# Executar exemplo básico
poetry run python examples/basic_usage.py

# Executar com dados de exemplo
poetry run python examples/sample_data.py
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🆘 Suporte

Se você encontrar problemas ou tiver dúvidas:

1. Verifique se as API Keys estão configuradas corretamente
2. Confirme se o arquivo está em um formato suportado
3. Verifique o tamanho do arquivo (máximo 10MB)
4. Consulte os logs de erro na aplicação

## 🔮 Roadmap

- [ ] Suporte a mais tipos de documento
- [ ] Integração com outras APIs de validação
- [ ] Interface de chat mais avançada
- [ ] Armazenamento de histórico
- [ ] API REST para integração
- [ ] Docker container
- [ ] Deploy na nuvem

---

**Desenvolvido com ❤️ para validação inteligente de documentos brasileiros**
