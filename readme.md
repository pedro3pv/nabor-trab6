# Comparação de Tecnologias de Invocação de Serviços Remotos

Este repositório contém o código-fonte e os experimentos realizados para o **Trabalho 6**, focado na comparação prática entre quatro tecnologias de invocação remota: **SOAP, REST, GraphQL e gRPC**.

O projeto implementa um serviço de streaming de músicas idêntico (mesmas regras de negócio e dados) utilizando duas stacks tecnológicas diferentes para fins de comparação: **Python** e **TypeScript (Node.js)**.

## 📂 Estrutura do Repositório

```
.
├── locust.py                               # Script de teste de carga (raiz)
├── trabalho-tecnologias-remotas/           # Implementação em TypeScript/Node.js
│   ├── data.ts                             # Dados mockados (compartilhado)
│   ├── rest-server.ts                      # Servidor REST (Express)
│   ├── graphql-server.ts                   # Servidor GraphQL (Apollo)
│   ├── grpc-server.ts                      # Servidor gRPC
│   ├── soap-server.ts                      # Servidor SOAP
│   ├── music.proto                         # Definição Protocol Buffers
│   └── service.wsdl                        # Definição WSDL
└── trabalho-tecnologias-remotas-python/    # Implementação em Python
    ├── data.py                             # Dados mockados (compartilhado)
    ├── rest_server.py                      # Servidor REST (FastAPI)
    ├── graphql_server.py                   # Servidor GraphQL (Strawberry)
    ├── grpc_server.py                      # Servidor gRPC
    ├── soap_server.py                      # Servidor SOAP (Spyne)
    └── music_service.proto                 # Definição Protocol Buffers
```

---

## 🚀 Pré-requisitos

Certifique-se de ter instalado em sua máquina:
*   **Python 3.8+** e `pip`
*   **Node.js 16+** e `npm`

---

## 🐍 Executando a Versão Python

A versão Python utiliza bibliotecas populares como FastAPI, Strawberry, Spyne e gRPCio.

1.  **Acesse o diretório:**
    ```
    cd trabalho-tecnologias-remotas-python
    ```

2.  **Crie e ative um ambiente virtual (Recomendado):**
    *   *Linux/Mac:*
        ```
        python3 -m venv venv
        source venv/bin/activate
        ```
    *   *Windows:*
        ```
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Instale as dependências:**
    ```
    pip install fastapi uvicorn strawberry-graphql grpcio grpcio-tools spyne lxml locust
    ```

4.  **Gere os arquivos do gRPC (Obrigatório para rodar o gRPC):**
    ```
    python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. music_service.proto
    ```

5.  **Execute os servidores (em terminais separados):**

    *   **SOAP:** `python soap_server.py` (Porta 8000)
    *   **REST:** `python rest_server.py` (Porta 8001)
    *   **GraphQL:** `python graphql_server.py` (Porta 8002)
    *   **gRPC:** `python grpc_server.py` (Porta 50051)

---

## 📘 Executando a Versão TypeScript

A versão TypeScript utiliza o ecossistema Node.js com Express, Apollo Server e gRPC-js.

1.  **Acesse o diretório:**
    ```
    cd trabalho-tecnologias-remotas
    ```

2.  **Instale as dependências:**
    ```
    npm install
    ```

3.  **Execute os servidores (em terminais separados):**
    Utilizamos o `ts-node` para rodar os arquivos TypeScript diretamente.

    *   **REST:** `npx ts-node rest-server.ts` (Porta 8001)
    *   **GraphQL:** `npx ts-node graphql-server.ts` (Porta 8002)
    *   **gRPC:** `npx ts-node grpc-server.ts` (Porta 50051)
    *   **SOAP:** `npx ts-node soap-server.ts` (Porta 8000)

---

## ⚡ Executando Testes de Carga (Locust)

Os testes de carga são realizados utilizando a ferramenta **Locust**. O arquivo de teste está na raiz do projeto.

1.  **Volte para a raiz do projeto:**
    ```
    cd ..
    ```

2.  **Certifique-se de que o Locust está instalado:**
    ```
    pip install locust
    ```

3.  **Execute o Locust:**
    ```
    locust -f locust.py
    ```

4.  **Acesse a interface web:**
    Abra seu navegador em `http://localhost:8089`.

5.  **Configuração do Teste:**
    *   **Number of users:** (Ex: 100)
    *   **Spawn rate:** (Ex: 10)
    *   **Host:** Insira a URL do serviço que deseja testar no momento.
        *   REST Python/Node: `http://localhost:8001`
        *   GraphQL Python/Node: `http://localhost:8002`
        *   SOAP Python/Node: `http://localhost:8000`

> **Nota:** Para testar gRPC com Locust, é necessário um setup de cliente específico dentro do arquivo `locust.py`, pois o Locust nativamente foca em requisições HTTP. O arquivo atual foca em testes HTTP (REST/GraphQL/SOAP).

---

## 🛠 Tecnologias Utilizadas

| Tecnologia | Implementação Python | Implementação TypeScript |
| :--- | :--- | :--- |
| **SOAP** | `spyne` | `soap` (node-soap) |
| **REST** | `FastAPI` | `Express` |
| **GraphQL** | `Strawberry` | `Apollo Server` |
| **gRPC** | `grpcio` | `@grpc/grpc-js` |

## 👥 Autores

*   Pedro Augusto De Oliveira Neto - 2224213
*   Natanael Freitas De Azevedo - 2224186
*   Francisco Dantas Da Silva Neto - 2223879