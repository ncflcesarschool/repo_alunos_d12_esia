"""Simulação de descontos (usada pelo relatório de marketing)."""

PERCENTUAIS = {"PROMO10": 10, "VIP15": 15}


def aplicar_desconto(total, cupom):
    """Aplica o desconto do cupom ao total."""
    if cupom is None:
        return total
    pct = PERCENTUAIS.get(cupom, 0)
    return total - (total * pct / 100)
