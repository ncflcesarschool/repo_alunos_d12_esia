#!/usr/bin/env python3
"""Mutação manual do calculo.py refatorado, rodando só os testes da AV2.

Uso, na raiz do pacote: python -B avaliacoes/av2/trabalho/mutacao_av2.py
Opção --sem-diferencial roda só os testes de contrato (mostra o que o golden master adiciona).
"""
import os
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ALVO = AQUI / "miniloja" / "calculo.py"
TESTES = ["test_calculo_contrato.py"]
if "--sem-diferencial" not in sys.argv:
    TESTES.append("test_comportamento_preservado.py")

MUTACOES = [
    ('"PROMO10": 0.9', '"PROMO10": 0.91', "PROMO10: 10% -> 9%"),
    ('"VIP15": 0.85', '"VIP15": 0.86', "VIP15: 15% -> 14%"),
    ("FATOR_NATAL = 0.8", "FATOR_NATAL = 0.79", "NATAL: 20% -> 21%"),
    ("if flags.promo_natal_ativa() else", "if not flags.promo_natal_ativa() else", "NATAL ignora a flag (inverte)"),
    ('cupom == "NATAL"', 'cupom == "NATALX"', "NATAL deixa de ser reconhecido"),
    ("subtotal_com_desconto > LIMITE", "subtotal_com_desconto >= LIMITE", "frete grátis: > vira >= (alinha ao contrato)"),
    ("LIMITE_FRETE_GRATIS = 200", "LIMITE_FRETE_GRATIS = 201", "limite do frete grátis 200 -> 201"),
    ("subtotal_com_desconto > LIMITE", "subtotal_com_desconto - 1 > LIMITE", "limite deslocado em R$ 1"),
    ('_frete(com_desconto, cupom, uf)', '_frete(_subtotal(itens), cupom, uf)', "frete decidido pelo subtotal sem desconto"),
    ('cupom == "FRETEGRATIS" or ', "", "FRETEGRATIS deixa de zerar o frete"),
    ('"PE": 12.9', '"PE": 13.9', "frete PE"),
    ('"SP": 19.9', '"SP": 20.9', "frete SP"),
    ('"RJ": 21.5}\nFRETE_DEMAIS', '"RJ": 22.5}\nFRETE_DEMAIS', "frete RJ"),
    ("FRETE_DEMAIS_UFS = 29.9", "FRETE_DEMAIS_UFS = 30.9", "frete demais UFs"),
    ('"PE": 0.05', '"PE": 0.06', "taxa PE"),
    ('"SP": 0.07', '"SP": 0.08', "taxa SP"),
    ('"RJ": 0.06}\nTAXA_DEMAIS', '"RJ": 0.07}\nTAXA_DEMAIS', "taxa RJ"),
    ("TAXA_DEMAIS_UFS = 0.08", "TAXA_DEMAIS_UFS = 0.09", "taxa demais UFs"),
    ('item["preco"] * item["qtd"]', 'item["preco"] + item["qtd"]', "subtotal: * vira +"),
    ('item["preco"] * item["qtd"]', 'item["preco"]', "subtotal ignora a quantidade"),
    ("total = total + item", "total = item", "subtotal só do último item"),
    ("return round(base + _taxa_servico(base, uf), 2)", "return round(base + _taxa_servico(base, uf), 3)", "arredondamento em 3 casas"),
    ("return round(base + _taxa_servico(base, uf), 2)", "return round(base, 2)", "sem taxa de serviço"),
    ("base = com_desconto + _frete", "base = _frete", "frete substitui o subtotal"),
    ("base = com_desconto + _frete(com_desconto, cupom, uf)\n    return round(base + _taxa_servico(base, uf), 2)",
     "base = com_desconto + _frete(com_desconto, cupom, uf)\n    return round(base + _taxa_servico(com_desconto, uf), 2)", "taxa só sobre o desconto (sem frete)"),
    ("    return subtotal\n\n\ndef _frete", "    return subtotal * 1.0\n\n\ndef _frete", "equivalente: multiplicar por 1.0"),
    ("    if cupom in FATOR_POR_CUPOM:", "    if cupom in FATOR_POR_CUPOM and True:", "equivalente: and True"),
    ("    total = 0\n    for item in itens:\n        total = total + item[\"preco\"] * item[\"qtd\"]\n    return total",
     "    return sum(i[\"preco\"] * i[\"qtd\"] for i in itens)", "refatoração errada: laço trocado por sum() (último bit)"),
    ("return 0\n    return FRETE_POR_UF", "return 0.0\n    return FRETE_POR_UF", "equivalente: frete 0 -> 0.0"),
]


def passa():
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    for t in TESTES:
        r = subprocess.run([sys.executable, "-B", str(AQUI / t)], capture_output=True, text=True, env=env)
        if r.returncode != 0:
            return False
    return True


def main():
    if not passa():
        sys.exit("A suíte já falha sem mutação.")
    original = ALVO.read_text(encoding="utf-8")
    mortos, vivos = 0, []
    for velho, novo, desc in MUTACOES:
        assert original.count(velho) >= 1, f"trecho não encontrado: {velho!r}"
        try:
            ALVO.write_text(original.replace(velho, novo, 1), encoding="utf-8")
            if passa():
                vivos.append(desc)
                print(f"SOBREVIVEU  {desc}")
            else:
                mortos += 1
                print(f"morto       {desc}")
        finally:
            ALVO.write_text(original, encoding="utf-8")
    print(f"\n{mortos} mortos, {len(vivos)} sobreviventes de {len(MUTACOES)}")
    for d in vivos:
        print("  -", d)
    sys.exit(0)


if __name__ == "__main__":
    main()
