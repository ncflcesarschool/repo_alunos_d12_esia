# Registro individual — AV2

**Limite: duas páginas de análise + anexo técnico curto.** Estudante: Caroline Lima — Data: 21/10/2026 — Caminho: B (MiniLoja)

**Escopo (seis campos):** objetivo: refatorar `calcular_total` em etapas nomeadas (subtotal, desconto, frete, taxa) sem mudar nenhuma saída; pode tocar: `calculo.py` na cópia `avaliacoes/av2/trabalho/miniloja/` e os arquivos novos de teste dessa pasta; não pode tocar: `caso/`, `testes/`, `regras.md`, a assinatura e os outros módulos; invariantes: resultado idêntico ao original para toda entrada, cupom desconhecido ignorado, `NATAL` só com a flag, ordem desconto → frete → taxa; pronto quando: golden master e diferencial passam, testes de contrato passam e só sobrevivem mutantes equivalentes; pare e pergunte se: for preciso mudar algum resultado (mesmo para seguir o contrato) ou tocar outro módulo.

**Plano do agente: o que cortei ou corrigi:** (1) cortei corrigir `>=` no frete grátis e o arredondamento meio para cima: é mudança de comportamento, fica para outra mudança; (2) cortei editar `caso/` no lugar: usei cópia, e o original serve de referência; (3) corrigi o uso de `sum()` no subtotal: no Python 3.12 ele muda o último bit; mantive o laço.

**Comportamento preservado:** método: golden master gravado do original + diferencial ao vivo contra o original, comparando o `repr` do float (igualdade exata); entradas: 2.880 cenários (24 carrinhos com fronteiras como 199,99 e 200,00 × 8 cupons × 5 UFs × flag de Natal ligada/desligada); resultado: `python -B avaliacoes/av2/trabalho/test_comportamento_preservado.py` → `Ran 2 tests ... OK`.

| Teste (regra do contrato) | Como provei que falharia | Resultado |
| --- | --- | --- |
| Descontos e `NATAL` com/sem flag (R1.2) | Mutantes: percentuais ±1 ponto, flag invertida, `NATAL` não reconhecido | 5 de 5 mortos |
| Frete grátis, limite e frete por UF (R1.3) | Mutantes: limite 200→201, `>` → `>=`, frete sobre subtotal sem desconto, valores por UF | 9 de 9 mortos |
| Taxa e ordem das etapas (R1.4, R1.6) | Mutantes: taxa +1 ponto, taxa sem frete, sem taxa | 7 de 7 mortos |
| Subtotal (R1.1) | Mutantes: `*` → `+`, ignora quantidade | 3 de 3 mortos |
| Golden master + diferencial | Refatoração errada: laço trocado por `sum()` (total 1036,95 vira 1036,94) | Morto depois de incluir o carrinho que o expõe |

Mutação: `python -B avaliacoes/av2/trabalho/mutacao_av2.py` → 26 mortos, 3 sobreviventes de 29.

**Mutantes sobreviventes e tratamento:** os 3 são equivalentes (não mudam nenhuma saída): `subtotal * 1.0`, `... and True` na condição do cupom e frete `0` → `0.0`. O mutante `sum()` sobreviveu na primeira rodada, porque minha grade não tinha carrinho que o distinguisse; achei um por busca aleatória e regerei o golden.

**Documentação ou ADR:** a docstring de `calculo.py` registra a ordem de R1.6, o motivo do laço no lugar de `sum()` e as divergências abaixo. ADR: *Contexto:* o código usa `> 200` (R1.3 pede `>= 200`: R$ 200,00 em PE dá 223,55, o correto é 210,00) e `round()` (R1.5 pede meio para cima: 1,25 em RJ dá 24,11, o correto é 24,12). *Decisão:* o contrato vence, mas a correção fica fora desta refatoração; os dois casos ficam como `expectedFailure`. *Consequências:* o desvio fica documentado sem quebrar a suíte, e a marca deve sair quando o código for corrigido. *Alternativa:* corrigir já, em mudança separada, com `Decimal` e golden regerado.

**O que a IA errou (o quê, onde, como detectei):** (1) `r1_3_frete_por_uf` usou item de R$ 10,00, que cai num empate de arredondamento (24,045); o teste falhou ao rodar e troquei para R$ 10,10; (2) `mutacao_av2.py` nasceu com âncora inexistente (`AssertionError` na primeira execução); (3) a grade inicial do golden não detectava o mutante `sum()`, que a mutação revelou. *(Estudante: confirme ou substitua pelos erros que você observou.)*

**Limite da verificação e condição para rever:** o golden prova igualdade só nas 2.880 entradas (não cobre preços negativos nem `qtd` zero). Os esperados foram calculados por mim em decimal; um erro de leitura do contrato se repetiria nos testes. R2 a R4 não foram tocados. Rever se o Python mudar de versão, se `caso/` mudar (regerar o golden) ou se R1.3/R1.5 forem corrigidos.

**Procedência/IA:** Claude Code, modelo Claude Sonnet 5.5; tarefa delegada e contexto: refatorar `calcular_total`, gerar o golden master, escrever os testes e a mutação e rascunhar este registro; trecho aproveitado: `calculo.py` refatorado, os arquivos de `avaliacoes/av2/trabalho/` e o rascunho; minha verificação/intervenção: ___. O raciocínio e a decisão registrados são meus.

**Anexo:** diff: `trabalho/miniloja/calculo.py`, 74 → 59 linhas (+47/−62). Novos: `test_calculo_contrato.py` (16 testes, 2 `expectedFailure`), `test_comportamento_preservado.py`, `gerar_golden.py`, `golden_master.json`, `mutacao_av2.py`. Para repetir, rode `test_calculo_contrato.py`, `test_comportamento_preservado.py` e `mutacao_av2.py` (na raiz, com `python -B avaliacoes/av2/trabalho/<arquivo>`).
```python
def test_r1_3_frete_decide_pelo_subtotal_com_desconto(self):
    # 210 bruto, 189 com PROMO10: paga frete. 189 + 12,90 = 201,90; x1,05 = 211,995 -> 212,00
    self.assertEqual(calcular_total([item(210.0)], "PROMO10", "PE"), 212.0)
```
**Revisão:** [x] escopo; [x] comportamento; [x] testes com prova; [x] documentação; [x] erros da IA; [x] limite.
