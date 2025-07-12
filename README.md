# 🤖 Validador de Documentos

Um validador inteligente para documentos brasileiros (CNH e RG) usando **Mindee** para extração de dados e **Groq LLM** para validação inteligente.

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

# Atualizar dependências
poetry update

# Ver dependências instaladas
poetry show

# Ativar shell do Poetry
poetry shell
```

## 🚀 Como usar

### Executando a aplicação

```bash
# Opção 1: Usando Streamlit diretamente (RECOMENDADO)
poetry run streamlit run src/chatbot_document_validator/app.py

# Opção 4: Ativando o shell do Poetry
poetry shell
streamlit run run_app.py
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
