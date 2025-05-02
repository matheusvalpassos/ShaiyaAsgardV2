import socket
from django.shortcuts import render
from .models import Char, NewsUpdate, ServerStatus
from django.views.generic import ListView
from django.http import HttpResponseNotFound


def home(request):
    updates = (
        NewsUpdate.objects.using("default")
        .filter(is_active=True)
        .order_by("-published_date")[:3]
    )

    return render(request, "home.html", {"news_updates": updates})


def register(request):
    return render(request, "accounts/register.html")


def is_server_online(host, port, timeout=10):
    """Verifica se uma porta específica está ativa no servidor."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError) as e:
        print(f"Erro ao conectar em {host}:{port}: {str(e)}")
        return False


def server_status_view(request):
    try:
        # Obtém o status manual (se existir)
        server_status_obj = ServerStatus.objects.get()
        server_status = "online" if server_status_obj.is_online else "offline"
    except ServerStatus.DoesNotExist:
        # Fallback para verificação automática (caso não tenha registro)
        server = "144.217.146.55"
        port_login = 30800
        port_game = 30810
        login_online = is_server_online(server, port_login)
        game_online = is_server_online(server, port_game)
        server_status = "online" if (login_online and game_online) else "offline"

    context = {"server_status": server_status}
    return render(request, "server_status.html", context)


class NewsUpdateView(ListView):
    model = NewsUpdate
    template_name = "news.html"  # Template dedicado para notícias
    context_object_name = "news_updates"
    queryset = (
        NewsUpdate.objects.using("default")
        .filter(is_active=True)
        .order_by("-published_date")[:3]
    )


def pvp_ranking(request):
    top_25_players = Char.objects.all().order_by("-kills")[:25]
    return render(request, "ranking/pvp.html", {"players": top_25_players})

def error_404_view(request):
    return HttpResponseNotFound(render(request, '404.html'))