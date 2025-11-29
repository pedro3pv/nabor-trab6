# grpc_server.py
from concurrent import futures
import grpc
import music_service_pb2
import music_service_pb2_grpc
import data

class MusicServicer(music_service_pb2_grpc.MusicServiceServicer):
    def ListUsers(self, request, context):
        response = music_service_pb2.UserList()
        for u in data.get_users():
            response.users.add(id=u['id'], name=u['name'], email=u['email'])
        return response

    def ListSongs(self, request, context):
        response = music_service_pb2.SongList()
        for s in data.get_songs():
            response.songs.add(id=s['id'], title=s['title'], artist=s['artist'])
        return response
    
    def ListUserPlaylists(self, request, context):
        response = music_service_pb2.PlaylistList()
        for p in data.get_playlists(request.id):
            response.playlists.add(id=p['id'], name=p['name'], user_id=p['user_id'], song_ids=p['song_ids'])
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    music_service_pb2_grpc.add_MusicServiceServicer_to_server(MusicServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC Server running on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
