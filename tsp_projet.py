import math
import random
import csv

# Charger les données des villes depuis le fichier CSV
def load_cities_from_csv(filename):
    cities = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            rows = list(csv_reader)
            
            if not rows:
                print("Erreur: Le fichier CSV est vide.")
                return None
            
            # Afficher les colonnes disponibles
            colonnes = list(rows[0].keys())
            print(f"\nColonnes trouvées dans le CSV: {colonnes}")
            
            # Détecter les noms de colonnes (flexibilité)
            name_col = None
            x_col = None
            y_col = None
            
            for col in colonnes:
                col_lower = col.lower().strip()
                if col_lower in ['name', 'nom', 'ville', 'city']:
                    name_col = col
                elif col_lower in ['x', 'x_km']:
                    x_col = col
                elif col_lower in ['y', 'y_km']:
                    y_col = col
            
            if not name_col or not x_col or not y_col:
                print(f"\nErreur: Colonnes requises non trouvées!")
                print(f"  - Colonne nom: {name_col}")
                print(f"  - Colonne x: {x_col}")
                print(f"  - Colonne y: {y_col}")
                return None
            
            print(f"Utilisation des colonnes: '{name_col}', '{x_col}', '{y_col}'")
            
            for idx, row in enumerate(rows):
                city = {
                    'id': idx,
                    'name': row[name_col],
                    'x': float(row[x_col]),
                    'y': float(row[y_col])
                }
                cities.append(city)
            
            print(f"\n{len(cities)} villes chargées avec succès!\n")
        return cities
    except FileNotFoundError:
        print(f"Erreur: Le fichier '{filename}' est introuvable.")
        return None
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

# Charger les villes
cities = load_cities_from_csv('algeria_20_cities_xy.csv')

if cities is None:
    exit(1)

def distance(city1, city2):
    dx = city1['x'] - city2['x']
    dy = city1['y'] - city2['y']
    return math.sqrt(dx * dx + dy * dy)

def total_distance(tour):
    total = 0
    for i in range(len(tour) - 1):
        total += distance(cities[tour[i]], cities[tour[i + 1]])
    total += distance(cities[tour[-1]], cities[tour[0]])
    return total

def random_tour():
    tour = [0]
    autres = list(range(1, len(cities)))
    random.shuffle(autres)
    tour.extend(autres)
    return tour

def swap(tour, i, j):
    new_tour = tour.copy()
    new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
    return new_tour

# 1. RECHERCHE ALÉATOIRE
def recherche_aleatoire():
    print("\n[1/6] Exécution: Recherche Aléatoire...")
    meilleur_trajet = random_tour()
    meilleure_dist = total_distance(meilleur_trajet)
    historique = [meilleure_dist]
    
    for i in range(10000):
        trajet = random_tour()
        dist = total_distance(trajet)
        if dist < meilleure_dist:
            meilleur_trajet = trajet
            meilleure_dist = dist
        historique.append(meilleure_dist)
    
    return meilleur_trajet, meilleure_dist, historique

# 2. RECHERCHE LOCALE
def recherche_locale():
    print("\n[2/6] Exécution: Recherche Locale...")
    trajet = random_tour()
    dist = total_distance(trajet)
    historique = [dist]
    ameliore = True
    
    while ameliore:
        ameliore = False
        for i in range(1, len(trajet) - 1):
            for j in range(i + 1, len(trajet)):
                nouveau_trajet = swap(trajet, i, j)
                nouvelle_dist = total_distance(nouveau_trajet)
                if nouvelle_dist < dist:
                    trajet = nouveau_trajet
                    dist = nouvelle_dist
                    ameliore = True
                    historique.append(dist)
    
    return trajet, dist, historique

# 3. HILL CLIMBING
def hill_climbing():
    print("\n[3/6] Exécution: Hill Climbing...")
    trajet = random_tour()
    dist = total_distance(trajet)
    historique = [dist]
    
    for iter in range(1000):
        meilleur_voisin = None
        meilleur_dist_voisin = dist
        
        for i in range(1, len(trajet) - 1):
            for j in range(i + 1, len(trajet)):
                voisin = swap(trajet, i, j)
                dist_voisin = total_distance(voisin)
                if dist_voisin < meilleur_dist_voisin:
                    meilleur_voisin = voisin
                    meilleur_dist_voisin = dist_voisin
        
        if meilleur_voisin is None:
            break
        trajet = meilleur_voisin
        dist = meilleur_dist_voisin
        historique.append(dist)
    
    return trajet, dist, historique

# 4. RECUIT SIMULÉ
def recuit_simule():
    print("\n[4/6] Exécution: Recuit Simulé...")
    trajet = random_tour()
    dist = total_distance(trajet)
    meilleur_trajet = trajet.copy()
    meilleure_dist = dist
    historique = [dist]
    temperature = 10000
    
    while temperature > 0.01:
        i = random.randint(1, len(trajet) - 1)
        j = random.randint(1, len(trajet) - 1)
        nouveau_trajet = swap(trajet, i, j)
        nouvelle_dist = total_distance(nouveau_trajet)
        
        delta = dist - nouvelle_dist
        
        if delta > 0 or random.random() < math.exp(delta / temperature):
            trajet = nouveau_trajet
            dist = nouvelle_dist
            if dist < meilleure_dist:
                meilleur_trajet = trajet.copy()
                meilleure_dist = dist
        
        historique.append(meilleure_dist)
        temperature *= 0.995
    
    return meilleur_trajet, meilleure_dist, historique

# 5. RECHERCHE TABOU
def recherche_tabou():
    print("\n[5/6] Exécution: Recherche Tabou...")
    trajet = random_tour()
    dist = total_distance(trajet)
    meilleur_trajet = trajet.copy()
    meilleure_dist = dist
    historique = [dist]
    liste_tabou = []
    taille_liste_tabou = 20
    
    for iter in range(1000):
        meilleur_voisin = None
        meilleur_dist_voisin = float('inf')
        meilleur_mouvement = None
        
        for i in range(1, len(trajet) - 1):
            for j in range(i + 1, len(trajet)):
                mouvement = f"{i}-{j}"
                if mouvement not in liste_tabou:
                    voisin = swap(trajet, i, j)
                    dist_voisin = total_distance(voisin)
                    if dist_voisin < meilleur_dist_voisin:
                        meilleur_voisin = voisin
                        meilleur_dist_voisin = dist_voisin
                        meilleur_mouvement = mouvement
        
        if meilleur_voisin:
            trajet = meilleur_voisin
            dist = meilleur_dist_voisin
            liste_tabou.append(meilleur_mouvement)
            if len(liste_tabou) > taille_liste_tabou:
                liste_tabou.pop(0)
            if dist < meilleure_dist:
                meilleur_trajet = trajet.copy()
                meilleure_dist = dist
        
        historique.append(meilleure_dist)
    
    return meilleur_trajet, meilleure_dist, historique

# 6. ALGORITHME GÉNÉTIQUE
def algorithme_genetique():
    print("\n[6/6] Exécution: Algorithme Génétique...")
    taille_population = 100
    generations = 500
    population = [random_tour() for _ in range(taille_population)]
    historique = []
    
    for gen in range(generations):
        nouvelle_population = []
        
        for i in range(taille_population):
            parent1 = random.choice(population)
            parent2 = random.choice(population)
            
            enfant = parent1.copy()
            if random.random() < 0.8:
                debut = random.randint(1, len(parent1) - 2)
                fin = debut + random.randint(1, len(parent1) - debut - 1)
                segment = parent2[debut:fin]
                enfant = [0]
                for gene in segment:
                    if gene != 0:
                        enfant.append(gene)
                for gene in parent1:
                    if gene != 0 and gene not in enfant:
                        enfant.append(gene)
            
            if random.random() < 0.02:
                i = random.randint(1, len(enfant) - 1)
                j = random.randint(1, len(enfant) - 1)
                enfant = swap(enfant, i, j)
            
            nouvelle_population.append(enfant)
        
        population = nouvelle_population
        
        meilleur_gen = population[0]
        meilleure_dist_gen = total_distance(meilleur_gen)
        for trajet in population:
            dist = total_distance(trajet)
            if dist < meilleure_dist_gen:
                meilleur_gen = trajet
                meilleure_dist_gen = dist
        historique.append(meilleure_dist_gen)
    
    meilleur_trajet = population[0]
    meilleure_dist = total_distance(meilleur_trajet)
    for trajet in population:
        dist = total_distance(trajet)
        if dist < meilleure_dist:
            meilleur_trajet = trajet
            meilleure_dist = dist
    
    return meilleur_trajet, meilleure_dist, historique

def afficher_resultat(methode, trajet, distance, historique):
    print("\n" + "="*70)
    print(f"MÉTHODE: {methode}")
    print("="*70)
    print(f"Distance finale: {distance:.2f} km")
    print(f"Nombre d'itérations: {len(historique)}")
    print(f"\nTrajet complet:")
    trajet_noms = [cities[i]['name'] for i in trajet]
    for i, nom in enumerate(trajet_noms, 1):
        print(f"  {i}. {nom}")
    print(f"  {len(trajet_noms)+1}. {cities[0]['name']} (retour)")
    print("="*70)

def main():
    print("\n" + "="*70)
    print("PROJET TSP - 20 VILLES D'ALGÉRIE")
    print("Départ et arrivée: Alger")
    print("="*70)
    
    resultats = []
    
    # Exécuter toutes les méthodes
    methodes = [
        ("Recherche Aléatoire", recherche_aleatoire),
        ("Recherche Locale", recherche_locale),
        ("Hill Climbing", hill_climbing),
        ("Recuit Simulé", recuit_simule),
        ("Recherche Tabou", recherche_tabou),
        ("Algorithme Génétique", algorithme_genetique)
    ]
    
    for nom, fonction in methodes:
        trajet, dist, hist = fonction()
        afficher_resultat(nom, trajet, dist, hist)
        resultats.append((nom, dist))
    
    # Résumé comparatif
    print("\n" + "="*70)
    print("RÉSUMÉ COMPARATIF")
    print("="*70)
    resultats.sort(key=lambda x: x[1])
    for i, (methode, distance) in enumerate(resultats, 1):
        print(f"{i}. {methode:<25} : {distance:.2f} km")
    print("="*70)

if __name__ == "__main__":
    main()