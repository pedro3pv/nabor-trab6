// grpc-server.ts
import * as grpc from '@grpc/grpc-js';
import * as protoLoader from '@grpc/proto-loader';
import path from 'path';
import { users, songs, getPlaylistsByUser } from './data';

const PROTO_PATH = path.join(__dirname, 'music.proto');

const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true
});

const musicProto = grpc.loadPackageDefinition(packageDefinition) as any;

const server = new grpc.Server();

// Implementação dos métodos do Proto
server.addService(musicProto.MusicService.service, {
    ListUsers: (_: any, callback: any) => {
        callback(null, { users: users });
    },
    ListSongs: (_: any, callback: any) => {
        callback(null, { songs: songs });
    },
    ListUserPlaylists: (call: any, callback: any) => {
        const userId = call.request.id;
        const userPlaylists = getPlaylistsByUser(userId);
        callback(null, { playlists: userPlaylists });
    }
});

const PORT = '0.0.0.0:50051';
server.bindAsync(PORT, grpc.ServerCredentials.createInsecure(), () => {
    console.log(`gRPC Server running on ${PORT}`);
});
