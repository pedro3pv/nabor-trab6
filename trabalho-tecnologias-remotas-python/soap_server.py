# soap_server.py
from spyne import Application, rpc, ServiceBase, Integer, Unicode, Array, ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import data

class SongModel(ComplexModel):
    id = Integer
    title = Unicode
    artist = Unicode

class PlaylistModel(ComplexModel):
    id = Integer
    name = Unicode
    user_id = Integer
    song_ids = Array(Integer)

class UserModel(ComplexModel):
    id = Integer
    name = Unicode
    email = Unicode

class MusicService(ServiceBase):
    @rpc(_returns=Array(UserModel))
    def list_users(ctx):
        return data.get_users()

    @rpc(_returns=Array(SongModel))
    def list_songs(ctx):
        return data.get_songs()

    @rpc(Integer, _returns=Array(PlaylistModel))
    def list_user_playlists(ctx, user_id):
        return data.get_playlists(user_id)
    
    @rpc(Integer, _returns=Array(SongModel))
    def list_playlist_songs(ctx, playlist_id):
        return data.get_playlist_songs(playlist_id)

application = Application([MusicService], 'music.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    print("SOAP Server running on port 8000...")
    server = make_server('0.0.0.0', 8000, WsgiApplication(application))
    server.serve_forever()
