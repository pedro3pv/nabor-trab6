## 📂 Documentos

📄 [Como Rodar O Projeto](docs/how_to_run.md)

---

# Comparação de Tecnologias de Invocação de Serviços Remotos

Este repositório contém o código-fonte, experimentos e análises realizados para o **Trabalho 6**, focado na comparação prática entre quatro tecnologias de invocação remota: **SOAP, REST, GraphQL e gRPC**.

O projeto implementa um serviço de streaming de músicas idêntico (mesmas regras de negócio e dados) utilizando duas stacks tecnológicas diferentes para fins de comparação: **Python** e **TypeScript (Node.js)**.

---

## 👥 Identificação da Equipe

* **Pedro Augusto De Oliveira Neto** - 2224213
* **Natanael Freitas De Azevedo** - 2224186
* **Francisco Dantas Da Silva Neto** - 2223879

---

## 📚 Análise das Tecnologias

Abaixo apresentamos a origem, características, vantagens, desvantagens e exemplos de implementação de cada tecnologia estudada.

### 1. SOAP (Simple Object Access Protocol)

* **Origem:** Criado pela Microsoft em 1998 e padronizado pela W3C. Foi a base da primeira geração de Web Services corporativos.
* **Características:** Protocolo baseado estritamente em XML. Possui contrato rígido definido via WSDL (Web Services Description Language) e suporta padrões avançados de segurança (WS-Security) e transações (WS-AtomicTransaction).
* **Vantagens:** Independência de linguagem e plataforma; robustez para ambientes corporativos; suporte a operações estatais e assíncronas complexas.
* **Desvantagens:** Verbosidade excessiva (XML); parsing lento; complexidade de implementação; maior uso de banda.

### 2. REST (Representational State Transfer)

* **Origem:** Definido por Roy Fielding em sua tese de doutorado em 2000.
* **Características:** Estilo arquitetural focado em recursos identificados por URIs. Utiliza os verbos HTTP (GET, POST, PUT, DELETE) semanticamente e é stateless.
* **Vantagens:** Simplicidade e facilidade de uso; cacheabilidade nativa (HTTP); flexibilidade de formatos (JSON, XML, etc.); ampla adoção e ferramentas de debug.
* **Desvantagens:** Pode sofrer de *over-fetching* (receber dados demais) ou *under-fetching* (receber dados de menos); falta de contrato estrito nativo (embora OpenAPI ajude).

### 3. GraphQL

* **Origem:** Desenvolvido pelo Facebook em 2012 e aberto ao público em 2015.
* **Características:** Linguagem de consulta para APIs. O cliente define exatamente a estrutura dos dados que deseja receber.
* **Vantagens:** Elimina *over-fetching* e *under-fetching*; tipagem forte; permite obter múltiplos recursos relacionados em uma única requisição; excelente experiência para o desenvolvedor frontend.
* **Desvantagens:** Complexidade no backend (problema N+1); cacheamento HTTP é mais difícil (geralmente usa apenas POST); curva de aprendizado maior.

### 4. gRPC (Google Remote Procedure Call)

* **Origem:** Lançado pelo Google em 2015, baseado na infraestrutura interna "Stubby".
* **Características:** Framework RPC moderno que utiliza HTTP/2 para transporte e Protocol Buffers (binário) para serialização de dados.
* **Vantagens:** Performance extrema (binário + multiplexação); streaming bidirecional nativo; geração automática de código cliente/servidor (stubs) em várias linguagens.
* **Desvantagens:** Formato binário não legível por humanos (dificulta debug simples); acoplamento forte via arquivos `.proto`; requer suporte a HTTP/2.

---

## 💻 Exemplos de Código (Python)

Demonstração de como realizar a mesma operação ("Buscar Usuário") em cada tecnologia usando Python.

```
# --- 1. REST (usando Requests) ---
import requests
response = requests.get("http://localhost:8001/users/1")
print(response.json())

# --- 2. SOAP (usando Zeep) ---
from zeep import Client
client = Client('http://localhost:8000/soap_service?wsdl')
result = client.service.get_user(id=1)
print(result)

# --- 3. GraphQL (usando Requests) ---
query = """
{
  user(id: 1) {
    id
    name
    playlists { title }
  }
}
"""
response = requests.post("http://localhost:8002/graphql", json={'query': query})
print(response.json())

# --- 4. gRPC (usando grpcio) ---
import grpc
import music_service_pb2, music_service_pb2_grpc

with grpc.insecure_channel('localhost:50051') as channel:
    stub = music_service_pb2_grpc.MusicServiceStub(channel)
    response = stub.GetUser(music_service_pb2.UserId(id=1))
    print(response.name)
```

---

## 📊 Resultados dos Testes de Carga

Realizamos testes de carga comparativos entre as implementações em **Python** e **TypeScript**. Os testes foram executados com a ferramenta **Locust**, simulando múltiplos usuários simultâneos.

### Gráfico 1: Throughput (Requisições por Segundo)

O gráfico abaixo mostra o desempenho máximo (RPS) alcançado por cada tecnologia nas duas linguagens.

![Comparativo RPS](comparativo_lang_rps.jpg)

**Análise:**

* **gRPC dominou:** Alcançou **~1400 RPS** (Python) e **~1300 RPS** (TypeScript), quase o triplo das outras tecnologias. Isso se deve à eficiência do HTTP/2 e da serialização binária (Protobuf).
* **Equilíbrio nas baseadas em texto:** REST, SOAP e GraphQL mantiveram-se na faixa de **500-600 RPS**.
* **Python vs. TypeScript:** Surpreendentemente, a implementação Python (usando bibliotecas C-optimized como `grpcio` e `fastapi`) teve desempenho ligeiramente superior ou equivalente ao Node.js neste cenário específico de I/O simulado.

### Gráfico 2: Latência Média (ms)

Este gráfico ilustra o tempo médio de resposta (quanto menor, melhor).

![Comparativo Latência](comparativo_lang_latencia.jpg)

**Análise:**

* **gRPC é praticamente instantâneo:** Latências na casa de **0.01ms a 0.03ms**, indicando overhead quase nulo de processamento.
* **GraphQL em Python:** Apresentou uma latência significativamente maior (~700ms). Isso provavelmente se deve à biblioteca `Strawberry` em Python, que pode ter um overhead maior de parsing/resolução comparada ao `Apollo Server` do Node.js.
* **Consistência:** REST e SOAP mantiveram latências baixas e estáveis (~2.5ms) em ambas as linguagens.

---

## 🧠 Análise Crítica e Conclusão

Com base na implementação e nos testes, concluímos:

1. **gRPC é a escolha definitiva para performance:** Se o requisito é alta vazão e baixa latência (ex: comunicação interna entre microsserviços), gRPC é imbatível, independentemente da linguagem (Python ou TS).
2. **REST continua sendo o "padrão ouro" para APIs públicas:** Oferece o melhor equilíbrio entre simplicidade, performance aceitável e facilidade de integração.
3. **GraphQL oferece a melhor DX (Developer Experience) no Frontend:** Embora tenha sido mais lento no backend (especialmente em Python), a flexibilidade de pedir exatamente o que se precisa compensa em aplicações complexas com muitos relacionamentos.
4. **SOAP é legado:** A complexidade de implementação e a verbosidade do XML não trouxeram benefícios tangíveis neste cenário. Seu uso só se justifica em sistemas legados ou cenários bancários específicos que exigem WS-Security estrito.
5. **Linguagem:** Para este tipo de microserviço de streaming simulado, **Python** mostrou-se tão capaz quanto TypeScript, derrubando o mito de que "Python é sempre lento para web". A escolha da biblioteca (FastAPI, gRPC C-core) faz toda a diferença.

---

## 📂 Estrutura do Repositório e Como Executar

### Pré-requisitos

* **Python 3.8+**
* **Node.js 16+**

### Executando a Versão Python

```
cd trabalho-tecnologias-remotas-python
python -m venv venv
source venv/bin/activate  # ou .\venv\Scripts\activate no Windows
pip install -r requirements.txt
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. music_service.proto

# Rodar servidores (em terminais separados):
python soap_server.py
python rest_server.py
python graphql_server.py
python grpc_server.py
```

### Executando a Versão TypeScript

```
cd trabalho-tecnologias-remotas
npm install

# Rodar servidores (em terminais separados):
npx ts-node soap-server.ts
npx ts-node rest-server.ts
npx ts-node graphql-server.ts
npx ts-node grpc-server.ts
```

### Rodando os Testes (Locust)

```
# Instalar Locust
pip install locust

# Executar (Exemplo REST)
locust -f locust_rest.py --host=http://localhost:8001
```
