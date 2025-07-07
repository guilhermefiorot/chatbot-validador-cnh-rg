"""
Serviço principal para processamento de documentos.
"""
import time
from typing import Dict, Any, Optional
import streamlit as st

from ..services.mindee_service import MindeeService
from ..services.validation_service import DocumentValidationService
from ..utils.file_utils import FileProcessor, DocumentAnalyzer
from ..models.document_models import (
    DocumentData, 
    ValidationResult, 
    ProcessedDocument, 
    DocumentType,
    ExtractedField
)


class DocumentProcessor:
    """Serviço principal para processamento e validação de documentos."""
    
    def __init__(self, mindee_api_key: str, groq_api_key: str):
        self.mindee_service = MindeeService(mindee_api_key)
        self.validation_service = DocumentValidationService(groq_api_key)
    
    def process_document(
        self, 
        file_path: str, 
        document_type: Optional[str] = None,
        auto_detect: bool = True
    ) -> ProcessedDocument:
        """
        Processa um documento completo: extração + validação.
        
        Args:
            file_path: Caminho para o arquivo
            document_type: Tipo do documento (cnh, rg)
            auto_detect: Se deve detectar automaticamente o tipo
            
        Returns:
            Documento processado com dados extraídos e validação
        """
        start_time = time.time()
        
        try:
            # Validação inicial do arquivo
            if not FileProcessor.is_supported_file(file_path):
                raise ValueError("Tipo de arquivo não suportado")
            
            if not FileProcessor.validate_file_size(file_path):
                raise ValueError("Arquivo muito grande")
            
            # Análise do documento
            analysis = DocumentAnalyzer.analyze_document_content(file_path)
            
            # Determina tipo do documento
            if auto_detect and not document_type:
                document_type = analysis.get("inferred_document_type")
            
            document_type = document_type
            
            st.info(f"Processando documento: {analysis['filename']} (Tipo: {document_type})")
            
            # Extração de dados com Mindee
            extraction_start = time.time()
            extracted_data = self.mindee_service.extract_document_data(file_path, document_type)
            extraction_time = time.time() - extraction_start
            
            # Converte para modelo de dados
            document_data = self._convert_to_document_data(extracted_data, analysis, extraction_time)
            
            # Validação com Groq
            validation_start = time.time()
            validation_result = self.validation_service.validate_document(extracted_data, document_type)
            validation_time = time.time() - validation_start
            
            # Converte para modelo de dados
            validation_data = self._convert_to_validation_result(validation_result, validation_time)
            
            # Cria documento processado
            processed_doc = ProcessedDocument(
                document_data=document_data,
                validation_result=validation_data,
                file_name=analysis['filename'],
                file_size=analysis['file_size']
            )
            
            total_time = time.time() - start_time
            st.success(f"Processamento concluído em {total_time:.2f}s")
            
            return processed_doc
            
        except Exception as e:
            st.error(f"Erro no processamento: {str(e)}")
            raise
    
    def _convert_to_document_data(
        self, 
        extracted_data: Dict[str, Any], 
        analysis: Dict[str, Any],
        processing_time: float
    ) -> DocumentData:
        """Converte dados extraídos para modelo DocumentData."""
        
        # Converte campos extraídos
        extracted_fields = {}
        raw_fields = extracted_data.get("extracted_fields", {})
        
        for field_name, field_value in raw_fields.items():
            if isinstance(field_value, dict):
                extracted_fields[field_name] = ExtractedField(
                    value=field_value.get("value"),
                    confidence=field_value.get("confidence", 0.0),
                    bounding_box=field_value.get("bounding_box")
                )
            else:
                extracted_fields[field_name] = ExtractedField(
                    value=str(field_value) if field_value else None,
                    confidence=0.5  # Confiança padrão
                )
        
        return DocumentData(
            document_type=DocumentType(extracted_data.get("document_type")),
            extracted_fields=extracted_fields,
            raw_response=extracted_data.get("raw_response", {}),
            confidence=extracted_data.get("confidence", 0.0),
            processing_time=processing_time
        )
    
    def _convert_to_validation_result(
        self, 
        validation_data: Dict[str, Any],
        validation_time: float
    ) -> ValidationResult:
        """Converte resultado de validação para modelo ValidationResult."""
        
        return ValidationResult(
            is_valid=validation_data.get("is_valid", False),
            confidence=validation_data.get("confidence", 0.0),
            errors=validation_data.get("errors", []),
            warnings=validation_data.get("warnings", []),
            analysis=validation_data.get("analysis", ""),
            recommendations=validation_data.get("recommendations", []),
            validation_time=validation_time,
            cnh_specific_errors=validation_data.get("cnh_specific_errors", []),
            cnh_specific_warnings=validation_data.get("cnh_specific_warnings", []),
            rg_specific_errors=validation_data.get("rg_specific_errors", []),
            rg_specific_warnings=validation_data.get("rg_specific_warnings", [])
        )
    
    def get_processing_summary(self, processed_doc: ProcessedDocument) -> Dict[str, Any]:
        """Retorna resumo do processamento."""
        
        return {
            "file_name": processed_doc.file_name,
            "document_type": processed_doc.document_data.document_type.value,
            "overall_status": processed_doc.overall_status.value,
            "extraction_confidence": processed_doc.document_data.confidence,
            "validation_confidence": processed_doc.validation_result.confidence,
            "total_errors": len(processed_doc.all_errors),
            "total_warnings": len(processed_doc.all_warnings),
            "processing_time": processed_doc.document_data.processing_time,
            "validation_time": processed_doc.validation_result.validation_time,
            "file_size_mb": processed_doc.file_size / (1024 * 1024) if processed_doc.file_size else 0
        }
    
    def get_detailed_analysis(self, processed_doc: ProcessedDocument) -> Dict[str, Any]:
        """Retorna análise detalhada do documento."""
        
        return {
            "extracted_fields": {
                name: {
                    "value": field.value,
                    "confidence": field.confidence
                }
                for name, field in processed_doc.document_data.extracted_fields.items()
            },
            "validation_details": {
                "is_valid": processed_doc.validation_result.is_valid,
                "confidence": processed_doc.validation_result.confidence,
                "errors": processed_doc.all_errors,
                "warnings": processed_doc.all_warnings,
                "analysis": processed_doc.validation_result.analysis,
                "recommendations": processed_doc.validation_result.recommendations
            },
            "performance_metrics": {
                "extraction_time": processed_doc.document_data.processing_time,
                "validation_time": processed_doc.validation_result.validation_time,
                "total_time": (processed_doc.document_data.processing_time or 0) + 
                            (processed_doc.validation_result.validation_time or 0)
            }
        } 