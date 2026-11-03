from django.contrib import admin
from django.utils.html import format_html
from .models import Specie, Brand, Categorie, Sediu, Raion, Produs
import csv
from django.http import HttpResponse

admin.site.site_title = "Blăniță - Admin"
admin.site.site_header = "Administrare Blăniță"
admin.site.index_title = "Panou de control al magazinului"
admin.site.site_url = "/"

class SpecieAdmin(admin.ModelAdmin):
    list_display = ["nume", "descriere"]
    search_fields = ["nume", "descriere"]
    search_help_text = "Caută după numele speciei sau după descriere."


class BrandAdmin(admin.ModelAdmin):
    list_display = ["nume", "tara_origine", "site_web"]
    search_fields = ["nume", "tara_origine"]
    search_help_text = "Caută după numele brandului sau după țara de origine."

class CategorieAdmin(admin.ModelAdmin):
    list_display = ["nume", "culoare", "ordine_afisare"]
    search_fields = ["nume", "descriere"]
    search_help_text = "Caută după numele categoriei sau după descriere."

class SediuAdmin(admin.ModelAdmin):
    list_display = ["nume", "adresa", "telefon", "email"]
    search_fields = ["nume", "adresa"]
    search_help_text = "Caută după numele sediului sau după adresă."


class RaionAdmin(admin.ModelAdmin):
    list_display = ["denumire", "sediu", "sediu__adresa", "sediu__telefon", "numar_raion", "etaj"]
    list_filter = ["sediu"]
    search_fields = ["denumire", "sediu__nume"]
    search_help_text = "Caută după denumirea raionului sau după numele sediului."


class ProdusAdmin(admin.ModelAdmin):
    list_display = ["nume", "categorie", "brand", "pret_colorat", "stoc", "disponibil", "data_adaugare"]
    list_filter = ["categorie", "disponibil", "varsta_recomandata"]
    search_fields = ["nume", "descriere"]
    search_help_text = "Caută după numele produsului sau după descriere."
    actions = ["marcheaza_disponibilitate", "exporta_csv"]
    ordering = ["pret"]
    list_per_page = 5
    fieldsets = [
            ("Date principale", {
                "fields": ["nume", "categorie", "specii", "pret", "stoc", "disponibil", "varsta_recomandata"],
            }),
            ("Detalii suplimentare", {
                "fields": ["brand", "descriere", "greutate", "taguri", "imagine"],
                "classes": ["collapse"],
            }),
        ]
    
    @admin.display(description="Preț", ordering="pret")
    def pret_colorat(self, obj):
        return format_html('<b style="color: {};">{} lei</b>', "#E8833A", obj.pret)
    
    @admin.action(description="Marchează produsele selectate ca indisponibile/dispnibile")
    def marcheaza_disponibilitate(self, request, queryset):
        if queryset.filter(disponibil=True) and queryset.filter(disponibil=False):
            return self.message_user(request, "Nu se pot marca produsele selectate deoarece unele sunt disponibile și altele indisponibile.")
        if queryset.filter(disponibil=True):
            numar = queryset.filter(disponibil=True).update(disponibil=False)
            self.message_user(request, f"{numar} produse au fost marcate ca indisponibile.")
        else:
            numar = queryset.filter(disponibil=False).update(disponibil=True)   
            self.message_user(request, f"{numar} produse au fost marcate ca disponibile.")
    

    @admin.action(description="Exportă produsele selectate în CSV")
    def exporta_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = 'attachment; filename="produse.csv"'
        response.write("\ufeff")
        writer = csv.writer(response)
        writer.writerow(["Nume", "Categorie", "Brand", "Preț", "Stoc", "Disponibil"])
        for produs in queryset:
            writer.writerow([produs.nume, produs.categorie, produs.brand, produs.pret, produs.stoc, produs.disponibil])
        return response


admin.site.register(Specie, SpecieAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Categorie, CategorieAdmin)
admin.site.register(Sediu, SediuAdmin)
admin.site.register(Raion, RaionAdmin)
admin.site.register(Produs, ProdusAdmin)