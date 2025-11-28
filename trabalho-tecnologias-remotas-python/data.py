# data.py
# Simulação de Banco de Dados em Memória

users = [
    {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
    {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'}
]

songs = [
    {'id': 1, 'title': 'Song A', 'artist': 'Artist X'},
    {'id': 2, 'title': 'Song B', 'artist': 'Artist Y'},
    {'id': 3, 'title': 'Song C', 'artist': 'Artist X'}
]

playlists = [
    {'id': 1, 'name': 'Alice Favorites', 'user_id': 1, 'song_ids': [1, 2]},
    {'id': 2, 'name': 'Bob Rock', 'user_id': 2, 'song_ids': [3]}
]

def get_users(): return users
def get_songs(): return songs
def get_playlists(user_id=None):
    if user_id:
        return [p for p in playlists if p['user_id'] == user_id]
    return playlists

def get_playlist_songs(playlist_id):
    pl = next((p for p in playlists if p['id'] == playlist_id), None)
    if not pl: return []
    return [s for s in songs if s['id'] in pl['song_ids']]

def get_playlists_with_song(song_id):
    return [p for p in playlists if song_id in p['song_ids']]
