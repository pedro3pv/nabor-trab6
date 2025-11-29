# locust-soap.py
"""
Teste de Carga para Serviços SOAP usando Locust
SOAP usa POST com XML, não GET com rotas REST
"""

from locust import HttpUser, task, between
import time
from locust import events


class SoapMusicStreamingUser(HttpUser):
    """
    Usuário simulado que acessa o serviço SOAP de streaming de músicas
    """
    wait_time = between(1, 2)
    
    # Endpoint SOAP (ajuste se necessário)
    soap_endpoint = "/"
    
    # Headers SOAP
    headers = {
        'Content-Type': 'text/xml; charset=utf-8',
        'SOAPAction': ''
    }
    
    @task(3)
    def list_users(self):
        """Lista todos os usuários via SOAP"""
        soap_body = """<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" 
               xmlns:mus="music.soap">
    <soap:Body>
        <mus:list_users/>
    </soap:Body>
</soap:Envelope>"""
        
        self.client.post(
            self.soap_endpoint,
            data=soap_body,
            headers=self.headers,
            name="SOAP: list_users"
        )
    
    @task(3)
    def list_songs(self):
        """Lista todas as músicas via SOAP"""
        soap_body = """<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" 
               xmlns:mus="music.soap">
    <soap:Body>
        <mus:list_songs/>
    </soap:Body>
</soap:Envelope>"""
        
        self.client.post(
            self.soap_endpoint,
            data=soap_body,
            headers=self.headers,
            name="SOAP: list_songs"
        )
    
    @task(1)
    def list_user_playlists(self):
        """Lista playlists do usuário 1 via SOAP"""
        soap_body = """<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" 
               xmlns:mus="music.soap">
    <soap:Body>
        <mus:list_user_playlists>
            <mus:user_id>1</mus:user_id>
        </mus:list_user_playlists>
    </soap:Body>
</soap:Envelope>"""
        
        self.client.post(
            self.soap_endpoint,
            data=soap_body,
            headers=self.headers,
            name="SOAP: list_user_playlists"
        )


if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║   Teste de Carga SOAP - Serviço de Streaming de Músicas  ║
    ╚═══════════════════════════════════════════════════════════╝
    
    SOAP usa POST com XML, não GET com rotas REST!
    
    Para executar:
    
    1. Inicie o servidor SOAP:
       Python: python soap_server.py
       TypeScript: npx ts-node soap-server.ts
    
    2. Execute o Locust:
       locust -f locust-soap.py --host=http://localhost:8000
    
    3. Acesse: http://localhost:8089
    """)
