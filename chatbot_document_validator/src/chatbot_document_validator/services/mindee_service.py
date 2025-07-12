"""
Serviço para integração com a API do Mindee para extração de dados de documentos.
"""
import json
import time
import requests
from pathlib import Path
from typing import Dict, Any, Optional
import streamlit as st



class MindeeService:
    """Serviço para processamento de documentos usando a API do Mindee."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {"Authorization": api_key}
        
        # Model IDs para diferentes tipos de documento
        self.model_ids = {
            "cnh": "6ac2f847-2eb9-434e-a2bc-8926d5777c5a",
            "rg": "b8250a82-3ca4-412c-9bf7-35a113c91af9",
        }
    
    def send_file_with_polling(
        self,
        file_path: str,
        document_type: str,
        max_retries: int = 30,
        polling_interval: int = 2,
    ) -> Dict[str, Any]:
        """
        Envia arquivo para o Mindee e aguarda o processamento.
        
        Args:
            file_path: Caminho para o arquivo
            document_type: Tipo do documento (cnh, rg)
            max_retries: Número máximo de tentativas de polling
            polling_interval: Intervalo entre tentativas em segundos
            
        Returns:
            Dados extraídos do documento
        """
        upload_file = Path(file_path)
        model_id = self.model_ids.get(document_type)
        
        form_data = {"model_id": model_id, "rag": False}
        
        try:
            with upload_file.open("rb") as fh:
                files = {"file": (upload_file.name, fh)}
                st.info(f"Enviando arquivo: {upload_file.name}")
                
                response = requests.post(
                    url="https://api-v2.mindee.net/v2/inferences/enqueue",
                    files=files,
                    data=form_data,
                    headers=self.headers,
                )
            
            response.raise_for_status()
            job_data = response.json().get("job")
            polling_url = job_data.get("polling_url")
            
            # Aguarda antes de começar o polling
            time.sleep(3)
            
            # Polling para verificar conclusão
            with st.spinner("Processando documento..."):
                for attempt in range(max_retries):
                    st.info(f"Verificando status... (tentativa {attempt + 1}/{max_retries})")
                    
                    poll_response = requests.get(
                        polling_url, 
                        headers=self.headers, 
                        allow_redirects=False
                    )
                    poll_data = poll_response.json()
                    job_status = poll_data.get("job", {}).get("status")
                    
                    if poll_response.status_code == 302 or job_status == "Processed":
                        result_url = poll_data.get("job", {}).get("result_url")
                        st.success("Documento processado com sucesso!")
                        
                        result_response = requests.get(result_url, headers=self.headers)
                        result_data = result_response.json()
                        print(result_data)
                        return result_data
                    
                    # Ainda processando, aguarda antes da próxima tentativa
                    time.sleep(polling_interval)
            
            # Se esgotou todas as tentativas
            raise TimeoutError(f"Timeout após {max_retries} tentativas")
            
        except requests.exceptions.RequestException as e:
            st.error(f"Erro na comunicação com Mindee: {str(e)}")
            raise
        except Exception as e:
            st.error(f"Erro inesperado: {str(e)}")
            raise
    
    def extract_document_data(self, file_path: str, document_type: str) -> Dict[str, Any]:
        """
        Extrai dados do documento usando o Mindee.
        
        Args:
            file_path: Caminho para o arquivo
            document_type: Tipo do documento
            
        Returns:
            Dados extraídos e estruturados
        """
        raw_data = self.send_file_with_polling(file_path, document_type)
        # Estrutura os dados extraídos
        extracted_data = {
            "raw_response": raw_data,
            "document_type": document_type,
            "extracted_fields": {},
            "confidence": 0.73
        }
        
        # Extrai campos específicos baseado no tipo de documento
        if document_type == "cnh":
            extracted_data.update(self._extract_cnh_fields(raw_data))
        elif document_type == "rg":
            extracted_data.update(self._extract_rg_fields(raw_data))
        
        return extracted_data
    
    def _extract_cnh_fields(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai campos específicos da CNH."""
        fields = {}
        try:
            # Corrigir caminho para os campos extraídos
            fields_data = raw_data.get('inference', {}).get('result', {}).get('fields', {})
            fields.update({
                "nome": self._get_field_value(fields_data, "name"),
                "cpf": self._get_field_value(fields_data, "cpf"),
                "categoria": self._get_field_value(fields_data, "category"),
                "data_emissao": self._get_field_value(fields_data, "issue_date"),
                "data_validade": self._get_field_value(fields_data, "expiry_date"),
                "data_nascimento": self._get_field_value(fields_data, "date_of_birth"),
                "numero_registro": self._get_field_value(fields_data, "license_number"),
                "orgao_emissor": self._get_field_value(fields_data, "issuing_authority"),
                "data_primeira_habilitacao": self._get_field_value(fields_data, "first_habilitation_date")
            })
        except Exception as e:
            st.warning(f"Erro ao extrair campos da CNH: {str(e)}")
        return {"extracted_fields": fields}
    
    def _extract_rg_fields(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai campos específicos do RG."""
        fields = {}
        try:
            # Corrigir caminho para os campos extraídos
            fields_data = raw_data.get('inference', {}).get('result', {}).get('fields', {})
            fields.update({
                "nome": self._get_field_value(fields_data, "name"),
                "numero_rg": self._get_field_value(fields_data, "rg_number"),
                "cpf": self._get_field_value(fields_data, "cpf_number"),
                "data_emissao": self._get_field_value(fields_data, "issue_date"),
                "nome_pai": self._get_field_value(fields_data, "fathers_name"),
                "nome_mae": self._get_field_value(fields_data, "mothers_name"),
                "data_nascimento": self._get_field_value(fields_data, "date_of_birth"),
                "local_nascimento": self._get_field_value(fields_data, "place_of_birth"),
                "orgao_emissor": self._get_field_value(fields_data, "issuing_authority")
            })
        except Exception as e:
            st.warning(f"Erro ao extrair campos do RG: {str(e)}")
        return {"extracted_fields": fields}
    
    def _get_field_value(self, predictions: Dict[str, Any], field_name: str) -> Optional[str]:
        """Extrai valor de um campo específico das predições."""
        try:
            field_data = predictions.get(field_name, {})
            if isinstance(field_data, dict):
                return field_data.get("value")
            return None 
        except Exception as e:
            st.warning(f"Erro ao extrair campo {field_name}: {str(e)}")
            return None
