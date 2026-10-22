"""Formatação de valores."""


def formatar_moeda(valor):
    """Formata o valor como moeda."""
    s = f"{valor:,.2f}"
    s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    return "R$ " + s
