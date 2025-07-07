"""
Serviço de validação de documentos usando Groq LLM.
"""
import json
from typing import Dict, Any, List, Optional
from groq import Groq
import streamlit as st
from datetime import datetime, date
import re
import validate_docbr

class DocumentValidationService:
    """Serviço para validação de documentos usando Groq LLM."""
    
    def __init__(self, groq_api_key: str):
        self.client = Groq(api_key=groq_api_key)
        self.model = "llama-3.3-70b-versatile"
    
    def preprocess_cnh_data(self, fields: Dict[str, Any]) -> Dict[str, Any]:
        """
        Pré-processa os dados da CNH para facilitar a validação
        """
        processed = fields.copy()
        
        # Converter datas para objetos datetime e calcular informações úteis
        date_fields = ['data_nascimento', 'data_emissao', 'data_validade', 'data_primeira_habilitacao']
        dates = {}
        
        for field in date_fields:
            if processed.get(field):
                try:
                    # Tentar formato ISO primeiro
                    dates[field] = datetime.strptime(processed[field], '%Y-%m-%d')
                except ValueError:
                    try:
                        # Tentar formato brasileiro
                        dates[field] = datetime.strptime(processed[field], '%d/%m/%Y')
                    except ValueError:
                        dates[field] = None
        
        # Calcular idade atual
        if dates.get('data_nascimento'):
            idade_atual = (datetime.now() - dates['data_nascimento']).days // 365
            processed['idade_atual'] = idade_atual
        
        # Calcular idade na emissão
        if dates.get('data_nascimento') and dates.get('data_emissao'):
            idade_emissao = (dates['data_emissao'] - dates['data_nascimento']).days // 365
            processed['idade_na_emissao'] = idade_emissao
        
        # Verificar se CNH está vencida
        if dates.get('data_validade'):
            dias_vencimento = (dates['data_validade'] - datetime.now()).days
            processed['dias_para_vencimento'] = dias_vencimento
            processed['esta_vencida'] = dias_vencimento < 0
        
        # Calcular período de validade
        if dates.get('data_emissao') and dates.get('data_validade'):
            periodo_validade = (dates['data_validade'] - dates['data_emissao']).days // 365
            processed['periodo_validade_anos'] = periodo_validade
        
        # Adicionar comparações explícitas de datas
        comparacoes = {}
        if dates.get('data_nascimento') and dates.get('data_emissao'):
            comparacoes['nascimento_anterior_emissao'] = dates['data_nascimento'] < dates['data_emissao']
        
        if dates.get('data_emissao') and dates.get('data_validade'):
            comparacoes['emissao_anterior_validade'] = dates['data_emissao'] < dates['data_validade']
        
        if dates.get('data_primeira_habilitacao') and dates.get('data_emissao'):
            comparacoes['primeira_hab_anterior_emissao'] = dates['data_primeira_habilitacao'] <= dates['data_emissao']
        
        processed['comparacoes_datas'] = comparacoes
        
        return processed
    
    def preprocess_rg_data(self, fields: Dict[str, Any]) -> Dict[str, Any]:
        """
        Pré-processa os dados do RG para facilitar a validação
        """
        processed = fields.copy()
        
        # Converter datas para objetos datetime
        date_fields = ['data_nascimento', 'data_emissao']
        dates = {}
        
        for field in date_fields:
            if processed.get(field):
                try:
                    # Tentar formato ISO primeiro
                    dates[field] = datetime.strptime(processed[field], '%Y-%m-%d')
                except ValueError:
                    try:
                        # Tentar formato brasileiro
                        dates[field] = datetime.strptime(processed[field], '%d/%m/%Y')
                    except ValueError:
                        dates[field] = None
        
        # Calcular idade atual
        if dates.get('data_nascimento'):
            idade_atual = (datetime.now() - dates['data_nascimento']).days // 365
            processed['idade_atual'] = idade_atual
        
        # Calcular idade na emissão
        if dates.get('data_nascimento') and dates.get('data_emissao'):
            idade_emissao = (dates['data_emissao'] - dates['data_nascimento']).days // 365
            processed['idade_na_emissao'] = idade_emissao
        
        # Adicionar comparações explícitas de datas
        comparacoes = {}
        if dates.get('data_nascimento') and dates.get('data_emissao'):
            comparacoes['nascimento_anterior_emissao'] = dates['data_nascimento'] < dates['data_emissao']
        
        processed['comparacoes_datas'] = comparacoes
        
        return processed
    
    def validate_document(self, document_data: Dict[str, Any], document_type: str) -> Dict[str, Any]:
        """
        Valida um documento usando Groq LLM.
        
        Args:
            document_data: Dados extraídos do documento
            document_type: Tipo do documento (cnh, rg)
            
        Returns:
            Resultado da validação
        """
        try:
            if document_type == "cnh":
                return self._validate_cnh(document_data)
            elif document_type == "rg":
                return self._validate_rg(document_data)
                
        except Exception as e:
            st.error(f"Erro na validação: {str(e)}")
            return {
                "is_valid": False,
                "errors": [f"Erro na validação: {str(e)}"],
                "warnings": [],
                "confidence": 0.0
            }
    
    def _validate_cnh(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """Valida CNH usando Groq com pré-processamento."""
        
        # Prepara os dados para o prompt
        extracted_fields = document_data.get("extracted_fields", {})
        processed_data = self.preprocess_cnh_data(extracted_fields)
        # Cria o prompt específico para CNH com pré-processamento
        prompt = self._create_enhanced_cnh_prompt(processed_data)
        
        # Chama o Groq
        response = self._call_groq(prompt)
        
        # Processa a resposta
        validation_result = self._parse_validation_response(response)
        
        # Adiciona validações específicas de CNH
        validation_result.update(self._validate_cnh_specific_fields(extracted_fields))
        
        return validation_result
    
    def _validate_rg(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """Valida RG usando Groq com pré-processamento."""
        
        # Prepara os dados para o prompt
        extracted_fields = document_data.get("extracted_fields", {})
        processed_data = self.preprocess_rg_data(extracted_fields)
        # Cria o prompt específico para RG com pré-processamento
        prompt = self._create_enhanced_rg_prompt(processed_data)
        
        # Chama o Groq
        response = self._call_groq(prompt)
        
        # Processa a resposta
        validation_result = self._parse_validation_response(response)
        
        # Adiciona validações específicas de RG
        validation_result.update(self._validate_rg_specific_fields(extracted_fields))
        
        return validation_result

    def _create_enhanced_cnh_prompt(self, fields: Dict[str, Any]) -> str:
        """
        Cria prompt melhorado com dados pré-processados para CNH
        """
        
        return f"""
Você é um especialista em validação de documentos brasileiros. Analise os dados PRÉ-PROCESSADOS de uma CNH.

DADOS PRÉ-PROCESSADOS:
{json.dumps(fields, indent=2, ensure_ascii=False)}

INSTRUÇÕES DE VALIDAÇÃO:

1. **Use os dados pré-processados** - As comparações de datas já foram calculadas
2. **Campos obrigatórios**: nome, cpf, numero_registro, todas as datas
3. **Validações automáticas já calculadas**:
   - idade_atual: idade da pessoa hoje
   - idade_na_emissao: idade quando a CNH foi emitida (deve ser ≥ 18)
   - dias_para_vencimento: negativo se vencida
   - periodo_validade_anos: deve ser 3-5 anos
   - comparacoes_datas: validações lógicas já calculadas

4. **Regras de validação**:
   - comparacoes_datas.nascimento_anterior_emissao deve ser true
   - comparacoes_datas.emissao_anterior_validade deve ser true  
   - comparacoes_datas.primeira_hab_anterior_emissao deve ser true
   - idade_na_emissao deve ser ≥ 18
   - periodo_validade_anos deve ser 3, 4 ou 5
   - CPF deve ter formato XXX.XXX.XXX-XX (11 dígitos)
   - numero_registro deve ter 11 dígitos
   - categoria pode estar vazia (erro de extração)

5. **NÃO faça comparações manuais de datas** - use os campos pré-processados

Responda em JSON:
{{
    "is_valid": true/false,
    "confidence": 0.0-1.0,
    "errors": ["erros críticos"],
    "warnings": ["avisos"],
    "analysis": "análise detalhada",
    "recommendations": ["recomendações"]
}}

Seja preciso e use APENAS os dados pré-processados para validação.
"""

    def _create_enhanced_rg_prompt(self, fields: Dict[str, Any]) -> str:
        """
        Cria prompt melhorado com dados pré-processados para RG
        """
        processed_data = self.preprocess_rg_data(fields)
        
        return f"""
Você é um especialista em validação de documentos brasileiros. Analise os dados PRÉ-PROCESSADOS de um RG.

DADOS PRÉ-PROCESSADOS:
{json.dumps(processed_data, indent=2, ensure_ascii=False)}

INSTRUÇÕES DE VALIDAÇÃO:

1. **Use os dados pré-processados** - As comparações de datas já foram calculadas
2. **Campos obrigatórios**: nome, numero_rg, data_nascimento, data_emissao
3. **Validações automáticas já calculadas**:
   - idade_atual: idade da pessoa hoje
   - idade_na_emissao: idade quando o RG foi emitido
   - comparacoes_datas: validações lógicas já calculadas

4. **Regras de validação**:
   - comparacoes_datas.nascimento_anterior_emissao deve ser true
   - idade_na_emissao deve ser ≥ 0 (pode ser emitido para recém-nascidos)
   - CPF deve ter formato XXX.XXX.XXX-XX (se presente)
   - numero_rg deve ter formato válido para o estado
   - Órgão emissor deve ser válido (SSP, DETRAN, etc.)

5. **Coerência geográfica**:
   - Local de nascimento deve corresponder ao órgão emissor
   - Estado emissor deve ser UF válida

6. **NÃO faça comparações manuais de datas** - use os campos pré-processados

Responda em JSON:
{{
    "is_valid": true/false,
    "confidence": 0.0-1.0,
    "errors": ["erros críticos"],
    "warnings": ["avisos"],
    "analysis": "análise detalhada",
    "recommendations": ["recomendações"]
}}

Seja preciso e use APENAS os dados pré-processados para validação.
"""

    def _call_groq(self, prompt: str) -> str:
        """Chama a API do Groq."""
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um especialista em validação de documentos brasileiros. Sempre responda em JSON válido."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,  # Temperatura baixa para mais consistência
                max_tokens=2000
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            st.error(f"Erro na chamada do Groq: {str(e)}")
            raise
    
    def _parse_validation_response(self, response: str) -> Dict[str, Any]:
        """Processa a resposta do Groq."""
        
        try:
            # Tenta extrair JSON da resposta
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                result = json.loads(json_str)
                
                # Garante que todos os campos necessários estão presentes
                return {
                    "is_valid": result.get("is_valid", False),
                    "confidence": result.get("confidence", 0.0),
                    "errors": result.get("errors", []),
                    "warnings": result.get("warnings", []),
                    "analysis": result.get("analysis", ""),
                    "recommendations": result.get("recommendations", [])
                }
            else:
                # Se não conseguir extrair JSON, cria resposta padrão
                return {
                    "is_valid": False,
                    "confidence": 0.0,
                    "errors": ["Não foi possível processar a resposta do validador"],
                    "warnings": [],
                    "analysis": response,
                    "recommendations": ["Verificar manualmente os dados extraídos"]
                }
                
        except json.JSONDecodeError as e:
            st.warning(f"Erro ao processar resposta JSON: {str(e)}")
            return {
                "is_valid": False,
                "confidence": 0.0,
                "errors": [f"Erro no formato da resposta: {str(e)}"],
                "warnings": [],
                "analysis": response,
                "recommendations": ["Verificar manualmente os dados extraídos"]
            }
    
    def _validate_cnh_specific_fields(self, fields: Dict[str, Any]) -> Dict[str, Any]:
        """Validações específicas para CNH."""
        errors = []
        warnings = []
        
        # Validação de CPF
        cpf = fields.get("cpf")
        if cpf and not self._is_valid_cpf(cpf):
            errors.append("CPF inválido")
        
        # Validação de número de registro
        numero_registro = fields.get("numero_registro")
        if numero_registro:
            # Remove caracteres não numéricos para validação
            numero_clean = re.sub(r'[^0-9]', '', str(numero_registro))
            if not re.fullmatch(r"\d{11}", numero_clean):
                warnings.append("Número de registro não segue o padrão de CNH (11 dígitos)")
        
        # Validação de categoria
        categoria = fields.get("categoria")
        if categoria and not self._is_valid_cnh_category(categoria):
            warnings.append("Categoria de CNH pode estar incorreta")
        
        # Validação de data de validade
        data_validade = fields.get("data_validade")
        if data_validade:
            if not self._is_valid_date(data_validade):
                errors.append("Data de validade inválida")
            elif self._is_expired(data_validade):
                warnings.append("CNH está vencida")
        
        return {
            "cnh_specific_errors": errors,
            "cnh_specific_warnings": warnings
        }

    def _validate_rg_specific_fields(self, fields: Dict[str, Any]) -> Dict[str, Any]:
        """Validações específicas para RG."""
        errors = []
        warnings = []
        
        # Validação de CPF
        cpf = fields.get("cpf")
        if cpf and not self._is_valid_cpf(cpf):
            errors.append("CPF inválido")
        
        # Validação de número do RG
        numero_rg = fields.get("numero_rg")
        if numero_rg and not self._is_valid_rg_format(numero_rg):
            warnings.append("Formato de RG pode estar incorreto")
        
        # Validação de nomes dos pais (mais flexível)
        nome_pai = fields.get("nome_pai", "").strip()
        nome_mae = fields.get("nome_mae", "").strip()
        
        # Verifica se pelo menos um dos nomes está presente
        if not nome_pai and not nome_mae:
            warnings.append("Nomes dos pais estão ausentes")
        elif not nome_pai:
            warnings.append("Nome do pai está ausente")
        elif not nome_mae:
            warnings.append("Nome da mãe está ausente")
        
        # Validação de data de nascimento
        data_nascimento = fields.get("data_nascimento")
        if data_nascimento and not self._is_valid_date(data_nascimento):
            errors.append("Data de nascimento inválida")
        
        return {
            "rg_specific_errors": errors,
            "rg_specific_warnings": warnings
        }

    def _is_valid_cpf(self, cpf: str) -> bool:
        """Valida CPF usando validate_docbr."""
        if not cpf:
            return False
        
        try:
            # Remove caracteres não numéricos
            cpf_clean = re.sub(r'[^0-9]', '', str(cpf))
            
            # Verifica se tem 11 dígitos
            if len(cpf_clean) != 11:
                return False
                
            # Verifica se não são todos os dígitos iguais
            if cpf_clean == cpf_clean[0] * 11:
                return False
                
            return validate_docbr.CPF().validate(cpf_clean)
        except:
            return False

    def _is_valid_date(self, date_str: str) -> bool:
        """Valida formato de data (formato yyyy-mm-dd)."""
        if not date_str:
            return False
            
        try:
            date_str = date_str.strip()
            parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
            
            # Verifica se a data é razoável (não muito no futuro ou passado)
            current_year = datetime.now().year
            if 1900 <= parsed_date.year <= current_year + 50:
                return True
            return False
        except:
            return False

    def _is_expired(self, date_str: str) -> bool:
        """Verifica se a data está vencida (formato yyyy-mm-dd)."""
        if not date_str:
            return False
            
        try:
            date_str = date_str.strip()
            doc_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            return doc_date < date.today()
        except:
            return False

    def _is_valid_cnh_category(self, category: str) -> bool:
        """Valida categoria de CNH."""
        if not category:
            return False
            
        # Categorias válidas de CNH no Brasil
        valid_categories = [
            "A", "B", "C", "D", "E", 
            "AB", "AC", "AD", "AE", 
            "ACC"
        ]
        
        # Limpa e converte para maiúscula
        category_clean = category.strip().upper()
        return category_clean in valid_categories

    def _is_valid_rg_format(self, rg: str) -> bool:
        """Valida formato básico de RG."""
        if not rg:
            return False
            
        try:
            # Remove caracteres não alfanuméricos
            rg_clean = re.sub(r'[^a-zA-Z0-9]', '', str(rg))
            
            # RG deve ter pelo menos 7 caracteres e no máximo 10
            if len(rg_clean) < 7 or len(rg_clean) > 10:
                return False
                
            # Verifica se não são todos os dígitos iguais
            if rg_clean.isdigit() and rg_clean == rg_clean[0] * len(rg_clean):
                return False
                
            return True
        except:
            return False