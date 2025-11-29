# locust-graphql.py
"""
Teste de Carga para Serviços GraphQL usando Locust
GraphQL usa POST com queries JSON
"""

from locust import HttpUser, task, between
from locust_global_time import StepLoadShape
import json


class GraphQLMusicStreamingUser(HttpUser):
    """
    Usuário simulado que acessa o serviço GraphQL de streaming de músicas
    """
    wait_time = between(1, 2)
    
    headers = {'Content-Type': 'application/json'}

    @task(3)
    def list_users(self):
        """Lista todos os usuários"""
        query = {
            "query": """
                query {
                    users {
                        id
                        name
                        email
                    }
                }
            """
        }
        self.client.post(
            "/graphql",
            data=json.dumps(query),
            headers=self.headers,
            name="GraphQL: users"
        )

    @task(3)
    def list_songs(self):
        """Lista todas as músicas"""
        query = {
            "query": """
                query {
                    songs {
                        id
                        title
                        artist
                    }
                }
            """
        }
        self.client.post(
            "/graphql",
            data=json.dumps(query),
            headers=self.headers,
            name="GraphQL: songs"
        )

    @task(2)
    def users_with_playlists(self):
        """Busca usuários com suas playlists (nested query)"""
        query = {
            "query": """
                query {
                    users {
                        id
                        name
                        playlists {
                            id
                            name
                        }
                    }
                }
            """
        }
        self.client.post(
            "/graphql",
            data=json.dumps(query),
            headers=self.headers,
            name="GraphQL: users with playlists"
        )
    
    @task(1)
    def full_nested_query(self):
        """Query completa aninhada - vantagem do GraphQL"""
        query = {
            "query": """
                query {
                    users {
                        id
                        name
                        email
                        playlists {
                            id
                            name
                            songs {
                                id
                                title
                                artist
                            }
                        }
                    }
                }
            """
        }
        self.client.post(
            "/graphql",
            data=json.dumps(query),
            headers=self.headers,
            name="GraphQL: full nested query"
        )


if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║ Teste de Carga GraphQL - Serviço de Streaming de Músicas ║
    ╚═══════════════════════════════════════════════════════════╝
    
    GraphQL usa POST com queries JSON, mostrando sua flexibilidade!
    
    Para executar:
    
    1. Inicie o servidor GraphQL:
       Python: python graphql_server.py
       TypeScript: npx ts-node graphql-server.ts
    
    2. Execute o Locust:
       locust -f locust-graphql.py --host=http://localhost:8002
    
    3. Acesse: http://localhost:8089
    """)

## StepLoadShape agora é importado de locust-global-time.py
