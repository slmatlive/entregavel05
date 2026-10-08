# Sprint 5 — Sistema de Análise de Dados em Python

## Sobre o trabalho

Neste projeto, fiz um programa para ler um arquivo CSV com nome, e-mail, CPF, telefone e data. O programa verifica o formato dos dados e mostra quais registros estão válidos e quais precisam de correção.

Também fiz um relatório que aparece no terminal e fica salvo no arquivo `relatorio.txt`.

Usei Python e somente bibliotecas que já vêm instaladas nele: `csv`, `re`, `datetime`, `pathlib` e `sys`.

## Arquivos do projeto

- `analisador_dados.py`: programa principal.
- `dados.csv`: dados fictícios que usei para testar.
- `teste_analisador.py`: testes do programa.
- `relatorio_exemplo.txt`: exemplo de relatório gerado.
- `README.md`: explicação da atividade.

## Como executar

1. Instalar o Python, caso ainda não tenha.
2. Abrir a pasta do projeto no VS Code ou no terminal.
3. Executar:

```bash
python analisador_dados.py
```

O arquivo `dados.csv` precisa estar na mesma pasta do programa. Depois da execução, o arquivo `relatorio.txt` será criado nessa pasta.

Também posso indicar outro arquivo CSV:

```bash
python analisador_dados.py outro_arquivo.csv
```

Para executar os testes:

```bash
python -m unittest -v teste_analisador.py
```

Se o comando `python` não funcionar no Windows, posso usar `py` no lugar.

## Como devem ser os dados de entrada

O arquivo CSV precisa ter estas colunas, escritas desse jeito:

`nome,email,cpf,telefone,data`

Exemplo de duas linhas de dados fictícios:

```csv
nome,email,cpf,telefone,data
Ana Souza,ana.souza@exemplo.com,123.456.789-09,(98) 98765-4321,12/03/2026
Eva Costa,eva@exemplo.com,567.890.123-45,(98) 95555-4444,31/02/2026
```

A primeira linha está no formato esperado. A segunda tem uma data impossível (31 de fevereiro).

## Validações que usei

- **E-mail:** conferi se o texto tem uma parte antes de `@` e um domínio com ponto, como `pessoa@exemplo.com`.
- **CPF:** conferi se está no formato `000.000.000-00`. **Atenção:** isso não verifica os dígitos verificadores nem confirma que o CPF existe. É apenas uma validação do formato pedido na atividade.
- **Telefone:** considerei celular com DDD no formato `(98) 98765-4321` (o espaço depois do DDD é opcional).
- **Data:** usei o formato `DD/MM/AAAA` e também o `datetime.strptime()` para verificar se o dia e o mês existem.
- **Nome:** não pode estar vazio.

As expressões regulares foram feitas com o módulo `re`. Usei `^` e `$` para marcar início e fim, `\d` para dígitos, `\w` para caracteres de palavra e `\s` para o espaço opcional no telefone.

## Exceções tratadas

- `FileNotFoundError`: acontece quando tento abrir um arquivo que não existe.
- `KeyError`: acontece quando falta alguma das colunas necessárias no cabeçalho do CSV.
- `ValueError`: usei para tratar um CSV vazio e para reconhecer datas que não existem, como `31/02/2026`.
- `FormatoInvalidoError`: criei essa exceção para identificar registros com campos incorretos. Quando isso acontece, o programa anota o motivo e continua lendo as outras linhas.
- `OSError`: tratei também problemas de leitura e gravação de arquivos.

No `main()`, usei `try`, `except`, `else` e `finally`. O `else` mostra o relatório quando a análise termina, e o `finally` mostra a mensagem de encerramento mesmo se houver algum erro.

## Exemplo de saída

Ao executar com o `dados.csv`, o começo do relatório fica assim:

```text
RELATÓRIO DE ANÁLISE DE DADOS
============================================================
Total de registros: 8
Registros válidos: 3
Registros inválidos: 5
Percentual de válidos: 37.5%
------------------------------------------------------------
```

Depois dessas estatísticas, o relatório lista os registros, com a situação e o motivo quando há erro. O exemplo completo está em `relatorio_exemplo.txt`.

## O que aprendi com a atividade

Com essa atividade, pratiquei a leitura e escrita de arquivos usando `with open()`, o uso de regex para conferir formatos e o tratamento de erros com `try/except`. Também vi que é melhor indicar o problema de cada linha do que fazer o programa parar por causa de um cadastro incorreto.

## Como entregar pelo GitHub

1. Entrar no [GitHub](https://github.com/) e criar um repositório **público**, com o nome `sprint-05-analise-dados`.
2. Clicar em **Add file > Upload files**.
3. Enviar os arquivos desta pasta (não é necessário enviar o ZIP).
4. Confirmar em **Commit changes**.
5. Copiar o link do repositório e enviar ao professor.

O repositório ainda precisa ser criado na sua conta. O arquivo ZIP é apenas para organizar os materiais antes do envio.
