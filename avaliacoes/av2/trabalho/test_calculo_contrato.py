"""Testes de calcular_total derivados do contrato (caso/regras.md, R1), não do código.

Cada esperado foi calculado à mão em decimal, na ordem de R1.6 (desconto, frete, taxa),
com arredondamento meio para cima. Uso, na raiz do pacote:
    python -B avaliacoes/av2/trabalho/test_calculo_contrato.py
"""
import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from miniloja.calculo import calcular_total  # noqa: E402


def item(preco, qtd=1):
    return {"preco": preco, "qtd": qtd}


class ComNatal:
    def __init__(self, valor):
        self.valor = valor

    def __enter__(self):
        self.antes = os.environ.get("MINILOJA_PROMO_NATAL")
        if self.valor is None:
            os.environ.pop("MINILOJA_PROMO_NATAL", None)
        else:
            os.environ["MINILOJA_PROMO_NATAL"] = self.valor

    def __exit__(self, *_):
        if self.antes is None:
            os.environ.pop("MINILOJA_PROMO_NATAL", None)
        else:
            os.environ["MINILOJA_PROMO_NATAL"] = self.antes


class TestContratoR1(unittest.TestCase):
    def test_r1_1_subtotal_soma_preco_vezes_quantidade(self):
        # 20*2 + 10*3 = 70; PE: 70 + 12,90 = 82,90; x1,05 = 87,045 -> 87,05
        self.assertEqual(calcular_total([item(20.0, 2), item(10.0, 3)], None, "PE"), 87.05)

    def test_r1_2_promo10_desconta_dez_por_cento(self):
        # 100 -> 90; SP: 90 + 19,90 = 109,90; x1,07 = 117,593 -> 117,59
        self.assertEqual(calcular_total([item(50.0, 2)], "PROMO10", "SP"), 117.59)

    def test_r1_2_vip15_desconta_quinze_por_cento(self):
        # 250 -> 212,50 (>= 200, frete grátis); RJ: x1,06 = 225,25
        self.assertEqual(calcular_total([item(250.0)], "VIP15", "RJ"), 225.25)

    def test_r1_2_natal_com_campanha_ativa_desconta_vinte_por_cento(self):
        # 100 -> 80; PE: 80 + 12,90 = 92,90; x1,05 = 97,545 -> 97,55
        with ComNatal("1"):
            self.assertEqual(calcular_total([item(100.0)], "NATAL", "PE"), 97.55)

    def test_r1_2_natal_sem_campanha_nao_desconta(self):
        # sem flag: 100 + 12,90 = 112,90; x1,05 = 118,545 -> 118,55
        for valor in (None, "0"):
            with ComNatal(valor):
                self.assertEqual(calcular_total([item(100.0)], "NATAL", "PE"), 118.55)

    def test_r1_2_fretegratis_zera_o_frete_sem_alterar_o_valor(self):
        # 100, frete 0; UF fora da tabela: x1,08 = 108,00
        self.assertEqual(calcular_total([item(100.0)], "FRETEGRATIS", "XX"), 108.0)

    def test_r1_2_cupom_desconhecido_e_ignorado(self):
        # 10 + 21,50 = 31,50; RJ: x1,06 = 33,39
        self.assertEqual(calcular_total([item(10.0)], "CUPOMFALSO", "RJ"), 33.39)

    def test_r1_3_frete_decide_pelo_subtotal_com_desconto(self):
        # 210 bruto (>200) mas 189 com PROMO10: paga frete. 189 + 12,90 = 201,90; x1,05 = 211,995 -> 212,00
        self.assertEqual(calcular_total([item(210.0)], "PROMO10", "PE"), 212.0)

    def test_r1_3_logo_abaixo_do_limite_paga_frete(self):
        # 199,99 + 12,90 = 212,89; x1,05 = 223,5345 -> 223,53
        self.assertEqual(calcular_total([item(199.99)], None, "PE"), 223.53)

    def test_r1_3_logo_acima_do_limite_nao_paga_frete(self):
        # 200,40 > 200: frete 0; PE: x1,05 = 210,42
        self.assertEqual(calcular_total([item(200.4)], None, "PE"), 210.42)

    def test_r1_3_acima_do_limite_nao_paga_frete(self):
        # 250, frete 0; x1,05 = 262,50
        self.assertEqual(calcular_total([item(250.0)], None, "PE"), 262.5)

    def test_r1_3_frete_por_uf(self):
        # item de 10,10 (evita empates de arredondamento): PE 23,00*1,05=24,15 | SP 30,00*1,07=32,10
        # RJ 31,60*1,06=33,496->33,50 | XX/MG 40,00*1,08=43,20
        esperado = {"PE": 24.15, "SP": 32.1, "RJ": 33.5, "XX": 43.2, "MG": 43.2}
        for uf, valor in esperado.items():
            with self.subTest(uf=uf):
                self.assertEqual(calcular_total([item(10.1)], None, uf), valor)

    def test_r1_4_taxa_incide_sobre_desconto_mais_frete(self):
        # FRETEGRATIS em 250 (frete 0), taxa por UF: PE 262,50 | SP 267,50 | RJ 265,00 | XX 270,00
        esperado = {"PE": 262.5, "SP": 267.5, "RJ": 265.0, "XX": 270.0}
        for uf, valor in esperado.items():
            with self.subTest(uf=uf):
                self.assertEqual(calcular_total([item(250.0)], "FRETEGRATIS", uf), valor)

    def test_r1_6_ordem_desconto_frete_taxa(self):
        # 33,33: PROMO10 -> 29,997; PE: + 12,90 = 42,897; x1,05 = 45,04185 -> 45,04
        self.assertEqual(calcular_total([item(33.33)], "PROMO10", "PE"), 45.04)

    # Divergências conhecidas do código atual (R1.3 e R1.5). Preservadas nesta refatoração;
    # `expectedFailure` registra o contrato correto sem esconder o desvio. Se alguém corrigir
    # o código, estes testes passam a "unexpected success" e devem perder a marca.
    @unittest.expectedFailure
    def test_r1_3_subtotal_exatamente_200_tem_frete_gratis(self):
        # 200,00 >= 200: frete 0; PE: x1,05 = 210,00
        self.assertEqual(calcular_total([item(200.0)], None, "PE"), 210.0)

    @unittest.expectedFailure
    def test_r1_5_arredondamento_meio_para_cima(self):
        # 1,25 + 21,50 = 22,75; RJ: x1,06 = 24,115 -> 24,12 (o código devolve 24,11)
        self.assertEqual(calcular_total([item(1.25)], None, "RJ"), 24.12)


if __name__ == "__main__":
    unittest.main()
