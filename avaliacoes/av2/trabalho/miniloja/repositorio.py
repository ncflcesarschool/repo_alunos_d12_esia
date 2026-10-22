"""Repositório de pedidos em memória."""


class RepositorioPedidos:
    def __init__(self):
        self._pedidos = {}
        self._seq = 0

    def salvar(self, pedido):
        self._seq += 1
        pedido = dict(pedido, id=self._seq)
        self._pedidos[self._seq] = pedido
        return pedido

    def obter(self, pedido_id):
        return self._pedidos.get(pedido_id)

    def todos(self):
        return list(self._pedidos.values())
