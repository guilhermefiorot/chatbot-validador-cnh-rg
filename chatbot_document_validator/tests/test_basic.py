"""
Testes básicos para o Chatbot Validador de Documentos.
"""
import pytest
import tempfile
import os
from unittest.mock import Mock, patch

from src.chatbot_document_validator.models.document_models import (
    DocumentType, 
    ValidationStatus, 
    ExtractedField,
    DocumentData,
    ValidationResult,
    ProcessedDocument
)
from src.chatbot_document_validator.utils.file_utils import FileProcessor


class TestDocumentModels:
    """Testes para os modelos de dados."""
    
    def test_document_type_enum(self):
        """Testa os tipos de documento."""
        assert DocumentType.CNH == "cnh"
        assert DocumentType.RG == "rg"
    
    def test_validation_status_enum(self):
        """Testa os status de validação."""
        assert ValidationStatus.VALID == "valid"
        assert ValidationStatus.INVALID == "invalid"
        assert ValidationStatus.WARNING == "warning"
        assert ValidationStatus.ERROR == "error"
    
    def test_extracted_field(self):
        """Testa o modelo ExtractedField."""
        field = ExtractedField(
            value="João Silva",
            confidence=0.95,
            bounding_box={"x": 100, "y": 200, "width": 300, "height": 50}
        )
        
        assert field.value == "João Silva"
        assert field.confidence == 0.95
        assert field.bounding_box["x"] == 100
    
    def test_document_data(self):
        """Testa o modelo DocumentData."""
        fields = {
            "nome": ExtractedField(value="João Silva", confidence=0.95),
            "cpf": ExtractedField(value="123.456.789-00", confidence=0.90)
        }
        
        doc_data = DocumentData(
            document_type=DocumentType.CNH,
            extracted_fields=fields,
            confidence=0.92,
            processing_time=2.5
        )
        
        assert doc_data.document_type == DocumentType.CNH
        assert len(doc_data.extracted_fields) == 2
        assert doc_data.confidence == 0.92
        assert doc_data.processing_time == 2.5
    
    def test_validation_result(self):
        """Testa o modelo ValidationResult."""
        result = ValidationResult(
            is_valid=True,
            confidence=0.85,
            errors=["CPF inválido"],
            warnings=["Data de nascimento pode estar incorreta"],
            analysis="Documento parece válido com algumas ressalvas",
            recommendations=["Verificar CPF manualmente"]
        )
        
        assert result.is_valid is True
        assert result.confidence == 0.85
        assert len(result.errors) == 1
        assert len(result.warnings) == 1
        assert "CPF inválido" in result.errors
        assert "Verificar CPF manualmente" in result.recommendations
    
    def test_processed_document(self):
        """Testa o modelo ProcessedDocument."""
        # Cria dados de teste
        fields = {
            "nome": ExtractedField(value="João Silva", confidence=0.95),
            "cpf": ExtractedField(value="123.456.789-00", confidence=0.90)
        }
        
        doc_data = DocumentData(
            document_type=DocumentType.CNH,
            extracted_fields=fields,
            confidence=0.92,
            processing_time=2.5
        )
        
        validation_result = ValidationResult(
            is_valid=True,
            confidence=0.85,
            errors=[],
            warnings=["Data de nascimento pode estar incorreta"],
            analysis="Documento válido",
            recommendations=[]
        )
        
        processed_doc = ProcessedDocument(
            document_data=doc_data,
            validation_result=validation_result,
            file_name="cnh_teste.pdf",
            file_size=1024000
        )
        
        assert processed_doc.file_name == "cnh_teste.pdf"
        assert processed_doc.file_size == 1024000
        assert processed_doc.overall_status == ValidationStatus.WARNING
        assert len(processed_doc.all_warnings) == 1
        assert len(processed_doc.all_errors) == 0


class TestFileProcessor:
    """Testes para o processador de arquivos."""
    
    def test_supported_extensions(self):
        """Testa extensões suportadas."""
        assert FileProcessor.is_supported_file("documento.pdf") is True
        assert FileProcessor.is_supported_file("imagem.jpg") is True
        assert FileProcessor.is_supported_file("arquivo.png") is True
        assert FileProcessor.is_supported_file("documento.txt") is False
        assert FileProcessor.is_supported_file("arquivo.doc") is False
    
    def test_image_file_detection(self):
        """Testa detecção de arquivos de imagem."""
        assert FileProcessor.is_image_file("imagem.jpg") is True
        assert FileProcessor.is_image_file("foto.png") is True
        assert FileProcessor.is_image_file("documento.pdf") is False
    
    def test_pdf_file_detection(self):
        """Testa detecção de arquivos PDF."""
        assert FileProcessor.is_pdf_file("documento.pdf") is True
        assert FileProcessor.is_pdf_file("imagem.jpg") is False
    
    def test_file_size_validation(self):
        """Testa validação de tamanho de arquivo."""
        # Cria arquivo temporário pequeno
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"test content")
            temp_path = f.name
        
        try:
            assert FileProcessor.validate_file_size(temp_path) is True
        finally:
            os.unlink(temp_path)
    
    def test_document_type_inference(self):
        """Testa inferência de tipo de documento."""
        assert FileProcessor.get_document_type_from_filename("cnh_joao.pdf") == "cnh"
        assert FileProcessor.get_document_type_from_filename("rg_maria.jpg") == "rg"
        assert FileProcessor.get_document_type_from_filename("carteira_habilitacao.png") == "cnh"


class TestMockServices:
    """Testes com serviços mockados."""
    
    @patch('src.chatbot_document_validator.services.mindee_service.MindeeService')
    def test_mindee_service_mock(self, mock_mindee):
        """Testa serviço Mindee mockado."""
        # Configura mock
        mock_instance = Mock()
        mock_instance.extract_document_data.return_value = {
            "document_type": "cnh",
            "extracted_fields": {
                "nome": {"value": "João Silva", "confidence": 0.95},
                "cpf": {"value": "123.456.789-00", "confidence": 0.90}
            },
            "confidence": 0.92
        }
        mock_mindee.return_value = mock_instance
        
        # Testa chamada
        service = mock_mindee("fake_api_key")
        result = service.extract_document_data("test.pdf", "cnh")
        
        assert result["document_type"] == "cnh"
        assert "nome" in result["extracted_fields"]
        assert result["confidence"] == 0.92
    
    @patch('src.chatbot_document_validator.services.validation_service.DocumentValidationService')
    def test_validation_service_mock(self, mock_validation):
        """Testa serviço de validação mockado."""
        # Configura mock
        mock_instance = Mock()
        mock_instance.validate_document.return_value = {
            "is_valid": True,
            "confidence": 0.85,
            "errors": [],
            "warnings": ["Data pode estar incorreta"],
            "analysis": "Documento válido",
            "recommendations": []
        }
        mock_validation.return_value = mock_instance
        
        # Testa chamada
        service = mock_validation("fake_api_key")
        result = service.validate_document({}, "cnh")
        
        assert result["is_valid"] is True
        assert result["confidence"] == 0.85
        assert len(result["warnings"]) == 1


if __name__ == "__main__":
    pytest.main([__file__]) 