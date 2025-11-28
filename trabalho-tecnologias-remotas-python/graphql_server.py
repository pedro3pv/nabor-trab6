# graphql_server.py
import strawberry
from typing import List
import data

@strawberry.type
class Song:
    id: int
    title: str
    artist: str

@strawberry.type
class Playlist:
    id: int
    name: str
    user_id: int
    song_ids: List[int]

    @strawberry.field
    def songs(self) -> List[Song]:
        return [Song(**s) for s in data.get_playlist_songs(self.id)]

@strawberry.type
class User:
    id: int
    name: str
    email: str

    @strawberry.field
    def playlists(self) -> List[Playlist]:
        raw_playlists = data.get_playlists(self.id)
        return [Playlist(id=p['id'], name=p['name'], user_id=p['user_id'], song_ids=p['song_ids']) for p in raw_playlists]

@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> List[User]:
        return [User(**u) for u in data.get_users()]

    @strawberry.field
    def songs(self) -> List[Song]:
        return [Song(**s) for s in data.get_songs()]

schema = strawberry.Schema(query=Query)

if __name__ == '__main__':
    import uvicorn
    from strawberry.asgi import GraphQL
    print("GraphQL Server running on port 8002...")
    graphql_app = GraphQL(schema)
    uvicorn.run(graphql_app, host="0.0.0.0", port=8002)
