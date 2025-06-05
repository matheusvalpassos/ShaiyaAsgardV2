import socket
from django.shortcuts import render
from .models import Char, NewsUpdate
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
    return render(request, "asgard/register.html")


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
    return HttpResponseNotFound(render(request, "404.html"))


def register_view(request):
    # Pegando idioma do cookie
    lang = request.COOKIES.get("lang", "en")  # 'en' como padrão
    return render(request, "register.html", {"lang": lang})
