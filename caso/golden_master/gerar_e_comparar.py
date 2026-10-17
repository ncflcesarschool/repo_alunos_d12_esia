"""Golden master de miniloja.calculo.calcular_total.

--gerar    grava as saídas ATUAIS do código como saida_golden (rodar antes do refactor);
           recusa sobrescrever um golden existente sem --forcar.
(padrão)   recalcula, preenche saida_obtida/igual e sai com 1 se houver diferença.
Comparação por igualdade exata (==), sem tolerância.
"""
import argparse
import itertools
import json
import os
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
GOLDEN = AQUI / "comportamento_original.json"
CARRINHOS = AQUI.parent / "dados" / "carrinhos.json"

# (rótulo, cupom, flag NATAL ligada)
CUPONS = [
    ("sem_cupom", None, False),
    ("PROMO10", "PROMO10", False),
    ("VIP15", "VIP15", False),
    ("FRETEGRATIS", "FRETEGRATIS", False),
    ("NATAL_flag_on", "NATAL", True),
    ("NATAL_flag_off", "NATAL", False),
    ("INVALIDO", "INVALIDO", False),
]
UFS = ["PE", "SP", "RJ", "AM"]


def carrinhos():
    base = json.loads(CARRINHOS.read_text(encoding="utf-8"))["carrinhos"]
    extras = {
        "vazio": [],
        "item_barato": [{"sku": "MEIA-01", "preco": 10.0, "qtd": 1}],
        "borda_200": [{"sku": "KIT-200", "preco": 200.0, "qtd": 1}],
    }
    return {**base, **extras}


def calcular(codigo, itens, cupom, uf, flag_natal):
    sys.path.insert(0, str(codigo))
    try:
        from miniloja.calculo import calcular_total
    finally:
        sys.path.remove(str(codigo))
    anterior = os.environ.get("MINILOJA_PROMO_NATAL")
    os.environ["MINILOJA_PROMO_NATAL"] = "1" if flag_natal else "0"
    try:
        return calcular_total(itens, cupom, uf)
    finally:
        if anterior is None:
            del os.environ["MINILOJA_PROMO_NATAL"]
        else:
            os.environ["MINILOJA_PROMO_NATAL"] = anterior


def gerar(codigo, forcar=False):
    if GOLDEN.exists() and not forcar:
        print(f"{GOLDEN.name} já existe e guarda o comportamento original; "
              "use --forcar para sobrescrever.", file=sys.stderr)
        return 2
    casos = []
    combos = itertools.product(carrinhos().items(), CUPONS, UFS)
    for (nome, itens), (rotulo, cupom, flag), uf in combos:
        casos.append({
            "id": f"{nome}|{rotulo}|{uf}",
            "itens": itens,
            "cupom": cupom,
            "uf": uf,
            "flag_natal": flag,
            "saida_golden": calcular(codigo, itens, cupom, uf, flag),
        })
    dados = {
        "funcao": "miniloja.calculo.calcular_total",
        "comparacao": "igualdade exata (==), sem tolerância",
        "casos": casos,
    }
    GOLDEN.write_text(json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(casos)} casos gravados em {GOLDEN}")
    return 0


def comparar(codigo):
    dados = json.loads(GOLDEN.read_text(encoding="utf-8"))
    diferentes = []
    for c in dados["casos"]:
        obtida = calcular(codigo, c["itens"], c["cupom"], c["uf"], c["flag_natal"])
        c["saida_obtida"] = obtida
        c["igual"] = obtida == c["saida_golden"]
        if not c["igual"]:
            diferentes.append(c)
    total = len(dados["casos"])
    dados["resumo"] = {"total": total, "iguais": total - len(diferentes), "diferentes": len(diferentes)}
    GOLDEN.write_text(json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for c in diferentes:
        print(f"DIFERE {c['id']}: golden={c['saida_golden']!r} obtida={c['saida_obtida']!r}")
    print(f"{dados['resumo']['iguais']}/{total} iguais")
    return 1 if diferentes else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--codigo", default=str(AQUI.parent), help="pasta com o pacote miniloja")
    ap.add_argument("--gerar", action="store_true")
    ap.add_argument("--forcar", action="store_true", help="permite --gerar sobrescrever o golden existente")
    args = ap.parse_args()
    codigo = Path(args.codigo).resolve()
    sys.exit(gerar(codigo, args.forcar) if args.gerar else comparar(codigo))
