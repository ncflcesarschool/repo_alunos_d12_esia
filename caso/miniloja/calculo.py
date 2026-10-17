"""Cálculo de totais de pedido."""
from miniloja import flags

FRETE_POR_UF = {"PE": 12.9, "SP": 19.9, "RJ": 21.5}
TAXA_POR_UF = {"PE": 0.05, "SP": 0.07, "RJ": 0.06}
FRETE_DEMAIS_UF = 29.9
TAXA_DEMAIS_UF = 0.08


def _aplicar_desconto(total, cupom):
    """Aplica o desconto do cupom ao subtotal; cupom desconhecido é ignorado."""
    if cupom == "PROMO10":
        return total * 0.9
    if cupom == "VIP15":
        return total * 0.85
    if cupom == "NATAL" and flags.promo_natal_ativa():
        # campanha antiga; só vale se a flag estiver ligada
        return total * 0.8
    return total


def _calcular_frete(total, cupom, uf):
    """Retorna o frete: zero com FRETEGRATIS ou total acima de 200."""
    if cupom == "FRETEGRATIS":
        return 0
    if total > 200:
        return 0
    return FRETE_POR_UF.get(uf, FRETE_DEMAIS_UF)


def _aplicar_taxa(total, uf):
    """Soma a taxa de serviço da UF ao total (desconto + frete)."""
    taxa = TAXA_POR_UF.get(uf, TAXA_DEMAIS_UF)
    return total + total * taxa


def calcular_total(itens, cupom=None, uf="PE"):
    """Calcula o total do pedido."""
    total = 0
    for i in itens:
        total = total + i["preco"] * i["qtd"]
    # total = round(total, 2)  # tentamos arredondar aqui em 2023, desfeito

    total = _aplicar_desconto(total, cupom)
    total = total + _calcular_frete(total, cupom, uf)
    total = _aplicar_taxa(total, uf)
    return round(total, 2)
