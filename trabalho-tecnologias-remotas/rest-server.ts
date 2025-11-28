// rest-server.ts
import express, { Request, Response } from 'express';
import cors from 'cors';
import { users, songs, playlists, getPlaylistsByUser, getSongsByPlaylist } from './data';

const app = express();
app.use(cors());
app.use(express.json());

// Listar usuários
app.get('/users', (req: Request, res: Response) => {
    res.json(users);
});

// Listar músicas
app.get('/songs', (req: Request, res: Response) => {
    res.json(songs);
});

// Listar playlists de um usuário
app.get('/users/:id/playlists', (req: Request, res: Response) => {
    const userId = parseInt(req.params.id);
    res.json(getPlaylistsByUser(userId));
});

// Listar músicas de uma playlist
app.get('/playlists/:id/songs', (req: Request, res: Response) => {
    const playlistId = parseInt(req.params.id);
    res.json(getSongsByPlaylist(playlistId));
});

const PORT = 8001;
app.listen(PORT, () => {
    console.log(`REST Server running on http://localhost:${PORT}`);
});
