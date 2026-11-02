from django.urls import path
from django.urls import re_path
from . import views

urlpatterns = [
	path("", views.index, name="index"),
    path("pagina/", views.pagina, name="pagina"),   
    path("afisare_sablon/", views.afisare_sablon, name="afisare_sablon"),
    path("info", views.info, name="info"),
    path("info/", views.info, name="info_cu_slash"),
    path("istoric", views.istoric, name="istoric"),
    path("log", views.log, name="log"),
    path("despre", views.despre, name="despre"),
    re_path(r"^accesare(?P<id>\d+)$", views.accesare, name="accesare"),
    path("produse/", views.produse, name="produse"),
    path("contact/", views.contact, name="contact"),
    path("cos_virtual/", views.cos_virtual, name="cos_virtual"),
    path("sfaturi/", views.sfaturi, name="sfaturi"),
    path("promotii/", views.promotii, name="promotii"),
]