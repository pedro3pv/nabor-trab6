import express from 'express';
import type { Request, Response } from 'express';
import cors from 'cors';
import { users, songs, getPlaylistsByUser, getSongsByPlaylist } from './data';

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
// A linha abaixo estava faltando no seu código original
app.get('/users/:id/playlists', (req: Request, res: Response) => {
    const userId = parseInt(req.params.id || '0');
    res.json(getPlaylistsByUser(userId));
});

// Listar músicas de uma playlist
// A linha abaixo estava faltando no seu código original
app.get('/playlists/:id/songs', (req: Request, res: Response) => {
    const playlistId = parseInt(req.params.id || '0');
    res.json(getSongsByPlaylist(playlistId));
});

const PORT = 8001;
app.listen(PORT, () => {
    console.log(`REST Server running on http://localhost:${PORT}`);
});
