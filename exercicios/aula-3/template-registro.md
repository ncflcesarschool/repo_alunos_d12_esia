# Registro individual — AV1.3

**Limite: uma página, incluindo evidências essenciais.** Estudante: Caroline Lima — Data: 21/10/2026
Origem: `caso/testes_existentes/` e `caso/regras.md` fictícios; modalidade: **execução própria** (cópia de trabalho de `caso/` e `testes/`; `caso/` original não foi alterado).

| Teste suspeito | Tipo de tautologia | Sabotagem que apliquei (ou raciocínio) | Continuou verde? |
| --- | --- | --- | --- |
| `test_calculo.test_cupom_natal_com_flag` | Sem asserção real (`assertIsNotNone`) | `calculo.py`: `total * 0.8` → `0.79` (NATAL 20%→21%) | Sim |
| `test_pedidos.test_fluxo_chama_colaboradores` | Super-mockado / afirma o mock (só `.called`) | `pedidos.py`: `total = calcular_total(...)` → `total = 0` | Sim |
| `test_calculo.test_cenarios_gravados` | Snapshot do próprio código | `calculo.py`: `total > 200` → `>= 200` (o que R1.3 manda) | Não: falhou, pois o snapshot grava `limite_200: 223.55`, que contradiz R1.3 (caso 1) |

| Mutante sobrevivente | Por que sobreviveu | Teste que o mataria (ou "equivalente", com justificativa) |
| --- | --- | --- |
| `frete = 21.5` → `22.5` (RJ) | Nenhum teste usa RJ sem `FRETEGRATIS` | `calcular_total([{"preco":40.0,"qtd":1}], None, "RJ") == 65.19`, pois (40+21,50)×1,06. Passa no original, falha no mutante |
| `disponivel < qtd` → `<=` (`estoque.py`) | Falta teste de borda | `Estoque({"BOLA-01":3}).reservar("BOLA-01",3,"p1")` retorna `True` e saldo 0. Passa no original, dá erro no mutante |
| (extra) `desconto_aplicado = True` → `False` | **Equivalente**: a variável só é lida em um `pass`; o retorno não muda | Nenhum |

| Caso derivado do contrato (entrada) | Esperado (cálculo à mão) | Observado no código | Decisão |
| --- | --- | --- | --- |
| 1. Fronteira R1.3: 2×R$ 100,00, sem cupom, PE | Subtotal 200,00 ≥ 200 → frete 0; 200×1,05 = **210,00** | **223,55** (cobra frete: usa `>`) | Código errado |
| 2. Arredondamento R1.5: 1×R$ 10,00, sem cupom, PE | (10+12,90)×1,05 = 24,045 → meio p/ cima = **24,05** | **24,04** (`round` de float) | Código errado |
| 3. Desconto cruza o limite: 1×R$ 210,00, `PROMO10`, SP | 210×0,9 = 189 (<200) → frete 19,90; (189+19,90)×1,07 = 223,523 → **223,52** | 223,52 | Código correto |

**ADR curto:** contexto: R1.3 diz "maior **ou igual** a R$ 200,00" e R1.5 "meio para cima", mas `calcular_total` usa `>` e `round()` de float, e o snapshot `limite_200 = 223.55` consagrou o erro; decisão: o código está errado e o contrato vale; corrigir para `>=` e arredondar com `Decimal`/`ROUND_HALF_UP`, e ajustar o snapshot para 210,00 só porque o esperado foi calculado à mão; consequências: totais na fronteira de R$ 200 e em meios-centavos mudam, e a correção exige bloco próprio com escopo e plano; alternativa descartada: mudar o contrato para `>` ou os testes para 223,55/24,04, o que faria o esperado vir do código.

**Trecho essencial de evidência:** `python -B testes/mutacao_manual.py` → `Mutantes: 31 | mortos: 23 | sobreviventes: 8 | escore: 74%`. Suíte existente com o mutante de frete RJ ou de estoque: `Ran 26 tests ... OK`. Novos testes dos casos 1 e 2 no código atual: `223.55 != 210.0` e `24.04 != 24.05`. **Limite do que a suíte garante e condição para rever a decisão:** mesmo com os novos testes, seguem vivos NATAL/VIP15 sem valor exato, e-mail obrigatório, `total_fmt` e relatório; R2.2 não é testado (o código reserva estoque antes do pagamento e não libera em pagamento recusado: indício, não verificado); R3 e R4 também não. 3 casos e 26 testes não provam correção geral. Rever o ADR se o dono do contrato confirmar que `>` ou o arredondamento atual são intencionais (nova versão de `regras.md`).

**Procedência/IA:** ferramenta e modelo visíveis: Claude Code, Claude Sonnet 5.5; tarefa delegada e contexto: rodar mutação e sabotagens na cópia, calcular esperados com `Decimal` e redigir o registro; trecho aproveitado: tabelas e ADR; minha verificação/intervenção: reexecutar os comandos e conferir à mão os três cálculos. O raciocínio e a decisão registrados são meus.

**Revisão:** [x] três testes; [x] dois mutantes; [x] três casos do contrato; [x] ADR; [x] até uma página.
