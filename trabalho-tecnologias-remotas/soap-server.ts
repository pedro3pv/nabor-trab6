// soap-server.ts
import * as soap from 'soap';
import http from 'http';
import fs from 'fs';
import { users } from './data';

const service = {
    MusicService: {
        MusicPort: {
            // Retornaremos JSON stringificado pois configurar tipos complexos 
            // XML no WSDL manualmente é muito propenso a erro para um trabalho simples.
            ListUsers: function (args: any) {
                return { users: JSON.stringify(users) };
            }
        }
    }
};

const xml = fs.readFileSync('service.wsdl', 'utf8');
const server = http.createServer(function (request, response) {
    response.end('404: Not Found: ' + request.url);
});

server.listen(8000);
soap.listen(server, '/wsdl', service, xml, function () {
    console.log('SOAP Server running on http://localhost:8000/wsdl?wsdl');
});
