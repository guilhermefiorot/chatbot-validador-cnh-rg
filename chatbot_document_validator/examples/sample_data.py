#!/usr/bin/env python3
"""
Dados de exemplo baseados na estrutura real do Mindee.
Use estes dados para testar a validação sem precisar de arquivos reais.
"""

# Exemplo de resposta do Mindee para CNH
SAMPLE_CNH_RESPONSE = {
    "fields": {
        "cpf": {
            "value": "188.433.327-32"
        },
        "name": {
            "value": "GUILHERME FIRME FIOROT"
        },
        "category": {
            "value": "B"
        },
        "issue_date": {
            "value": "2025-01-27"
        },
        "expiry_date": {
            "value": "2035-01-27"
        },
        "date_of_birth": {
            "value": "2001-05-02"
        },
        "license_number": {
            "value": "07450883117"
        },
        "issuing_authority": {
            "value": "SPTC ES"
        },
        "first_habilitation_date": {
            "value": "2020-08-07"
        }
    },
    "options": None
}

# Exemplo de resposta do Mindee para RG
SAMPLE_RG_RESPONSE = {
    "fields": {
        "name": {
            "value": "GUILHERME FIRME FIOROT"
        },
        "rg_number": {
            "value": "4.021.923 - ES"
        },
        "cpf_number": {
            "value": "188.433.327-32"
        },
        "issue_date": {
            "value": "2020-02-07"
        },
        "fathers_name": {
            "value": "LEONARDO VICENTINI FIOROT"
        },
        "mothers_name": {
            "value": "GISELE FIRME BIANCHI FIOROT"
        },
        "date_of_birth": {
            "value": "2001-02-05"
        },
        "place_of_birth": {
            "value": "VITORIA - ES"
        },
        "issuing_authority": {
            "value": "ES"
        }
    },
    "options": None
}

# Dados processados esperados para CNH
EXPECTED_CNH_FIELDS = {
    "nome": "GUILHERME FIRME FIOROT",
    "cpf": "188.433.327-32",
    "categoria": "B",
    "data_emissao": "2025-01-27",
    "data_validade": "2035-01-27",
    "data_nascimento": "2001-05-02",
    "numero_registro": "07450883117",
    "orgao_emissor": "SPTC ES",
    "data_primeira_habilitacao": "2020-08-07"
}

# Dados processados esperados para RG
EXPECTED_RG_FIELDS = {
    "nome": "GUILHERME FIRME FIOROT",
    "numero_rg": "4.021.923 - ES",
    "cpf": "188.433.327-32",
    "data_emissao": "2020-02-07",
    "nome_pai": "LEONARDO VICENTINI FIOROT",
    "nome_mae": "GISELE FIRME BIANCHI FIOROT",
    "data_nascimento": "2001-02-05",
    "local_nascimento": "VITORIA - ES",
    "orgao_emissor": "ES"
}

# Exemplo de CNH com problemas para teste de validação
SAMPLE_CNH_WITH_ISSUES = {
    "fields": {
        "cpf": {
            "value": "111.111.111-11"  # CPF inválido
        },
        "name": {
            "value": "JOAO SILVA"
        },
        "category": {
            "value": "X"  # Categoria inválida
        },
        "issue_date": {
            "value": "2030-01-27"  # Data futura
        },
        "expiry_date": {
            "value": "2020-01-27"  # Data vencida
        },
        "date_of_birth": {
            "value": "2005-05-02"  # Muito jovem para ter CNH
        },
        "license_number": {
            "value": "123"  # Número muito curto
        },
        "issuing_authority": {
            "value": "DETRAN SP"
        },
        "first_habilitation_date": {
            "value": "2030-08-07"  # Data futura
        }
    },
    "options": None
}

# Exemplo de RG com problemas para teste de validação
SAMPLE_RG_WITH_ISSUES = {
    "fields": {
        "name": {
            "value": "MARIA SANTOS"
        },
        "rg_number": {
            "value": "123"  # Número muito curto
        },
        "cpf_number": {
            "value": "222.222.222-22"  # CPF inválido
        },
        "issue_date": {
            "value": "2030-02-07"  # Data futura
        },
        "fathers_name": {
            "value": ""  # Nome do pai ausente
        },
        "mothers_name": {
            "value": "ANA SANTOS"
        },
        "date_of_birth": {
            "value": "2010-02-05"  # Muito jovem
        },
        "place_of_birth": {
            "value": "SAO PAULO - SP"  # Inconsistente com órgão emissor
        },
        "issuing_authority": {
            "value": "RJ"  # Órgão emissor diferente do local
        }
    },
    "options": None
}


def get_sample_data(document_type: str, with_issues: bool = False):
    """
    Retorna dados de exemplo para teste.
    
    Args:
        document_type: 'cnh' ou 'rg'
        with_issues: Se deve retornar dados com problemas para teste
    
    Returns:
        Dicionário com dados de exemplo
    """
    if document_type.lower() == "cnh":
        if with_issues:
            return SAMPLE_CNH_WITH_ISSUES
        return SAMPLE_CNH_RESPONSE
    elif document_type.lower() == "rg":
        if with_issues:
            return SAMPLE_RG_WITH_ISSUES
        return SAMPLE_RG_RESPONSE
    else:
        raise ValueError("document_type deve ser 'cnh' ou 'rg'")


def get_expected_fields(document_type: str):
    """
    Retorna os campos esperados após processamento.
    
    Args:
        document_type: 'cnh' ou 'rg'
    
    Returns:
        Dicionário com campos esperados
    """
    if document_type.lower() == "cnh":
        return EXPECTED_CNH_FIELDS
    elif document_type.lower() == "rg":
        return EXPECTED_RG_FIELDS
    else:
        raise ValueError("document_type deve ser 'cnh' ou 'rg'")


if __name__ == "__main__":
    # Exemplo de uso
    print("📄 Dados de exemplo para CNH:")
    print(get_sample_data("cnh"))
    
    print("\n📄 Dados de exemplo para RG:")
    print(get_sample_data("rg"))
    
    print("\n📄 CNH com problemas:")
    print(get_sample_data("cnh", with_issues=True))
    
    print("\n📄 RG com problemas:")
    print(get_sample_data("rg", with_issues=True)) 