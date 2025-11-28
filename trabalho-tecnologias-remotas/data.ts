// data.ts

export interface Song {
    id: number;
    title: string;
    artist: string;
}

export interface User {
    id: number;
    name: string;
    email: string;
}

export interface Playlist {
    id: number;
    name: string;
    user_id: number;
    song_ids: number[];
}

// Dados Mockados (Em memória)
export const users: User[] = [
    { id: 1, name: 'Alice', email: 'alice@example.com' },
    { id: 2, name: 'Bob', email: 'bob@example.com' }
];

export const songs: Song[] = [
    { id: 1, title: 'Song A', artist: 'Artist X' },
    { id: 2, title: 'Song B', artist: 'Artist Y' },
    { id: 3, title: 'Song C', artist: 'Artist X' }
];

export const playlists: Playlist[] = [
    { id: 1, name: 'Alice Favorites', user_id: 1, song_ids: [1, 2] },
    { id: 2, name: 'Bob Rock', user_id: 2, song_ids: [3] }
];

// Helpers de consulta
export const getPlaylistsByUser = (userId: number) => playlists.filter(p => p.user_id === userId);
export const getSongsByPlaylist = (playlistId: number) => {
    const playlist = playlists.find(p => p.id === playlistId);
    if (!playlist) return [];
    return songs.filter(s => playlist.song_ids.includes(s.id));
};
