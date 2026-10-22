"""Gateway de pagamento fictício."""


class GatewayFake:
    def __init__(self):
        self.cobrancas = []

    def cobrar(self, valor, token):
        if token == "recusado":
            return {"status": "recusado", "id": None}
        self.cobrancas.append((valor, token))
        return {"status": "aprovado", "id": f"ch_{len(self.cobrancas)}"}
