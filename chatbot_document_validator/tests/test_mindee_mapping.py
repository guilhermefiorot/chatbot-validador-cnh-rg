"""
Testes para verificar o mapeamento correto dos campos do Mindee.
"""
import pytest
import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from chatbot_document_validator.services.mindee_service import MindeeService
from chatbot_document_validator.examples.sample_data import (
    SAMPLE_CNH_RESPONSE, 
    SAMPLE_RG_RESPONSE,
    EXPECTED_CNH_FIELDS,
    EXPECTED_RG_FIELDS
)


class TestMindeeMapping:
    """Testes para mapeamento de campos do Mindee."""
    
    def setup_method(self):
        """Configuração para cada teste."""
        self.mindee_service = MindeeService("fake_api_key")
    
    def test_cnh_field_mapping(self):
        """Testa mapeamento de campos da CNH."""
        # Simula dados extraídos da CNH
        extracted_data = {
            "raw_response": SAMPLE_CNH_RESPONSE,
            "document_type": "cnh",
            "extracted_fields": {},
            "confidence": 0.95
        }
        
        # Chama o método de extração
        fields = self.mindee_service._extract_cnh_fields(SAMPLE_CNH_RESPONSE)
        
        # Verifica se os campos foram mapeados corretamente
        assert fields["nome"] == "GUILHERME FIRME FIOROT"
        assert fields["cpf"] == "188.433.327-32"
        assert fields["categoria"] == "B"
        assert fields["data_emissao"] == "2025-01-27"
        assert fields["data_validade"] == "2035-01-27"
        assert fields["data_nascimento"] == "2001-05-02"
        assert fields["numero_registro"] == "07450883117"
        assert fields["orgao_emissor"] == "SPTC ES"
        assert fields["data_primeira_habilitacao"] == "2020-08-07"
    
    def test_rg_field_mapping(self):
        """Testa mapeamento de campos do RG."""
        # Chama o método de extração
        fields = self.mindee_service._extract_rg_fields(SAMPLE_RG_RESPONSE)
        
        # Verifica se os campos foram mapeados corretamente
        assert fields["nome"] == "GUILHERME FIRME FIOROT"
        assert fields["numero_rg"] == "4.021.923 - ES"
        assert fields["cpf"] == "188.433.327-32"
        assert fields["data_emissao"] == "2020-02-07"
        assert fields["nome_pai"] == "LEONARDO VICENTINI FIOROT"
        assert fields["nome_mae"] == "GISELE FIRME BIANCHI FIOROT"
        assert fields["data_nascimento"] == "2001-02-05"
        assert fields["local_nascimento"] == "VITORIA - ES"
        assert fields["orgao_emissor"] == "ES"
    
    def test_field_value_extraction(self):
        """Testa extração de valores de campos."""
        # Testa campo com valor
        field_data = {"value": "test_value"}
        result = self.mindee_service._get_field_value({"test_field": field_data}, "test_field")
        assert result == "test_value"
        
        # Testa campo sem valor
        result = self.mindee_service._get_field_value({"test_field": {}}, "test_field")
        assert result is None
        
        # Testa campo inexistente
        result = self.mindee_service._get_field_value({}, "inexistent_field")
        assert result is None
        
        # Testa valor direto (não dicionário)
        result = self.mindee_service._get_field_value({"test_field": "direct_value"}, "test_field")
        assert result == "direct_value"
    
    def test_empty_response_handling(self):
        """Testa tratamento de respostas vazias."""
        empty_response = {"fields": {}}
        
        # CNH
        fields = self.mindee_service._extract_cnh_fields(empty_response)
        assert fields == {}
        
        # RG
        fields = self.mindee_service._extract_rg_fields(empty_response)
        assert fields == {}
    
    def test_malformed_response_handling(self):
        """Testa tratamento de respostas malformadas."""
        malformed_response = {"invalid_key": "invalid_value"}
        
        # CNH
        fields = self.mindee_service._extract_cnh_fields(malformed_response)
        assert fields == {}
        
        # RG
        fields = self.mindee_service._extract_rg_fields(malformed_response)
        assert fields == {}


class TestFieldValidation:
    """Testes para validação de campos específicos."""
    
    def setup_method(self):
        """Configuração para cada teste."""
        self.mindee_service = MindeeService("fake_api_key")
    
    def test_cnh_required_fields(self):
        """Testa se campos obrigatórios da CNH estão presentes."""
        fields = self.mindee_service._extract_cnh_fields(SAMPLE_CNH_RESPONSE)
        
        required_fields = ["nome", "cpf", "categoria", "data_emissao", "data_validade", "data_nascimento"]
        
        for field in required_fields:
            assert field in fields, f"Campo obrigatório '{field}' não encontrado"
            assert fields[field] is not None, f"Campo '{field}' está vazio"
    
    def test_rg_required_fields(self):
        """Testa se campos obrigatórios do RG estão presentes."""
        fields = self.mindee_service._extract_rg_fields(SAMPLE_RG_RESPONSE)
        
        required_fields = ["nome", "cpf", "numero_rg", "data_emissao", "data_nascimento"]
        
        for field in required_fields:
            assert field in fields, f"Campo obrigatório '{field}' não encontrado"
            assert fields[field] is not None, f"Campo '{field}' está vazio"
    
    def test_date_format_consistency(self):
        """Testa se as datas estão no formato correto."""
        cnh_fields = self.mindee_service._extract_cnh_fields(SAMPLE_CNH_RESPONSE)
        rg_fields = self.mindee_service._extract_rg_fields(SAMPLE_RG_RESPONSE)
        
        # Verifica formato YYYY-MM-DD
        date_fields = [
            cnh_fields["data_emissao"],
            cnh_fields["data_validade"],
            cnh_fields["data_nascimento"],
            cnh_fields["data_primeira_habilitacao"],
            rg_fields["data_emissao"],
            rg_fields["data_nascimento"]
        ]
        
        for date_str in date_fields:
            assert date_str is not None
            assert len(date_str) == 10  # YYYY-MM-DD
            assert date_str.count("-") == 2
            parts = date_str.split("-")
            assert len(parts) == 3
            assert len(parts[0]) == 4  # Ano
            assert len(parts[1]) == 2  # Mês
            assert len(parts[2]) == 2  # Dia


if __name__ == "__main__":
    pytest.main([__file__]) 