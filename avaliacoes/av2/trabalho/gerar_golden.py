"""Gera golden_master.json a partir do código ORIGINAL (caso/miniloja/calculo.py).

Uso (na raiz do pacote): python -B avaliacoes/av2/trabalho/gerar_golden.py
Só rode de novo se o código original mudar; o arquivo gerado é a referência da refatoração.
"""
import importlib.util
import itertools
import json
import os
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ORIGINAL = AQUI.parent.parent.parent / "caso" / "miniloja" / "calculo.py"

PRECOS = [0.0, 0.01, 1.2, 1.25, 9.99, 19.99, 33.33, 49.9, 50.0, 80.0, 99.99, 100.0,
          111.11, 133.34, 199.99, 200.0, 222.23, 250.0, 1234.56]
CARRINHOS = [[]] + [[{"preco": p, "qtd": 1}] for p in PRECOS] \
    + [[{"preco": p, "qtd": q}] for p in (19.99, 33.33, 50.0, 100.0) for q in (2, 3, 7)] \
    + [[{"preco": 80.0, "qtd": 1}, {"preco": 50.0, "qtd": 1}],
       [{"preco": 0.1, "qtd": 3}, {"preco": 0.2, "qtd": 3}, {"preco": 0.7, "qtd": 1}],
       [{"preco": 19.99, "qtd": 3}, {"preco": 33.33, "qtd": 2}, {"preco": 7.77, "qtd": 5}],
       # achado por busca aleatória: com sum() (Python 3.12) o total difere em R$ 0,01 do laço
       [{"preco": 84.47, "qtd": 1}, {"preco": 55.21, "qtd": 4}, {"preco": 105.74, "qtd": 1},
        {"preco": 94.1, "qtd": 4}, {"preco": 14.36, "qtd": 3}, {"preco": 49.24, "qtd": 3}]]
CUPONS = [None, "PROMO10", "VIP15", "NATAL", "FRETEGRATIS", "CUPOMFALSO", "promo10", ""]
UFS = ["PE", "SP", "RJ", "XX", "MG"]
NATAL = ["0", "1"]


def carregar_original():
    spec = importlib.util.spec_from_file_location("calculo_original", ORIGINAL)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def cenarios():
    for itens, cupom, uf, natal in itertools.product(CARRINHOS, CUPONS, UFS, NATAL):
        yield {"itens": itens, "cupom": cupom, "uf": uf, "natal": natal}


def executar(calcular_total, c):
    os.environ["MINILOJA_PROMO_NATAL"] = c["natal"]
    try:
        return calcular_total(c["itens"], c["cupom"], c["uf"])
    finally:
        os.environ.pop("MINILOJA_PROMO_NATAL", None)


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(AQUI))
    original = carregar_original()
    saida = [dict(c, total=repr(executar(original.calcular_total, c))) for c in cenarios()]
    (AQUI / "golden_master.json").write_text(json.dumps(saida, ensure_ascii=False, indent=0), encoding="utf-8")
    print(len(saida), "cenários gravados")
