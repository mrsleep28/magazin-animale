import random
def valoare_sql(valoare):
    if valoare is None:
        return "NULL"
    if isinstance(valoare, bool):
        return "TRUE" if valoare else "FALSE"
    if isinstance(valoare, str):
        return "'" + valoare.replace("'", "''") + "'"
    if isinstance(valoare, list):
        return "ARRAY[" + ", ".join([valoare_sql(t) for t in valoare]) + "]::varchar[]"
    return str(valoare)

tipuri = ["Hrană uscată", "Hrană umedă", "Minge", "Os de ros", "Zgardă", "Lesă", "Pat", "Cușcă", "Acvariu", "Nisip", "Șampon", "Perie", "Jucărie de pluș", "Castron", "Hamac"]
descrieri = ["premium", "pentru talie mică", "din cauciuc", "reglabilă", "eco", "cu aromă de pui", "rezistentă", "deluxe", "mini", "XL"]
etichete = ["bio", "fără cereale", "natural", "rezistent", "pluș", "cauciuc", "premium", "reducere", "nou", "eco", "piele", "pui"]
varste = ["pui", "adult", "senior", "toate"]
categorii = [1, 2, 3, 4, 5]
branduri = [1, 2, 3, 4, 5, None]
texte = [None, "Produs de calitate pentru animalul tău.", "Recomandat de medicii veterinari.", "Ușor de folosit și de curățat.", "Cel mai vândut produs din categorie."]
descriere = random.choice(texte)

with open("inserare_produse.sql", "w", encoding="utf-8") as fisier:
    for i in range(40):
        nume = random.choice(tipuri) + " " + random.choice(descrieri)
        pret = round(random.uniform(5, 300), 2)
        stoc = random.randint(0, 50)
        disponibil = stoc > 0
        greutate = random.choice([None, round(random.uniform(0.1, 15), 2)])
        varsta = random.choice(varste)
        categorie = random.choice(categorii)
        brand = random.choice(branduri)
        taguri = random.sample(etichete, random.randint(1, 3))
        descriere = random.choice(texte)

        comanda = (
            "INSERT INTO magazin_clienti_produs "
            "(nume, descriere, pret, greutate, stoc, disponibil, varsta_recomandata, data_adaugare, taguri, brand_id, categorie_id) "
            f"VALUES ({valoare_sql(nume)}, {valoare_sql(descriere)}, {valoare_sql(pret)}, {valoare_sql(greutate)}, "
            f"{valoare_sql(stoc)}, {valoare_sql(disponibil)}, {valoare_sql(varsta)}, NOW(), "
            f"{valoare_sql(taguri)}, {valoare_sql(brand)}, {valoare_sql(categorie)});"
        )
        fisier.write(comanda + "\n")

print("Am generat 40 de produse în inserare_produse.sql")