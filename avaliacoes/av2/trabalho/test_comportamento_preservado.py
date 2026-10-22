"""Comportamento preservado: refatoração == original, com igualdade exata (repr do float).

Dois métodos: (1) golden master gravado do original; (2) diferencial ao vivo contra
caso/miniloja/calculo.py. Uso, na raiz do pacote:
    python -B avaliacoes/av2/trabalho/test_comportamento_preservado.py
"""
import json
import sys
import unittest
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import gerar_golden  # noqa: E402
from miniloja.calculo import calcular_total  # noqa: E402


class TestComportamentoPreservado(unittest.TestCase):
    def test_golden_master_igualdade_exata(self):
        golden = json.loads((AQUI / "golden_master.json").read_text(encoding="utf-8"))
        self.assertGreater(len(golden), 2000)
        diferentes = [g for g in golden if repr(gerar_golden.executar(calcular_total, g)) != g["total"]]
        self.assertEqual(diferentes[:3], [])

    def test_diferencial_contra_o_original(self):
        original = gerar_golden.carregar_original().calcular_total
        diferentes = [c for c in gerar_golden.cenarios()
                      if repr(gerar_golden.executar(calcular_total, c)) != repr(gerar_golden.executar(original, c))]
        self.assertEqual(diferentes[:3], [])


if __name__ == "__main__":
    unittest.main()
