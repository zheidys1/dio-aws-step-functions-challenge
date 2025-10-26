# dio-aws-step-functions-challenge
Projeto desenvolvido como parte do desafio da DIO para praticar AWS Step Functions. O objetivo é aprender a orquestrar funções serverless e integrar serviços da AWS.

DIO Challenge: Orquestração de Microsserviços com AWS Step Functions

Este repositório documenta a conclusão do desafio prático da DIO, que visa consolidar o conhecimento sobre a criação de **Workflows Automatizados (Máquinas de Estado)** usando o **AWS Step Functions**.

O projeto demonstra a orquestração de três microsserviços (funções AWS Lambda) para processar uma entrada de dados com lógica de decisão e tratamento de erros.

##  1. Arquitetura da Solução

O fluxo de trabalho foi modelado para garantir que a execução de tarefas seja sequencial e condicional, baseado na validação dos dados de entrada.

**Nome da Máquina de Estado:** `DIO-Workflow-Microservices`
### Diagrama do Workflow

O diagrama abaixo, gerado pelo AWS Workflow Studio, ilustra o fluxo exato implementado:

### Prova de Execução Bem-Sucedida

Abaixo, o status da Máquina de Estado com a execução "Com êxito" no console AWS, provando a correta implantação e funcionalidade:

![Status Com Êxito no Console Step Functions](images/maquina-estado-sucesso-geral.png)

### Serviços Envolvidos

| Serviço | Função | Componentes no Workflow |
| :--- | :--- | :--- |
| **AWS Step Functions** | O orquestrador central. Gerencia o estado e as transições lógicas. | Estados `Task`, `Choice`, `Fail`, `Catch`, `End`. |
| **AWS Lambda** | Os microsserviços *serverless* que executam a lógica de negócio. | `Validate Input`, `Process Data`, `Notify Success (sns)`. |
| **AWS IAM** | Gerencia as permissões. | **IAM Role** criada automaticamente para o Step Functions invocar as Lambdas. |

##  2. Implementação e Lógica do Workflow

O fluxo segue uma lógica de aprovação e processamento em estágios:

### 2.1. Estados Chave (Tasks)

As tarefas (`Task`) são funções Lambda, cujos ARNs foram configurados no JSON (Amazon States Language - ASL):

| `Validate Input` | Checa se a entrada tem um campo `amount` > 0. | `arn:aws:lambda:us-east-1:408585017203:function:sf-validate-input-function` |
| `Process Data` | Simula a gravação de dados em um banco de dados. | `arn:aws:lambda:us-east-1:408585017203:function:sf-process-data-function` |
| `Notify Success (sns)` | Simula o envio de confirmação (via SNS/e-mail). | `arn:aws:lambda:us-east-1:408585017203:function:sf-notify-success-function` |

O estado `Choice` utiliza a saída do `Validate Input` para controlar o fluxo:

* **Condição:** Verifica se o campo `$.ValidationResult.isValid` (retornado pela primeira Lambda) é **`true`**.
* **Caminho Verde:** Se `true`, avança para o estado **`Process Data`**.
* **Caminho Vermelho/Default:** Se `false` (ou se a condição não for atendida), avança para o estado terminal **`Fail`**.

### 2.3. Tratamento de Erros (`Catch State`)

O estado **`Process Data`** inclui uma cláusula `Catch`:
* Se a Lambda `Process Data` falhar por qualquer motivo (`"ErrorEquals": ["States.ALL"]`), o fluxo é redirecionado para o estado **`Handle failure`** (um estado `Pass` simples de registro), em vez de fazer com que toda a execução falhe.

---

## 3. Arquivos do Repositório

| Arquivo/Pasta | Descrição |
| :--- | :--- |
| `README.md` | Este arquivo, documentando a arquitetura e a implementação. |
| `step-function-definition.json` | O código ASL JSON completo da Máquina de Estado, copiado do Workflow Studio. |
| `lambda/` | Contém os códigos Python de simulação para cada microsserviço. |
| `images/` | Contém capturas de tela do diagrama e da execução bem-sucedida. |

---

## 4. Insights e Aprendizados

Durante a execução deste desafio, os seguintes conceitos foram consolidados:

* **Orquestração vs. Coreografia:** O Step Functions permite orquestrar (gerenciar o fluxo centralmente), diferentemente da coreografia, onde os serviços comunicam-se de forma descentralizada.
* **Sintaxe ASL:** A importância de uma sintaxe JSON perfeita, onde erros sutis (aspas corrompidas, vírgulas faltando) impedem a implantação do workflow.
* **Gestão de Estado:** O Step Functions gerencia automaticamente o estado (o resultado) de cada tarefa, passando-o como entrada para o próximo estado. A Lambda de `Validate Input` retorna `isValid`, e o `Choice` o consome.
* **Resiliência:** A implementação do bloco `Catch` no `Process Data` é um padrão de resiliência, garantindo que falhas em microsserviços sejam tratadas sem derrubar todo o workflow.