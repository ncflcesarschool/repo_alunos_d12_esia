"""Relatórios gerenciais."""
from miniloja.descontos import aplicar_desconto


def _fmt(v):
    return "R$ " + str(round(v, 2)).replace(".", ",")


def resumo_vendas(pedidos):
    total = sum(p["total"] for p in pedidos)
    return {"quantidade": len(pedidos), "total": total, "total_fmt": _fmt(total)}


def simular_desconto(total, cupom):
    return _fmt(aplicar_desconto(total, cupom))
