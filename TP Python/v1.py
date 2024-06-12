import wikipediaapi
import random

# Initialisation de l'API Wikipédia
wiki = wikipediaapi.Wikipedia('en')

def get_random_page():
    # Fonction pour obtenir une page Wikipédia au hasard
    random_page = wiki.random(pages=1)
    return random_page

def get_links(page):
    # Fonction pour obtenir les liens d'une page
    return page.links

def main():
    # Sélectionner deux pages au hasard
    start_page_name = get_random_page()
    target_page_name = get_random_page()
    
    # Charger les pages
    start_page = wiki.page(start_page_name)
    target_page = wiki.page(target_page_name)
    
    if not start_page.exists() or not target_page.exists():
        print("Une des pages sélectionnées n'existe pas. Réessayez.")
        return
    
    print("************************ WikiGame **** tour 1")
    print(f"Départ : {start_page.title}")
    print(f"Cible : {target_page.title}")
    current_page = start_page
    
    # Boucle du jeu
    tour = 1
    while current_page.title != target_page.title:
        print(f"Actuellement : {current_page.title}")
        links = get_links(current_page)
        link_names = list(links.keys())
        
        # Afficher les liens disponibles
        for i, link in enumerate(link_names):
            print(f"{i + 1:02d} - {link}")
        
        # Demander à l'utilisateur de choisir un lien
        choice = int(input("Votre choix: ")) - 1
        if choice < 0 or choice >= len(link_names):
            print("Choix invalide. Réessayez.")
            continue
        
        # Mettre à jour la page actuelle
        current_page = wiki.page(link_names[choice])
        tour += 1
    
    print(f"Félicitations ! Vous avez atteint la page {target_page.title} en {tour} tours.")

if __name__ == "__main__":
    main()
