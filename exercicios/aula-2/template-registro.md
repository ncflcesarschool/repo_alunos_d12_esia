# Registro individual — AV1.2

**Limite: uma página, incluindo evidências essenciais.** Estudante: Caroline Lima — Data: 17/10/2026
Origem: `caso/miniloja/calculo.py` fictício; modalidade: **execução própria** (a rodada 2 foi executada de fato; o plano do agente veio no escopo fornecido).

**Golden master:** 168 entradas (6 carrinhos × 7 variações de cupom × 4 UFs); gerado por `caso/golden_master/gerar_e_comparar.py --gerar` a partir da saída atual de `calcular_total`; comparação exata por igualdade `==` entre floats, sem tolerância. Resultado: 168/168 iguais, sem diferenças; uma mutação de teste (`0.9`→`0.91`) foi detectada (20 diferenças).

| Medida | Rodada 1 (sem escopo) | Rodada 2 (com escopo) |
| --- | --- | --- |
| Linhas adicionadas/removidas | + 28 linhas / - 61 linhas | + 33 linhas / - 60 linhas |
| Arquivos alterados (e quais estavam fora do esperado) | caso/miniloja/calculo.py | caso/miniloja/calculo.py; nenhum fora do esperado |
| Mudou comportamento? (golden master) | Não alterou o comportamento | Não: 168/168 iguais; 11 verificações passam |
| Tempo de revisão | 30s, a IA criou um script para gerar e comparar a golden master automaticamente | 20s |
| Idas e vindas | Várias confirmações de execução, porém apenas 1 único prompt de refatoração e 1 de confirmação da golden master | 1 pausa para pergunta (2 divergências com o contrato), resposta "siga com A", depois execução direta |

**Escopo da rodada 2:** objetivo separar desconto, frete e taxa em funções; pode tocar só `calculo.py`; não pode tocar a assinatura pública de `calcular_total` nem outros arquivos; invariantes: golden master exato (`==`); pronto quando as verificações e o golden estiverem verdes; pare e pergunte se achar algo que pareça bug.
**Plano do agente: o que eu cortei ou corrigi antes de executar:** plano de 6 passos mantido (`_aplicar_desconto`, `_calcular_frete`, `_aplicar_taxa`, mesma assinatura, rodar golden e verificações, reportar sem corrigir); o agente pediu decisão antes de editar e eu escolhi preservar o comportamento (opção A) em vez de corrigir junto.
**Algo que parecia bug e eu apenas reportei:** (1) frete grátis usa `total > 200`, mas R1.3 diz `>= 200` (caso `borda_200`); (2) `round()` do Python (par mais próximo, float) em vez de meio para cima (R1.5). Ambos preservados; correção fica para tarefa separada com golden regenerado.
**`AGENTS.md` mínimo:** (1) testar: `python -B testes/test_miniloja.py --codigo caso`; (2) golden: `python -B caso/golden_master/gerar_e_comparar.py` (exit 1 se houver diferença); (3) não alterar `testes/` nem `caso/regras.md`; (4) o contrato `regras.md` vale mais que o código; (5) refatorar só com escopo declarado e golden verde; (6) convenção não óbvia: divergência com o contrato é reportada, não corrigida, dentro de uma refatoração.

**Trecho essencial de evidência:** golden `168/168 iguais` antes e depois; `Ran 11 tests ... OK`; `git diff --numstat`: `33 60 caso/miniloja/calculo.py`. **Limite e condição para rever o escopo:** o golden prova só equivalência com o comportamento atual, não conformidade com `regras.md` (frete `>= 200` e arredondamento meio para cima seguem divergentes); rever o escopo ao corrigir essas duas, o que muda o golden e exige regeneração consciente.

**Procedência/IA:** não utilizada / ferramenta e modelo visíveis: Claude Code, Claude Sonnet 5.5; tarefa delegada e contexto: refatorar `calcular_total` em três funções, com escopo declarado, `regras.md` e golden master; trecho aproveitado: `calculo.py` refatorado; minha verificação/intervenção: escolhi a opção A (preservar comportamento) ao ser consultada e conferi golden e verificações. Use "não informado" para metadados indisponíveis. O raciocínio e a decisão registrados são meus.

**Revisão:** [x] golden master; [x] duas rodadas com números; [x] seis campos; [x] AGENTS.md; [x] até uma página.
