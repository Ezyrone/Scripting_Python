# pylint: disable=import-error
import requests
from bs4 import BeautifulSoup

WIKI_BASE_URL = 'https://fr.wikipedia.org/wiki/'

def get_random_page():
    # Obtenir une page Wikipédia aléatoire
    response = requests.get('https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard')
    return response.url.split('/')[-1]

def get_page_links(page_title):
    # Obtenir les liens d'une page Wikipédia
    url = f'{WIKI_BASE_URL}{page_title}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    content_div = soup.find(id='bodyContent')
    links = content_div.find_all('a', href=True)
    page_links = {link.get_text(): link['href'].split('/')[-1] for link in links if link['href'].startswith('/wiki/') and ':' not in link['href']}
    return page_links

def main():
    # Sélectionner deux pages au hasard
    start_page_name = get_random_page()
    target_page_name = get_random_page()
    
    print("************************ WikiGame **** tour 1")
    print(f"Départ : {start_page_name.replace('_', ' ')}")
    print(f"Cible : {target_page_name.replace('_', ' ')}")
    current_page_name = start_page_name
    
    # Boucle du jeu
    tour = 1
    while current_page_name != target_page_name:
        print(f"Actuellement : {current_page_name.replace('_', ' ')}")
        links = get_page_links(current_page_name)
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
        current_page_name = links[link_names[choice]]
        tour += 1
    
    print(f"Félicitations ! Vous avez atteint la page {target_page_name.replace('_', ' ')} en {tour} tours.")

if __name__ == "__main__":
    main()
