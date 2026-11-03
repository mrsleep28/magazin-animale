

from urllib.parse import urlparse

from django.http import HttpResponse
from django.shortcuts import render
from django.utils import html, timezone
from django.utils.dateformat import format as format_data
from .models import Produs
# Create your views here.


class Accesare:
    urmatorul_id = 1

    def __init__(self, ip_client, url, parametri=None,):
        # Fiecare obiect primește un id nou.
        self.id = Accesare.urmatorul_id
        Accesare.urmatorul_id += 1

        self.ip_client = ip_client
        self.url = url

        # Dacă nu primim parametri, folosim un dicționar gol.
        self.parametri = {} if parametri is None else parametri

        # Salvăm momentul în care a fost creat obiectul.
        self.data = timezone.now()
        
        

    def lista_parametri(self):
        """Returnează parametrii sub forma unei liste de tupluri."""
        return list(self.parametri.items())

    def string_url(self):
        """Returnează URL-ul complet, inclusiv query string-ul."""
        return self.url

    def pagina(self):
        """Returnează doar calea paginii, fără domeniu și parametri."""
        return urlparse(self.url).path or "/"

    def calculeaza_data(self, tip="", format="%A, %-d %B %Y"):
        """Returnează secțiunea HTML cu data accesării, în română."""
        if tip == "zi":
            format = "%-d %B %Y"
        elif tip == "timp":
            format = "%H:%M:%S"

        data_formatata = timezone.localtime(self.data).strftime(format)

        zile = {
            "Monday": "Luni",
            "Tuesday": "Marți",
            "Wednesday": "Miercuri",
            "Thursday": "Joi",
            "Friday": "Vineri",
            "Saturday": "Sâmbătă",
            "Sunday": "Duminică",
        }
        luni = {
            "January": "Ianuarie",
            "February": "Februarie",
            "March": "Martie",
            "April": "Aprilie",
            "May": "Mai",
            "June": "Iunie",
            "July": "Iulie",
            "August": "August",
            "September": "Septembrie",
            "October": "Octombrie",
            "November": "Noiembrie",
            "December": "Decembrie",
        }

        for nume_englezesc, nume_romanesc in {**zile, **luni}.items():
            data_formatata = data_formatata.replace(
                nume_englezesc, nume_romanesc
            )

        return f"<section><h2>Data și ora</h2><p>{data_formatata}</p></section>"

    def __str__(self):
        return (
            f"id: {self.id}\n"
            f"ip_client: {self.ip_client}\n"
            f"string_url: {self.string_url()}\n"
            f"pagina: {self.pagina()}\n"
            f"calculeaza_data: {self.calculeaza_data()}\n"
            f"lista_parametri: {self.lista_parametri()}"
        )

lista_accesari = []
def inregistreaza_accesarea(request):
    """Creează o înregistrare pentru cererea primită."""
    accesare = Accesare(
        ip_client=request.ip_client,
        url=request.build_absolute_uri(),
        parametri=request.GET.dict(),
    )
    lista_accesari.append(accesare)
    return accesare


def index(request):
    accesare = inregistreaza_accesarea(request)
    print(accesare)
    return render(request, "magazin_clienti/index.html")

def pagina(request):
    accesare = inregistreaza_accesarea(request)
    return render(request, "pagina.html", {"nume_variabila": valoare})

def afisare_sablon(request):
    inregistreaza_accesarea(request)
    context = {
        'titlu_tab': 'Pagina de test',
        'titlu_pagina': 'Bine ati venit!',
        'continut_articol': 'Acesta este un articol de test.',
    }
    return render(request, 'sablon.html', context)  

def info(request):
    accesare = inregistreaza_accesarea(request)
    print(accesare)
    tip_data = request.GET.get("data", "")
    sectiune_data = accesare.calculeaza_data(tip_data)
    return render(request, "magazin_clienti/info.html", {"sectiune_data": sectiune_data})
    
def despre(request):
    inregistreaza_accesarea(request)
    return render(request, "magazin_clienti/despre.html")

def istoric(request):
    inregistreaza_accesarea(request)
    return render(request, "magazin_clienti/istoric.html")

def log(request):
    inregistreaza_accesarea(request)
    html = "<h1>Logul accesărilor</h1>"
    ultimele = request.GET.get("ultimele")
    accesari = request.GET.getlist("accesari")

    dubluri = request.GET.get("dubluri") == "true"
    lista_iduri = []
    for bucata in request.GET.getlist("iduri"):
        for id_text in bucata.split(","):
            try:
                id_nr = int(id_text)
            except ValueError:
                html += "<p>Eroare: Parametrul 'iduri' trebuie să conțină doar numere întregi, separate prin virgulă.</p>"
                return render(request, "magazin_clienti/log.html", {"continut": html})
            if dubluri or id_nr not in lista_iduri:
                lista_iduri.append(id_nr)

    if ultimele is None:
        de_afisat = lista_accesari
    else:
        try:
            n = int(ultimele)
        except ValueError:
            html += "<p>Eroare: Parametrul 'ultimele' trebuie să fie un număr întreg.</p>"
            return render(request, "magazin_clienti/log.html", {"continut": html})
        if n < 1:
            html += "<p>Eroare: Parametrul 'ultimele' trebuie să fie un număr întreg pozitiv.</p>"
            return render(request, "magazin_clienti/log.html", {"continut": html})
        de_afisat = lista_accesari[-n:]

    if len(lista_iduri) > 0:
        gasite = []
        for id_cautat in lista_iduri:
            for a in lista_accesari:
                if a.id == id_cautat:
                    gasite.append(a)
        de_afisat = gasite

    for a in de_afisat:
        html += f"<p>{a.id} - {a.pagina()} - {a.ip_client}</p>"
        
    tabel = request.GET.get("tabel")
    if tabel is not None:
        permise = ["id", "ip_client", "url", "parametri", "data"]
        if tabel == "tot":
            coloane = permise
        else:
            coloane = tabel.split(",")

        for coloana in coloane:
            if coloana not in permise:
                html += f"<p>Eroare: coloana '{coloana}' nu există. Coloanele permise sunt: {permise}</p>"
                return render(request, "magazin_clienti/log.html", {"continut": html})

        html += '<table border="1"><tr>'
        for coloana in coloane:
            html += f"<th>{coloana}</th>"
        html += "</tr>"

        for a in de_afisat:
            html += "<tr>"
            for coloana in coloane:
                if coloana == "data":
                    valoare = timezone.localtime(a.data).strftime("%d.%m.%Y %H:%M:%S")
                else:
                    valoare = getattr(a, coloana)
                html += f"<td>{valoare}</td>"
            html += "</tr>"

        html += "</table>"
    if ultimele is not None and n > len(lista_accesari):
        html += f"<p>Exista doar {len(lista_accesari)} accesari fata de {n} accesari cerute</p>"

    if "nr" in accesari:
        html += f"<section><h2>Număr de accesări</h2><p>{len(lista_accesari)}</p></section>"
    
    if "detalii" in accesari:
        html += "<section><h2>Detalii accesări</h2><ul>"
        for a in lista_accesari:
            data_ora = timezone.localtime(a.data).strftime("%d.%m.%Y %H:%M:%S")
            html += f"<li>{data_ora}</li>"
        html += "</ul></section>"
    
    numarare = {}
    for a in lista_accesari:
        pagina = a.pagina()
        if pagina in numarare:
            numarare[pagina] += 1
        else:
            numarare[pagina] = 1

    cea_mai = None
    cea_mai_putin = None
    for pagina in numarare:
        if cea_mai is None or numarare[pagina] > numarare[cea_mai]:
            cea_mai = pagina
        if cea_mai_putin is None or numarare[pagina] < numarare[cea_mai_putin]:
            cea_mai_putin = pagina

    html += f"<p>Cea mai accesată pagină: {cea_mai} ({numarare[cea_mai]} accesări)</p>"
    html += f"<p>Cea mai puțin accesată pagină: {cea_mai_putin} ({numarare[cea_mai_putin]} accesări)</p>"
    html += f"<section><h2>Parametri</h2><p>Numar parametri: {len(request.GET)}</p><ul>"
    for parametru in request.GET:
        html += f"<li>{parametru}</li>"
    html += "</ul></section>"
    return render(request, "magazin_clienti/log.html", {"continut": html})

def accesare(request, id):
    inregistreaza_accesarea(request)
    id_cautat = int(id)
    gasita = None
    for a in lista_accesari:
        if a.id == id_cautat:
            gasita = a
    if gasita is None:
        html = f"<h1>Accesarea {id_cautat}</h1><p>Nu există nicio accesare cu id-ul {id_cautat}.</p>"
        return render(request, "magazin_clienti/accesare.html", {"continut": html})

    data_ora = timezone.localtime(gasita.data).strftime("%d.%m.%Y %H:%M:%S")
    html = f"<h1>Accesarea {gasita.id}</h1>"
    html += "<ul>"
    html += f"<li>id: {gasita.id}</li>"
    html += f"<li>ip_client: {gasita.ip_client}</li>"
    html += f"<li>url: {gasita.string_url()}</li>"
    html += f"<li>pagina: {gasita.pagina()}</li>"
    html += f"<li>parametri: {gasita.lista_parametri()}</li>"
    html += f"<li>data: {data_ora}</li>"
    html += "</ul>"
    return render(request, "magazin_clienti/accesare.html", {"continut": html})

def produse(request):
    inregistreaza_accesarea(request)
    lista = Produs.objects.all()
    return render(request, "magazin_clienti/produse.html", {"produse": lista})

def contact(request):
    inregistreaza_accesarea(request)
    return render(request, "magazin_clienti/in_lucru.html")
def cos_virtual(request):
    inregistreaza_accesarea(request)
    return render(request, "magazin_clienti/in_lucru.html")
def sfaturi(request):
    inregistreaza_accesarea(request)
    return render(request, "magazin_clienti/in_lucru.html")
def promotii(request):
    inregistreaza_accesarea(request)
    return render(request, "magazin_clienti/in_lucru.html") 

def pagina_produs(request, id):
    inregistreaza_accesarea(request)
    try:
        produs = Produs.objects.get(id=id)
    except Produs.DoesNotExist:
        return render(request, "magazin_clienti/produs_inexistent.html", {"id": id}, status=404)
    similare = Produs.objects.filter(categorie=produs.categorie).exclude(id=produs.id).order_by("?")[:4]
    return render(request, "magazin_clienti/pagina_produs.html", {"produs": produs, "similare": similare})
