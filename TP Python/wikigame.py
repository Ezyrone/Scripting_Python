import tkinter as tk
from tkinter import messagebox, ttk
import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote

WIKI_BASE_URL = 'https://fr.wikipedia.org/wiki/'
GAME_DURATION = 10 * 60 * 1000  # Durée du jeu de 10 minutes

class WikiGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("WikiGame")
        
        self.start_page_name = ""
        self.target_page_name = ""
        self.current_page_name = ""
        self.start_time = None
        self.moves_count = 0  # Compteur de coups
        self.difficulty = tk.StringVar()
        self.difficulty.set("Facile")  # Niveau de difficulté par défaut
        
        self.create_widgets()
    
    def create_widgets(self):
        self.label_title = tk.Label(self.root, text="WikiGame", font=("Arial", 18))
        self.label_title.pack(pady=10)
        
        self.button_start = tk.Button(self.root, text="Démarrer", command=self.start_game)
        self.button_start.pack()
        
        self.label_start = tk.Label(self.root, text="", font=("Arial", 12))
        self.label_start.pack()
        
        self.label_target = tk.Label(self.root, text="", font=("Arial", 12))
        self.label_target.pack()
        
        self.label_current = tk.Label(self.root, text="", font=("Arial", 12))
        self.label_current.pack(pady=10)
        
        self.listbox_links = tk.Listbox(self.root, width=80, height=15)
        self.listbox_links.pack(pady=10)
        
        self.button_choose = tk.Button(self.root, text="Choisir", command=self.choose_link)
        self.button_choose.pack()
        
        self.label_moves = tk.Label(self.root, text="Coups : 0", font=("Arial", 12))
        self.label_moves.pack(pady=10)
        
        self.label_timer = tk.Label(self.root, text="Temps restant : 10:00", font=("Arial", 12))
        self.label_timer.pack(pady=10)
        
        self.optionmenu_difficulty = ttk.OptionMenu(self.root, self.difficulty, "Facile", "Facile", "Moyen", "Difficile")
        self.optionmenu_difficulty.pack(pady=10)
        
        self.button_reset = tk.Button(self.root, text="Réinitialiser", command=self.reset_game)
        self.button_reset.pack(pady=10)
        
        self.button_quit = tk.Button(self.root, text="Quitter", command=self.root.quit)
        self.button_quit.pack(pady=10)
    
    def start_game(self):
        difficulty_level = self.difficulty.get()
        self.start_page_name = self.get_random_page(difficulty_level)
        self.target_page_name = self.get_random_page(difficulty_level)
        self.current_page_name = self.start_page_name
        self.show_current_page()
        self.start_timer(GAME_DURATION)
    
    def get_random_page(self, difficulty_level):
        if difficulty_level == "Facile":
            # Obtenir une page Wikipédia aléatoire directement
            response = requests.get('https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard')
            page_title = response.url.split('/')[-1]
            return unquote(page_title)
        elif difficulty_level == "Moyen":
            # Obtenir une page à partir d'une catégorie aléatoire
            random_category = random.choice(["Physique", "Biologie", "Géographie"])
            url = f"https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard_dans_la_cat%C3%A9gorie_{random_category}"
            response = requests.get(url)
            page_title = response.url.split('/')[-1]
            return unquote(page_title)
        elif difficulty_level == "Difficile":
            # Obtenir une page via un lien interne plus spécifique
            response = requests.get('https://fr.wikipedia.org/wiki/Wikip%C3%A9dia:Accueil_principal')
            soup = BeautifulSoup(response.content, 'html.parser')
            link_div = soup.find("div", {"id": "mp-itn"})
            link = link_div.find("a", href=True)
            page_title = link['href'].split('/')[-1]
            return unquote(page_title)
        else:
            raise ValueError("Niveau de difficulté non reconnu")

    def get_page_links(self, page_title):
        # Obtenir les liens d'une page Wikipédia
        url = f'{WIKI_BASE_URL}{page_title}'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        content_div = soup.find(id='bodyContent')
        links = content_div.find_all('a', href=True)
        page_links = {unquote(link.get_text()): unquote(link['href'].split('/')[-1]) for link in links if link['href'].startswith('/wiki/') and ':' not in link['href']}
        return page_links
    
    def show_current_page(self):
        self.label_start.config(text=f"Départ : {self.start_page_name.replace('_', ' ')}")
        self.label_target.config(text=f"Cible : {self.target_page_name.replace('_', ' ')}")
        self.label_current.config(text=f"Actuellement : {self.current_page_name.replace('_', ' ')}")
        self.show_links()
    
    def show_links(self):
        self.listbox_links.delete(0, tk.END)
        links = self.get_page_links(self.current_page_name)
        for link_name in links.keys():
            self.listbox_links.insert(tk.END, link_name)
    
    def choose_link(self):
        try:
            index = self.listbox_links.curselection()[0]
            link_names = list(self.get_page_links(self.current_page_name).keys())
            new_page_name = self.get_page_links(self.current_page_name)[link_names[index]]
            self.current_page_name = new_page_name
            self.show_current_page()
            self.moves_count += 1  # Incrémentation du compteur de coups
            self.label_moves.config(text=f"Coups : {self.moves_count}")
            if self.current_page_name == self.target_page_name:
                self.stop_timer()
                self.calculate_score()
        except IndexError:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un lien.")

    def start_timer(self, duration):
        self.remaining_time = duration
        self.start_time = self.remaining_time
        self.update_timer()

    def update_timer(self):
        minutes = self.remaining_time // 60000
        seconds = (self.remaining_time // 1000) % 60
        self.label_timer.config(text=f"Temps restant : {minutes:02}:{seconds:02}")
        
        if self.remaining_time <= 0:
            self.stop_timer()
            messagebox.showinfo("Temps écoulé", "Temps écoulé ! La partie est terminée.")
            self.show_score(0)
        else:
            self.remaining_time -= 1000
            self.root.after(1000, self.update_timer)

    def stop_timer(self):
        self.remaining_time = 0

    # Calculer le score du joueur (potentiellement à modifier)
    def calculate_score(self):
        if self.moves_count > 0:
            score = 10000 // self.moves_count
        else:
            score = 0
        self.show_score(score)

    def show_score(self, score):
        messagebox.showinfo("Score", f"Votre score est de : {score} points.")

    def reset_game(self):
        self.start_page_name = ""
        self.target_page_name = ""
        self.current_page_name = ""
        self.start_time = None
        self.moves_count = 0
        self.label_start.config(text="")
        self.label_target.config(text="")
        self.label_current.config(text="")
        self.listbox_links.delete(0, tk.END)
        self.label_moves.config(text="Coups : 0")
        self.label_timer.config(text="Temps restant : 10:00")
    
if __name__ == "__main__":
    root = tk.Tk()
    app = WikiGameGUI(root)
    root.mainloop()
