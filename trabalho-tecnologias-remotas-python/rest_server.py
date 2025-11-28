# rest_server.py
from fastapi import FastAPI
from typing import List, Optional
from pydantic import BaseModel
import data

app = FastAPI()

class Song(BaseModel):
    id: int
    title: str
    artist: str

class Playlist(BaseModel):
    id: int
    name: str
    user_id: int
    song_ids: List[int]

class User(BaseModel):
    id: int
    name: str
    email: str

@app.get("/users", response_model=List[User])
def get_users():
    return data.get_users()

@app.get("/songs", response_model=List[Song])
def get_songs():
    return data.get_songs()

@app.get("/users/{user_id}/playlists", response_model=List[Playlist])
def get_user_playlists(user_id: int):
    return data.get_playlists(user_id)

@app.get("/playlists/{playlist_id}/songs", response_model=List[Song])
def get_playlist_songs(playlist_id: int):
    return data.get_playlist_songs(playlist_id)

if __name__ == '__main__':
    import uvicorn
    print("REST Server running on port 8001...")
    uvicorn.run(app, host="0.0.0.0", port=8001)
