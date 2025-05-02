# helpers.py
import socket
from django.db import connections


class ServerStatusChecker:
    def __init__(self, host, login_port=30800, game_port=30810):
        self.host = host
        self.login_port = login_port
        self.game_port = game_port

    def is_server_online(self, port):
        """Verifica se uma porta específica está ativa."""
        try:
            with socket.create_connection((self.host, port), timeout=5):
                return True
        except (socket.timeout, ConnectionRefusedError, OSError) as e:
            print(f"Erro ao conectar em {self.host}:{port}: {str(e)}")
            return False

    def get_status(self):
        """Retorna o status geral do servidor (online/offline)."""
        login_online = self.is_server_online(self.login_port)
        game_online = self.is_server_online(self.game_port)
        return "online" if (login_online and game_online) else "offline"

    def get_database_status(self, db_alias):
        """Verifica se um banco de dados está acessível."""
        try:
            connections[db_alias].ensure_connection()
            return True
        except Exception as e:
            print(f"Erro no banco {db_alias}: {str(e)}")
            return False
