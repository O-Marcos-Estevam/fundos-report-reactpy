"""
Testes unitários para models
"""

import pytest
from src.models.fundo import FundoData


def test_fundo_data_creation():
    """Testa criação de FundoData"""
    fundo = FundoData(
        nome="Fundo Teste",
        tipo="Multimercado",
        cnpj="12.345.678/0001-99",
        pl=1000000.0,
        cotistas=100,
        data_cadastro="01/01/2024"
    )

    assert fundo.nome == "Fundo Teste"
    assert fundo.tipo == "Multimercado"
    assert fundo.pl == 1000000.0


def test_fundo_data_propriedades_calculadas():
    """Testa propriedades calculadas"""
    fundo = FundoData(
        nome="Fundo Teste",
        tipo="Multimercado",
        cnpj="12.345.678/0001-99",
        pl=1000000.0,
        cotistas=100,
        data_cadastro="01/01/2024"
    )

    # Adicionar testes para propriedades calculadas quando implementadas
    assert fundo.nome is not None
