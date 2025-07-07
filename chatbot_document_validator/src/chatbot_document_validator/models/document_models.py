"""
Modelos de dados para documentos e validação.
"""
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum


class DocumentType(str, Enum):
    """Tipos de documento suportados."""
    CNH = "cnh"
    RG = "rg"


class ValidationStatus(str, Enum):
    """Status de validação."""
    VALID = "valid"
    INVALID = "invalid"
    WARNING = "warning"
    ERROR = "error"


class ExtractedField(BaseModel):
    """Campo extraído de um documento."""
    value: Optional[str] = None
    confidence: float = 0.0
    bounding_box: Optional[Dict[str, float]] = None


class DocumentData(BaseModel):
    """Dados extraídos de um documento."""
    document_type: DocumentType
    extracted_fields: Dict[str, ExtractedField] = Field(default_factory=dict)
    raw_response: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = 0.0
    processing_time: Optional[float] = None


class ValidationResult(BaseModel):
    """Resultado da validação de um documento."""
    is_valid: bool
    confidence: float = 0.0
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    analysis: str = ""
    recommendations: List[str] = Field(default_factory=list)
    validation_time: Optional[float] = None
    
    # Campos específicos por tipo de documento
    cnh_specific_errors: List[str] = Field(default_factory=list)
    cnh_specific_warnings: List[str] = Field(default_factory=list)
    rg_specific_errors: List[str] = Field(default_factory=list)
    rg_specific_warnings: List[str] = Field(default_factory=list)


class ProcessedDocument(BaseModel):
    """Documento processado com dados extraídos e validação."""
    document_data: DocumentData
    validation_result: ValidationResult
    file_name: str
    file_size: Optional[int] = None
    upload_time: datetime = Field(default_factory=datetime.now)
    
    @property
    def overall_status(self) -> ValidationStatus:
        """Retorna o status geral do documento."""
        if not self.validation_result.is_valid:
            return ValidationStatus.INVALID
        elif self.validation_result.warnings or self.validation_result.cnh_specific_warnings or self.validation_result.rg_specific_warnings:
            return ValidationStatus.WARNING
        else:
            return ValidationStatus.VALID
    
    @property
    def all_errors(self) -> List[str]:
        """Retorna todos os erros encontrados."""
        errors = self.validation_result.errors.copy()
        errors.extend(self.validation_result.cnh_specific_errors)
        errors.extend(self.validation_result.rg_specific_errors)
        return errors
    
    @property
    def all_warnings(self) -> List[str]:
        """Retorna todos os avisos encontrados."""
        warnings = self.validation_result.warnings.copy()
        warnings.extend(self.validation_result.cnh_specific_warnings)
        warnings.extend(self.validation_result.rg_specific_warnings)
        return warnings


class ChatMessage(BaseModel):
    """Mensagem do chat."""
    role: str  # "user" ou "assistant"
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)


class ChatSession(BaseModel):
    """Sessão de chat."""
    session_id: str
    messages: List[ChatMessage] = Field(default_factory=list)
    processed_documents: List[ProcessedDocument] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now) 