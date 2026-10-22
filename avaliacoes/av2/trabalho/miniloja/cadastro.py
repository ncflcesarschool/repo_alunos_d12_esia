"""Cadastro de clientes."""

_CLIENTES = []


def cadastrar_cliente(payload):
    """Cadastra um cliente."""
    if not payload.get("nome"):
        return 400, {"erro": "payload inválido"}
    if not payload.get("email"):
        return 400, {"erro": "payload inválido"}
    cliente = dict(payload, id=len(_CLIENTES) + 1)
    _CLIENTES.append(cliente)
    return 201, cliente


def limpar():
    _CLIENTES.clear()
