#!/usr/bin/env python3
"""
Exemplo básico de uso do Chatbot Validador de Documentos.

Este exemplo demonstra como usar a biblioteca programaticamente
sem a interface Streamlit.
"""
import sys
import os
import json
from pathlib import Path

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from chatbot_document_validator.services.document_processor import DocumentProcessor
from chatbot_document_validator.utils.file_utils import FileProcessor


def main():
    """Exemplo principal de uso."""
    
    print("🤖 Chatbot Validador de Documentos - Exemplo de Uso")
    print("=" * 60)
    
    # Configuração das API Keys
    # ⚠️ IMPORTANTE: Substitua pelas suas chaves reais
    MINDEE_API_KEY = "sua_mindee_api_key_aqui"
    GROQ_API_KEY = "sua_groq_api_key_aqui"
    
    # Verifica se as chaves foram configuradas
    if MINDEE_API_KEY == "sua_mindee_api_key_aqui" or GROQ_API_KEY == "sua_groq_api_key_aqui":
        print("❌ Erro: Configure suas API Keys no código antes de executar")
        print("   - MINDEE_API_KEY: Obtenha em https://mindee.com/")
        print("   - GROQ_API_KEY: Obtenha em https://groq.com/")
        return
    
    try:
        # Inicializa o processador
        print("🔧 Inicializando processador...")
        processor = DocumentProcessor(MINDEE_API_KEY, GROQ_API_KEY)
        print("✅ Processador inicializado com sucesso!")
        
        # Exemplo 1: Processamento de CNH
        print("\n📄 Exemplo 1: Processamento de CNH")
        print("-" * 40)
        
        # Simula dados de uma CNH (em um caso real, você teria um arquivo)
        cnh_file_path = "exemplo_cnh.pdf"  # Substitua pelo caminho real
        
        if os.path.exists(cnh_file_path):
            print(f"📋 Processando arquivo: {cnh_file_path}")
            
            # Processa o documento
            result = processor.process_document(
                file_path=cnh_file_path,
                document_type="cnh",
                auto_detect=False
            )
            
            # Exibe resultados
            display_results(result)
        else:
            print(f"⚠️ Arquivo {cnh_file_path} não encontrado")
            print("   Crie um arquivo de exemplo ou ajuste o caminho")
        
        # Exemplo 2: Processamento de RG
        print("\n📄 Exemplo 2: Processamento de RG")
        print("-" * 40)
        
        rg_file_path = "exemplo_rg.jpg"  # Substitua pelo caminho real
        
        if os.path.exists(rg_file_path):
            print(f"📋 Processando arquivo: {rg_file_path}")
            
            # Processa o documento
            result = processor.process_document(
                file_path=rg_file_path,
                document_type="rg",
                auto_detect=False
            )
            
            # Exibe resultados
            display_results(result)
        else:
            print(f"⚠️ Arquivo {rg_file_path} não encontrado")
            print("   Crie um arquivo de exemplo ou ajuste o caminho")
        
        # Exemplo 4: Análise de arquivo
        print("\n📄 Exemplo 4: Análise de arquivo")
        print("-" * 40)
        
        test_file = "teste.pdf"
        if os.path.exists(test_file):
            analysis = FileProcessor.get_file_info(test_file)
            print(f"📊 Informações do arquivo:")
            print(f"   Nome: {analysis[0]}")
            print(f"   Tamanho: {analysis[1]} bytes")
            print(f"   Tipo: {analysis[2]}")
            
            # Inferência de tipo
            inferred_type = FileProcessor.get_document_type_from_filename(analysis[0])
            print(f"   Tipo inferido: {inferred_type}")
        else:
            print(f"⚠️ Arquivo {test_file} não encontrado")
        
        print("\n✅ Exemplos concluídos!")
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        print("   Verifique suas API Keys e conexão com a internet")


def display_results(processed_doc):
    """Exibe resultados do processamento."""
    
    print(f"📊 Resultados para: {processed_doc.file_name}")
    print(f"   Tipo: {processed_doc.document_data.document_type.value}")
    print(f"   Status: {processed_doc.overall_status.value}")
    print(f"   Válido: {processed_doc.validation_result.is_valid}")
    print(f"   Confiança Extração: {processed_doc.document_data.confidence:.1%}")
    print(f"   Confiança Validação: {processed_doc.validation_result.confidence:.1%}")
    
    # Dados extraídos
    if processed_doc.document_data.extracted_fields:
        print(f"   📋 Dados extraídos:")
        for field_name, field in processed_doc.document_data.extracted_fields.items():
            if field.value:
                print(f"      {field_name}: {field.value} (confiança: {field.confidence:.1%})")
    
    # Erros e avisos
    if processed_doc.all_errors:
        print(f"   ❌ Erros: {len(processed_doc.all_errors)}")
        for error in processed_doc.all_errors[:3]:  # Mostra apenas os 3 primeiros
            print(f"      • {error}")
    
    if processed_doc.all_warnings:
        print(f"   ⚠️ Avisos: {len(processed_doc.all_warnings)}")
        for warning in processed_doc.all_warnings[:3]:  # Mostra apenas os 3 primeiros
            print(f"      • {warning}")
    
    # Análise
    if processed_doc.validation_result.analysis:
        print(f"   🔍 Análise: {processed_doc.validation_result.analysis[:100]}...")
    
    # Métricas de performance
    total_time = (processed_doc.document_data.processing_time or 0) + \
                (processed_doc.validation_result.validation_time or 0)
    print(f"   ⚡ Tempo total: {total_time:.2f}s")


def create_sample_files():
    """Cria arquivos de exemplo para teste."""
    
    print("📝 Criando arquivos de exemplo...")
    
    # Cria diretório de exemplos se não existir
    examples_dir = Path("examples")
    examples_dir.mkdir(exist_ok=True)
    
    # Arquivo de exemplo 1: CNH
    cnh_content = """
    CNH - Carteira Nacional de Habilitação
    Nome: João Silva Santos
    CPF: 123.456.789-00
    Categoria: B
    Data Emissão: 2025-01-27
    Data Validade: 2035-01-27
    Data Nascimento: 2001-05-02
    Número Registro: 07450883117
    Órgão Emissor: SPTC SP
    Data Primeira Habilitação: 2020-08-07
    """
    
    with open("exemplo_cnh.pdf", "w") as f:
        f.write(cnh_content)
    
    # Arquivo de exemplo 2: RG
    rg_content = """
    RG - Registro Geral
    Nome: Maria Oliveira Costa
    Número RG: 4.021.923 - SP
    CPF: 987.654.321-00
    Data Emissão: 2020-02-07
    Nome do Pai: Carlos Costa Silva
    Nome da Mãe: Ana Oliveira Costa
    Data Nascimento: 2001-02-05
    Local Nascimento: SÃO PAULO - SP
    Órgão Emissor: SP
    """
    
    with open("exemplo_rg.jpg", "w") as f:
        f.write(rg_content)
    
    print("✅ Arquivos de exemplo criados!")


if __name__ == "__main__":
    # Descomente a linha abaixo para criar arquivos de exemplo
    # create_sample_files()
    
    main() 