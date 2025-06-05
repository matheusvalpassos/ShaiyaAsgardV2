from django_ckeditor_5.fields import CKEditor5Field
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    pass


class NewsUpdate(models.Model):
    LABEL_CHOICES = [
        ("NEWS", "News"),
        ("FIX", "Updates"),
        ("EVENT", "Event"),
    ]

    # Campos do modelo
    title = models.CharField("Título", max_length=200)
    content = models.TextField("Conteúdo")
    redirect_link = models.URLField("Link de Redirecionamento", blank=True)
    published_date = models.DateTimeField("Data de Publicação", default=timezone.now)
    is_active = models.BooleanField("Ativo", default=True)
    image = models.ImageField("Imagem", upload_to="news/", blank=True, null=True)
    label = models.CharField(
        max_length=10, choices=LABEL_CHOICES, default="NEWS", blank=True, null=True
    )

    class Meta:
        verbose_name = "Noticia"
        verbose_name_plural = "Noticias"
        ordering = ["-published_date"]

    def __str__(self):
        return self.title


class Char(models.Model):
    # Mapeie os nomes das colunas do MSSQL
    name = models.CharField(max_length=50, db_column="CharName")  # CharName no MSSQL
    char_class = models.IntegerField(db_column="char_class")  # char_class no MSSQL
    level = models.SmallIntegerField(db_column="Level")  # Level no MSSQL
    kills = models.IntegerField(db_column="K1")  # K1 = kills
    deaths = models.IntegerField(db_column="K2")  # K2 = deaths

    @property
    def kdr(self):
        return round(
            self.kills / max(1, self.deaths), 3
        )  # Adicione round para formatar [[3]]

    @property
    def rank_img(self):
        # Mantenha a lógica do PHP (kill count define a imagem)
        if self.kills >= 200000:
            return 16
        elif self.kills >= 150000:
            return 15
        elif self.kills >= 130000:
            return 14
        elif self.kills >= 110000:
            return 13
        elif self.kills >= 90000:
            return 12
        elif self.kills >= 70000:
            return 11
        elif self.kills >= 50000:
            return 10
        elif self.kills >= 40000:
            return 9
        elif self.kills >= 30000:
            return 8
        elif self.kills >= 20000:
            return 7
        elif self.kills >= 10000:
            return 6
        elif self.kills >= 5000:
            return 5
        elif self.kills >= 1000:
            return 4
        elif self.kills >= 300:
            return 3
        elif self.kills >= 50:
            return 2
        elif self.kills >= 1:
            return 1
        return 0

    class Meta:
        managed = False
        db_table = "chars"
        ordering = ["-kills"]


class ServerStatus(models.Model):
    is_online = models.BooleanField(default=False, verbose_name="Servidor Online?")
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Status do Servidor"
        verbose_name_plural = "Status do Servidor"

    def __str__(self):
        return "Online" if self.is_online else "Offline"
