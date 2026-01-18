PIPELINE B3 – RAW → REFINED
==========================

1. VISÃO GERAL
--------------
Este projeto implementa um pipeline de dados batch utilizando AWS,
com ingestão de dados da B3, armazenamento em S3, processamento com
AWS Glue (Spark) e consumo via Athena.

O pipeline segue uma arquitetura em camadas:
- Raw: dados brutos particionados por data
- Refined: dados transformados, agregados e enriquecidos

A orquestração entre as camadas é feita via eventos S3 e AWS Lambda.


2. ARQUITETURA
--------------
Fluxo principal:

Fonte de Dados
   ↓
Glue Job RAW (Spark)
   ↓
S3 Raw (Parquet particionado por dt)
   ↓
Arquivo de controle (_READY.json)
   ↓
Evento S3
   ↓
AWS Lambda
   ↓
Glue Job REFINED (Spark)
   ↓
S3 Refined (Parquet particionado por dt e ticker)
   ↓
Athena



3. CAMADA RAW
-------------
- Armazena dados brutos em formato Parquet
- Particionamento por dt (data do processamento)
- Não depende de arquivo _SUCCESS
- Gera arquivo de controle "_READY.json" ao final do processamento

Exemplo de path:
s3://fiap-b3-data/raw/b3_stock/dt=2024-01-10/


4. CONTROLE DE PROCESSAMENTO
----------------------------
Ao final da escrita da camada RAW, é gerado um arquivo:

_READY.json

Conteúdo:
{
  "process_date": "YYYY-MM-DD"
}

Este arquivo é usado como gatilho para a execução da camada REFINED.


5. LAMBDA
---------
A função Lambda é acionada por evento do S3 quando um arquivo
"_READY.json" é criado no prefixo:

raw/b3_stock/

A Lambda:
- Lê o arquivo JSON
- Extrai o campo "process_date"
- Inicia o Glue Job REFINED passando o parâmetro PROCESS_DATE


6. CAMADA REFINED
-----------------
O job Glue REFINED:
- Lê dados da camada RAW
- Processa uma janela  D-5 (dias)
- Realiza agregações e cálculos analíticos
- Escreve apenas a data processada (PROCESS_DATE)

Transformações obrigatórias implementadas:
A) Agregação numérica (avg e sum)
B) Renomeação de colunas
C) Cálculo baseado em data (média móvel de 5 dias)

Particionamento final:
- dt
- ticker


7. CONSUMO VIA ATHENA
--------------------
Os dados da camada REFINED são consultados diretamente via Athena,
permitindo análises analíticas e validação do pipeline.


8. TECNOLOGIAS UTILIZADAS
-------------------------
- AWS S3
- AWS Glue (Spark)
- AWS Lambda
- AWS Athena
- Python
- PySpark
