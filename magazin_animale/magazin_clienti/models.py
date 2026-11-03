from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Specie(models.Model):
    nume = models.CharField(
        max_length=30,
        unique=True,
        help_text="Animalul pentru care sunt produsele, de exemplu câine sau pisică.",
        error_messages={
            "unique": "Există deja o specie cu acest nume.",
            "max_length": "Numele speciei poate avea maxim 30 de caractere.",
        },
    )
    descriere = models.TextField(
        null=True,
        blank=True,
        help_text="Câteva cuvinte despre specie (opțional).",
    )

    class Meta:
        ordering = ["nume"]
        verbose_name = "specie"
        verbose_name_plural = "specii"

    def __str__(self):
        return self.nume
    
    
class Brand(models.Model):
    nume = models.CharField(
        max_length=50,
        unique=True,
        error_messages={
            "unique": "Există deja un brand cu acest nume.",
            "max_length": "Numele brandului poate avea maxim 50 de caractere.",
        },
    )
    tara_origine = models.CharField(
        max_length=40,
        default="România",
        blank=True,
        help_text="Țara din care provine brandul.",
    )
    site_web = models.URLField(
        null=True,
        blank=True,
        help_text="Adresa completă, cu https://",
        error_messages={
            "invalid": "Adresa site-ului nu e validă. Exemplu: https://www.royalcanin.com",
        },
    )

    class Meta:
        ordering = ["nume"]
        verbose_name = "brand"
        verbose_name_plural = "branduri"

    def __str__(self):
        return self.nume
    
class Categorie(models.Model):
    nume = models.CharField(
        max_length=40,
        unique=True,
        error_messages={
            "unique": "Există deja o categorie cu acest nume.",
        },
    )
    descriere = models.TextField(null=True, blank=True)
    culoare = models.CharField(
        max_length=7,
        default="#8B5E3C",
        help_text="Cod de culoare, de exemplu #E8833A. Se folosește la afișarea produselor din categorie.",
    )
    sigla = models.ImageField(
        upload_to="categorii/",
        null=True,
        blank=True,
        help_text="Imaginea afișată lângă numele categoriei.",
    )
    ordine_afisare = models.PositiveIntegerField(
        default=0,
        help_text="Categoriile cu un număr mai mic apar primele.",
    )

    class Meta:
        ordering = ["ordine_afisare", "nume"]
        verbose_name = "categorie"
        verbose_name_plural = "categorii"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(culoare__startswith="#"),
                name="categorie_culoare_incepe_cu_diez",
            ),
        ]

    def __str__(self):
        return self.nume

class Sediu(models.Model):
    nume = models.CharField(max_length=60)
    adresa = models.CharField(max_length=150)
    telefon = models.CharField(
        max_length=15,
        help_text="Număr de telefon care începe cu 0, de exemplu 0712 345 678.",
    )
    email = models.EmailField(
        null=True,
        blank=True,
        error_messages={
            "invalid": "Adresa de email nu e validă. Exemplu: iasi@blanita.ro",
        },
    )

    class Meta:
        verbose_name = "sediu"
        verbose_name_plural = "sedii"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(telefon__regex=r"^0[0-9 ]+$"),
                name="sediu_telefon_valid",
            ),
        ]

    def __str__(self):
        return self.nume
    
class Raion(models.Model):
    sediu = models.ForeignKey(Sediu, on_delete=models.CASCADE)
    numar_raion = models.PositiveSmallIntegerField()
    denumire = models.CharField(max_length=50)
    etaj = models.IntegerField(
        default=0,
        help_text="0 înseamnă parter, -1 subsol.",
    )

    class Meta:
        ordering = ["sediu", "numar_raion"]
        verbose_name = "raion"
        verbose_name_plural = "raioane"
        constraints = [
            models.UniqueConstraint(
                fields=["sediu", "numar_raion"],
                name="raion_unic_in_sediu",
            ),
            models.CheckConstraint(
                condition=models.Q(numar_raion__gte=1),
                name="raion_numar_pozitiv",
            ),
            models.CheckConstraint(
                condition=models.Q(etaj__gte=-1) & models.Q(etaj__lte=5),
                name="raion_etaj_valid",
            ),
        ]

    def __str__(self):
        return f"{self.sediu} - Raion {self.numar_raion}"
    
class Produs(models.Model):
    VARSTE = [
        ("pui", "Pui"),
        ("adult", "Adult"),
        ("senior", "Senior"),
        ("toate", "Toate vârstele"),
    ]

    categorie = models.ForeignKey(Categorie, on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    specii = models.ManyToManyField(Specie)
    nume = models.CharField(max_length=100)
    descriere = models.TextField(null=True, blank=True)
    pret = models.DecimalField(max_digits=8, decimal_places=2)
    greutate = models.FloatField(
        null=True,
        blank=True,
        help_text="Greutatea în kilograme, de exemplu 2.5",
    )
    stoc = models.PositiveIntegerField(default=0)
    disponibil = models.BooleanField(default=True)
    varsta_recomandata = models.CharField(
        max_length=10,
        choices=VARSTE,
        default="toate",
    )
    data_adaugare = models.DateTimeField(auto_now_add=True)
    taguri = ArrayField(
        models.CharField(max_length=30),
        blank=True,
        default=list,
        help_text="Cuvinte cheie separate prin virgulă, de exemplu: fără cereale, bio",
    )
    imagine = models.ImageField(
        upload_to="produse/",
        null=True,
        blank=True,
        help_text="Poza produsului. Dacă lipsește, se afișează o imagine default.",
    )

    class Meta:
        ordering = ["-data_adaugare"]
        verbose_name = "produs"
        verbose_name_plural = "produse"
        indexes = [
            models.Index(fields=["nume"]),
            models.Index(fields=["pret"]),
            models.Index(fields=["data_adaugare"]),
            models.Index(fields=["varsta_recomandata"]),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(pret__gt=0),
                name="produs_pret_pozitiv",
            ),
            models.CheckConstraint(
                condition=models.Q(greutate__isnull=True) | models.Q(greutate__gt=0),
                name="produs_greutate_pozitiva",
            ),
            models.CheckConstraint(
                condition=models.Q(disponibil=False) | models.Q(stoc__gt=0),
                name="produs_disponibil_doar_cu_stoc",
            ),
        ]

    def __str__(self):
        return self.nume