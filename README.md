# Pipeline de ETL com Python e MySQL

Este é o meu primeiro projeto prático focado em engenharia e integração de dados. Desenvolvi este repositório para consolidar meus estudos em bancos de dados relacionais (MySQL) e aplicar na prática conceitos fundamentais de ETL (Extract, Transform, Load), migração e tratamento de dados.

## O que este projeto faz

O objetivo do script `etl.py` é simular o fluxo de recebimento e tratamento de um lote de cadastros vindos de um sistema externo antes de entrarem no banco de dados final.

O processo foi dividido em três etapas principais:

1. Extração: O código lê uma lista de dicionários em Python contendo dados brutos (ID, nome, e-mail, cidade e empresa).
2. Transformação: Antes de ir para o banco, os dados passam por uma padronização simples, pois sabemos que alguns dados acabam chegando "bagunçados":
   - Nomes e empresas são convertidos para letras maiúsculas.
   - E-mails são convertidos para letras minúsculas.
   - É gerado um registro de data e hora (`datetime`) no momento do processamento para controle das atualizações.
3. Carga (Idempotente): Os dados tratados são inseridos na tabela `tb_usuarios_tratados` do MySQL. Para evitar duplicidade caso o script seja executado mais de uma vez com os mesmos registros, utilizei a cláusula `ON DUPLICATE KEY UPDATE`. Assim, se o ID já existir, o registro é apenas atualizado.

## Notas sobre o desenvolvimento (C vs. Python)

Neste repositório também deixei disponível o arquivo `etl.c`. Minha ideia inicial era construir toda essa integração utilizando Linguagem C pura com a API nativa do MySQL (`mysql.h`), aproveitando minha familiaridade com a linguagem. 

Depois de uma certa dificuldade com a segurança do sistema, visto que utilizo o windows 11, consegui estruturar e compilar o código em C, mas esbarrei em bloqueios de políticas de execução de binários locais no ambiente Windows. Diante disso, migrei a solução principal para Python usando o driver `pymysql`, o que tornou a execução mais limpa, segura e próxima do que é utilizado no dia a dia do mercado.

## Tecnologias utilizadas

- Python 3
- Biblioteca `PyMySQL`
- MySQL Workbench Server 8.0
- Linguagem C (protótipo inicial)

## Como rodar na sua máquina

Para testar este pipeline localmente, siga os passos abaixo:

**1. Crie o banco e a tabela no MySQL**
Execute o seguinte script no seu ambiente MySQL:

```sql
CREATE DATABASE IF NOT EXISTS integracao_estagio;
USE integracao_estagio;

CREATE TABLE IF NOT EXISTS tb_usuarios_tratados (
    id INT PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100),
    cidade VARCHAR(50),
    empresa VARCHAR(100),
    data_importacao DATETIME
);
```

**2. Instale a dependência do Python**
No terminal do vscode, instale o conector do MySQL:

```bash
pip install pymysql
```

**3. Ajuste a conexão e execute**
* Abra o arquivo `etl.py` e altere a linha do `password="sua_senha_aqui"` colocando os dados do seu MySQL local.
* No terminal do seu sistema operacional, navegue até a pasta do arquivo e execute:
```bash
python etl.py
```
* Abra o banco e rode um `SELECT * FROM tb_usuarios_tratados;` para checar os registros que foram inseridos e tratados pelo pipeline.
