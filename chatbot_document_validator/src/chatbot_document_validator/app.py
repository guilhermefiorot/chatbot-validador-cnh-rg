"""
Aplicação Streamlit para validação de documentos.
"""
import streamlit as st
import os
import json
from datetime import datetime
from typing import Optional

from .services.document_processor import DocumentProcessor
from .utils.file_utils import FileProcessor
from .models.document_models import ProcessedDocument, ValidationStatus


def main():
    """Função principal da aplicação Streamlit."""
    
    # Configuração da página
    st.set_page_config(
        page_title="Chatbot Validador de Documentos",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # CSS personalizado
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .status-valid {
        color: #28a745;
        font-weight: bold;
    }
    .status-invalid {
        color: #dc3545;
        font-weight: bold;
    }
    .status-warning {
        color: #ffc107;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">🤖 Chatbot Validador de Documentos</h1>', unsafe_allow_html=True)
    st.markdown("### Validação inteligente de CNH e RG usando IA")
    
    # Sidebar para configurações
    with st.sidebar:
        st.header("⚙️ Configurações")
        
        # API Keys
        mindee_api_key = st.text_input(
            "Mindee API Key",
            type="password",
            help="Chave da API do Mindee para extração de dados"
        )
        
        groq_api_key = st.text_input(
            "Groq API Key",
            type="password",
            help="Chave da API do Groq para validação"
        )
        
        # Configurações de processamento
        st.subheader("🔧 Configurações de Processamento")
        
        auto_detect = st.checkbox(
            "Detectar tipo automaticamente",
            value=True,
            help="Detecta automaticamente se é CNH ou RG"
        )
        
        document_type = None
        if not auto_detect:
            document_type = st.selectbox(
                "Tipo de documento",
                ["cnh", "rg"],
                help="Tipo específico do documento"
            )
        
        # Informações sobre o sistema
        st.subheader("ℹ️ Sobre")
        st.info("""
        Este sistema utiliza:
        - **Mindee**: Para extração de dados dos documentos
        - **Groq LLM**: Para validação inteligente
        - **Streamlit**: Interface web
        
        Suporta: PDF, JPG, PNG, BMP, TIFF
        """)
    
    # Verificação de API Keys
    if not mindee_api_key or not groq_api_key:
        st.warning("⚠️ Configure as API Keys no sidebar para começar.")
        st.stop()
    
    # Inicialização do processador
    try:
        processor = DocumentProcessor(mindee_api_key, groq_api_key)
    except Exception as e:
        st.error(f"❌ Erro ao inicializar processador: {str(e)}")
        st.stop()
    
    # Área principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📤 Upload de Documento")
        
        # Upload de arquivo
        uploaded_file = st.file_uploader(
            "Escolha um documento para validar",
            type=['pdf', 'jpg', 'jpeg', 'png', 'bmp', 'tiff', 'tif'],
            help="Arraste um arquivo ou clique para selecionar"
        )
        
        if uploaded_file is not None:
            # Validação do arquivo
            is_valid, message = FileProcessor.validate_uploaded_file(uploaded_file)
            
            if not is_valid:
                st.error(f"❌ {message}")
            else:
                st.success(f"✅ {message}")
                
                # Informações do arquivo
                file_info = {
                    "Nome": uploaded_file.name,
                    "Tamanho": f"{uploaded_file.size / (1024*1024):.2f} MB",
                    "Tipo": uploaded_file.type
                }
                
                st.json(file_info)
                
                # Botão de processamento
                if st.button("🚀 Processar Documento", type="primary"):
                    process_document(uploaded_file, processor, document_type, auto_detect)
    
    with col2:
        st.header("📊 Estatísticas")
        
        # Métricas gerais
        if 'processed_documents' not in st.session_state:
            st.session_state.processed_documents = []
        
        total_docs = len(st.session_state.processed_documents)
        valid_docs = len([d for d in st.session_state.processed_documents if d.overall_status == ValidationStatus.VALID])
        invalid_docs = len([d for d in st.session_state.processed_documents if d.overall_status == ValidationStatus.INVALID])
        
        st.metric("Total Processados", total_docs)
        st.metric("Válidos", valid_docs)
        st.metric("Inválidos", invalid_docs)
        
        if total_docs > 0:
            success_rate = (valid_docs / total_docs) * 100
            st.metric("Taxa de Sucesso", f"{success_rate:.1f}%")
    
    # Histórico de documentos processados
    if st.session_state.processed_documents:
        st.header("📋 Histórico de Processamento")
        
        for i, doc in enumerate(reversed(st.session_state.processed_documents)):
            display_document_result(doc, i)


def process_document(uploaded_file, processor, document_type, auto_detect):
    """Processa um documento."""
    
    try:
        # Salva arquivo temporário
        temp_path = FileProcessor.save_uploaded_file(uploaded_file)
        
        if not temp_path:
            st.error("❌ Erro ao salvar arquivo temporário")
            return
        
        try:
            # Processa documento
            with st.spinner("🔄 Processando documento..."):
                processed_doc = processor.process_document(
                    temp_path, 
                    document_type=document_type,
                    auto_detect=auto_detect
                )
            
            # Adiciona à sessão
            if 'processed_documents' not in st.session_state:
                st.session_state.processed_documents = []
            
            st.session_state.processed_documents.append(processed_doc)
            
            # Exibe resultado
            st.success("✅ Documento processado com sucesso!")
            display_document_result(processed_doc, 0)
            
        finally:
            # Limpa arquivo temporário
            FileProcessor.cleanup_temp_file(temp_path)
    
    except Exception as e:
        st.error(f"❌ Erro no processamento: {str(e)}")


def display_document_result(processed_doc: ProcessedDocument, index: int):
    """Exibe resultado do processamento de um documento."""
    
    # Determina cor do status
    status_colors = {
        ValidationStatus.VALID: "status-valid",
        ValidationStatus.INVALID: "status-invalid",
        ValidationStatus.WARNING: "status-warning"
    }
    
    status_class = status_colors.get(processed_doc.overall_status, "")
    
    # Cabeçalho do resultado
    with st.expander(f"📄 {processed_doc.file_name} - {processed_doc.upload_time.strftime('%H:%M:%S')}"):
        
        # Resumo
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Status", 
                processed_doc.overall_status.value.upper(),
                delta=None
            )
        
        with col2:
            st.metric(
                "Confiança Extração",
                f"{processed_doc.document_data.confidence:.1%}"
            )
        
        with col3:
            st.metric(
                "Confiança Validação",
                f"{processed_doc.validation_result.confidence:.1%}"
            )
        
        # Resultado da validação
        st.subheader("🔍 Resultado da Validação")
        
        # Status com cor
        status_text = f"<span class='{status_class}'>{processed_doc.overall_status.value.upper()}</span>"
        st.markdown(f"**Status:** {status_text}", unsafe_allow_html=True)
        
        # Análise
        if processed_doc.validation_result.analysis:
            st.markdown("**Análise:**")
            st.write(processed_doc.validation_result.analysis)
        
        # Erros
        if processed_doc.all_errors:
            st.error("❌ **Erros encontrados:**")
            for error in processed_doc.all_errors:
                st.write(f"• {error}")
        
        # Avisos
        if processed_doc.all_warnings:
            st.warning("⚠️ **Avisos:**")
            for warning in processed_doc.all_warnings:
                st.write(f"• {warning}")
        
        # Recomendações
        if processed_doc.validation_result.recommendations:
            st.info("💡 **Recomendações:**")
            for rec in processed_doc.validation_result.recommendations:
                st.write(f"• {rec}")
        
        # Métricas de performance
        st.subheader("⚡ Métricas de Performance")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if processed_doc.document_data.processing_time:
                st.metric(
                    "Tempo Extração",
                    f"{processed_doc.document_data.processing_time:.2f}s"
                )
        
        with col2:
            if processed_doc.validation_result.validation_time:
                st.metric(
                    "Tempo Validação",
                    f"{processed_doc.validation_result.validation_time:.2f}s"
                )
        
        with col3:
            total_time = (processed_doc.document_data.processing_time or 0) + \
                        (processed_doc.validation_result.validation_time or 0)
            if total_time > 0:
                st.metric("Tempo Total", f"{total_time:.2f}s")


if __name__ == "__main__":
    main() 