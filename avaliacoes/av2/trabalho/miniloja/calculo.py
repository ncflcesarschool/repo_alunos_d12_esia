"""Cálculo de totais de pedido (contrato: caso/regras.md, R1).

Ordem de R1.6: subtotal -> desconto -> frete -> taxa de serviço -> arredondamento.
Cada etapa é uma função pequena para poder ser testada isoladamente.

Refatoração (AV2): a estrutura mudou, o comportamento não. As operações de ponto
flutuante foram mantidas na mesma ordem e com os mesmos literais, porque a igualdade
com a versão anterior é exata (ver avaliacoes/av2/trabalho/test_comportamento_preservado.py).
Por isso `_subtotal` usa laço e não `sum()`: no Python 3.12, `sum()` de floats usa soma
compensada e pode diferir no último bit do laço original.

Divergências conhecidas em relação ao contrato, preservadas de propósito nesta mudança
(estão fora do escopo; ver ADR em avaliacoes/av2/registro.md):
  - R1.3: o frete grátis deveria valer com subtotal >= 200; aqui vale só com > 200.
  - R1.5: o arredondamento deveria ser meio para cima; `round()` usa meio para par
    sobre a representação binária do float.
"""
from miniloja import flags

LIMITE_FRETE_GRATIS = 200
FRETE_POR_UF = {"PE": 12.9, "SP": 19.9, "RJ": 21.5}
FRETE_DEMAIS_UFS = 29.9
TAXA_POR_UF = {"PE": 0.05, "SP": 0.07, "RJ": 0.06}
TAXA_DEMAIS_UFS = 0.08
FATOR_POR_CUPOM = {"PROMO10": 0.9, "VIP15": 0.85}
FATOR_NATAL = 0.8


def _subtotal(itens):
    total = 0
    for item in itens:
        total = total + item["preco"] * item["qtd"]
    return total


def _aplicar_desconto(subtotal, cupom):
    """Cupom desconhecido é ignorado (R1.2); NATAL só vale com a campanha ativa."""
    if cupom == "NATAL":
        return subtotal * FATOR_NATAL if flags.promo_natal_ativa() else subtotal
    if cupom in FATOR_POR_CUPOM:
        return subtotal * FATOR_POR_CUPOM[cupom]
    return subtotal


def _frete(subtotal_com_desconto, cupom, uf):
    if cupom == "FRETEGRATIS" or subtotal_com_desconto > LIMITE_FRETE_GRATIS:
        return 0
    return FRETE_POR_UF.get(uf, FRETE_DEMAIS_UFS)


def _taxa_servico(base, uf):
    return base * TAXA_POR_UF.get(uf, TAXA_DEMAIS_UFS)


def calcular_total(itens, cupom=None, uf="PE"):
    """Total do pedido em reais, com duas casas (R1)."""
    com_desconto = _aplicar_desconto(_subtotal(itens), cupom)
    base = com_desconto + _frete(com_desconto, cupom, uf)
    return round(base + _taxa_servico(base, uf), 2)
