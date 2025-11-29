# Comparação de Tecnologias de Invocação de Serviços Remotos

Este repositório contém o código-fonte e os experimentos realizados para o **Trabalho 6**, focado na comparação prática entre quatro tecnologias de invocação remota: **SOAP, REST, GraphQL e gRPC**.

O projeto implementa um serviço de streaming de músicas idêntico (mesmas regras de negócio e dados) utilizando duas stacks tecnológicas diferentes para fins de comparação: **Python** e **TypeScript (Node.js)**.

## 📂 Estrutura do Repositório

```
.
├── locust-rest.py                          # Script de teste de carga REST
├── locust-graphql.py                       # Script de teste de carga GraphQL
├── locust-soap.py                          # Script de teste de carga SOAP
├── locust-grpc.py                          # Script de teste de carga gRPC básico
├── locust-grpc-advanced.py                 # Script de teste de carga gRPC avançado
├── trabalho-tecnologias-remotas/           # Implementação em TypeScript/Node.js
│   ├── package.json                        # Dependências Node.js
│   ├── tsconfig.json                       # Configuração TypeScript
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
    ├── music_service.proto                 # Definição Protocol Buffers
    ├── music_service_pb2.py                # Gerado automaticamente pelo protoc
    └── music_service_pb2_grpc.py           # Gerado automaticamente pelo protoc
```

---

## 🚀 Pré-requisitos

Certifique-se de ter instalado em sua máquina:

* **Python 3.8+** e `pip`
* **Node.js 16+** e `npm`

---

## 🐍 Executando a Versão Python

A versão Python utiliza bibliotecas populares como FastAPI, Strawberry, Spyne e gRPCio.

### 1. Acesse o diretório:

```
cd trabalho-tecnologias-remotas-python
```

### 2. Crie e ative um ambiente virtual (Recomendado):

**Linux/Mac:**

```
python3 -m venv venv
source venv/bin/activate
```

**Windows:**

```
python -m venv venv
.\venv\Scripts\activate
```

### 3. Instale as dependências:

```
pip install fastapi uvicorn strawberry-graphql grpcio grpcio-tools spyne lxml locust
```

### 4. Gere os arquivos do gRPC (Obrigatório):

```
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. music_service.proto
```

> **Importante:** Este comando gera os arquivos `music_service_pb2.py` e `music_service_pb2_grpc.py`, necessários para o funcionamento do servidor e dos testes gRPC.

### 5. Execute os servidores (em terminais separados):

| Tecnologia        | Comando                      | Porta |
| :---------------- | :--------------------------- | :---- |
| **SOAP**    | `python soap_server.py`    | 8000  |
| **REST**    | `python rest_server.py`    | 8001  |
| **GraphQL** | `python graphql_server.py` | 8002  |
| **gRPC**    | `python grpc_server.py`    | 50051 |

---

## 📘 Executando a Versão TypeScript

A versão TypeScript utiliza o ecossistema Node.js com Express, Apollo Server e gRPC-js.

### 1. Acesse o diretório:

```
cd trabalho-tecnologias-remotas
```

### 2. Instale as dependências:

```
npm install
```

Isso instalará todas as dependências listadas no `package.json`:

- `express`, `@types/express` - Servidor REST
- `@apollo/server`, `graphql` - Servidor GraphQL
- `@grpc/grpc-js`, `@grpc/proto-loader` - Servidor gRPC
- `soap` - Servidor SOAP
- `typescript`, `ts-node` - Compilação e execução TypeScript

### 3. Execute os servidores (em terminais separados):

Utilizamos o `ts-node` para rodar os arquivos TypeScript diretamente sem compilação prévia.

| Tecnologia        | Comando                           | Porta |
| :---------------- | :-------------------------------- | :---- |
| **REST**    | `npx ts-node rest-server.ts`    | 8001  |
| **GraphQL** | `npx ts-node graphql-server.ts` | 8002  |
| **gRPC**    | `npx ts-node grpc-server.ts`    | 50051 |
| **SOAP**    | `npx ts-node soap-server.ts`    | 8000  |

---

## ⚡ Executando Testes de Carga

Os testes de carga são realizados utilizando a ferramenta **Locust**. Existem scripts específicos para cada protocolo, pois cada um exige um formato de requisição diferente.

### 🌐 Testes HTTP (REST, GraphQL, SOAP)

#### 1. Volte para a raiz do projeto:

```
cd ..  # Se estiver dentro de uma das pastas de implementação
```

#### 2. Certifique-se de que o Locust está instalado:

```
pip install locust
```

#### 3. Execute o script correspondente à tecnologia que deseja testar:

**Para testar REST:**

```
locust -f locust-rest.py --host=http://localhost:8001
```

**Para testar GraphQL:**

```
locust -f locust-graphql.py --host=http://localhost:8002
```

**Para testar SOAP:**

```
locust -f locust-soap.py --host=http://localhost:8000
```

#### 4. Acesse a interface web:

Abra seu navegador em `http://localhost:8089`

#### 5. Configuração do Teste:

* **Number of users:** (Ex: 1000)
* **Spawn rate:** (Ex: 100)
* **Host:** (Já preenchido automaticamente pelo comando acima)

---

### 🚀 Testes gRPC

O gRPC requer um cliente customizado, pois o Locust nativamente suporta apenas HTTP.

#### 1. Certifique-se de que os arquivos Protocol Buffer foram gerados:

```
cd trabalho-tecnologias-remotas-python
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. music_service.proto
cd ..
```

#### 2. Execute o servidor gRPC (Python ou TypeScript):

```
# Python
cd trabalho-tecnologias-remotas-python
python grpc_server.py

# OU TypeScript
cd trabalho-tecnologias-remotas
npx ts-node grpc-server.ts
```

#### 3. Em outro terminal, execute o teste de carga gRPC:

**Teste Básico:**

```
locust -f locust-grpc.py --host=localhost:50051
```

**Teste Avançado (com múltiplos tipos de usuários e carga em degraus):**

```
locust -f locust-grpc-advanced.py --host=localhost:50051
```

#### 4. Acesse a interface web:

`http://localhost:8089`

> **Nota:** Para gRPC, o formato do host é `hostname:porta` (ex: `localhost:50051`), diferente do HTTP que usa `http://hostname:porta`.

---

## 📊 Comparando Resultados

Para uma análise completa, recomendamos:

1. **Executar cada servidor separadamente** (um de cada vez)
2. **Rodar o teste de carga correspondente** por 2-3 minutos
3. **Anotar as métricas principais:**

   - Requests per second (RPS)
   - Tempo médio de resposta
   - Percentil 95 e 99
   - Taxa de falhas
4. **Gerar gráficos** usando a funcionalidade de download do Locust ou exportando os dados

### Métricas Esperadas

Com base em benchmarks típicos:

| Tecnologia        | Performance           | Tamanho Payload    | Complexidade |
| :---------------- | :-------------------- | :----------------- | :----------- |
| **gRPC**    | ⭐⭐⭐⭐⭐ Muito Alta | Pequeno (binário) | Média       |
| **REST**    | ⭐⭐⭐⭐ Alta         | Médio (JSON)      | Baixa        |
| **GraphQL** | ⭐⭐⭐ Média         | Variável (JSON)   | Alta         |
| **SOAP**    | ⭐⭐ Baixa            | Grande (XML)       | Muito Alta   |

---

## 🛠 Tecnologias Utilizadas

| Tecnologia        | Implementação Python        | Implementação TypeScript                 |
| :---------------- | :---------------------------- | :----------------------------------------- |
| **SOAP**    | `spyne` + `lxml`          | `soap` (node-soap)                       |
| **REST**    | `FastAPI` + `uvicorn`     | `Express`                                |
| **GraphQL** | `Strawberry GraphQL`        | `Apollo Server`                          |
| **gRPC**    | `grpcio` + `grpcio-tools` | `@grpc/grpc-js` + `@grpc/proto-loader` |

---

## 🧪 Testando Manualmente

### REST (usando curl):

```
# Listar usuários
curl http://localhost:8001/users

# Listar músicas
curl http://localhost:8001/songs

# Playlists do usuário 1
curl http://localhost:8001/users/1/playlists
```

### GraphQL (usando curl):

```
curl -X POST http://localhost:8002/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ users { id name playlists { name songs { title } } } }"}'
```

### gRPC (usando grpcurl):

```
# Instalar grpcurl: https://github.com/fullstorydev/grpcurl

# Listar serviços
grpcurl -plaintext localhost:50051 list

# Chamar método
grpcurl -plaintext -d '{}' localhost:50051 MusicService/ListUsers
```

---

## 👥 Autores

* **Pedro Augusto De Oliveira Neto** - 2224213
* **Natanael Freitas De Azevedo** - 2224186
* **Francisco Dantas Da Silva Neto** - 2223879

---
