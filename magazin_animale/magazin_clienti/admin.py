from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Specie, Brand, Categorie, Sediu, Raion, Produs


class SpecieAdmin(admin.ModelAdmin):
    list_display = ["nume", "descriere"]


class BrandAdmin(admin.ModelAdmin):
    list_display = ["nume", "tara_origine", "site_web"]


class CategorieAdmin(admin.ModelAdmin):
    list_display = ["nume", "culoare", "ordine_afisare"]


class SediuAdmin(admin.ModelAdmin):
    list_display = ["nume", "adresa", "telefon", "email"]


class RaionAdmin(admin.ModelAdmin):
    list_display = ["denumire", "sediu", "numar_raion", "etaj"]
    list_filter = ["sediu"]


class ProdusAdmin(admin.ModelAdmin):
    list_display = ["nume", "categorie", "brand", "pret", "stoc", "disponibil", "data_adaugare"]
    list_filter = ["categorie", "disponibil", "varsta_recomandata"]
    search_fields = ["nume"]


admin.site.register(Specie, SpecieAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Categorie, CategorieAdmin)
admin.site.register(Sediu, SediuAdmin)
admin.site.register(Raion, RaionAdmin)
admin.site.register(Produs, ProdusAdmin)