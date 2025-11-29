# locustfile.py
from locust import HttpUser, task, between

class MusicStreamingUser(HttpUser):
    wait_time = between(1, 2)

    @task(3)
    def list_users(self):
        self.client.get("/users")

    @task(3)
    def list_songs(self):
        self.client.get("/songs")

    @task(1)
    def view_playlist(self):
        # Exemplo simulando acesso a playlist do usuário 1
        self.client.get("/users/1/playlists")
