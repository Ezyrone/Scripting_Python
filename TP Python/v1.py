import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote

WIKI_BASE_URL = 'https://fr.wikipedia.org/wiki/'
GAME_DURATION = 10 * 60 * 1000  # Durée du jeu en millisecondes (10 minutes)

class WikiGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("WikiGame")
        
        self.start_page_name = self.get_random_page()
        self.target_page_name = self.get_random_page()
        self.current_page_name = self.start_page_name
        
        self.create_widgets()
        self.show_current_page()
        self.start_timer(GAME_DURATION)
    
    def create_widgets(self):
        self.label_title = tk.Label(self.root, text="WikiGame", font=("Arial", 18))
        self.label_title.pack(pady=10)
        
        self.label_start = tk.Label(self.root, text=f"Départ : {self.start_page_name.replace('_', ' ')}", font=("Arial", 12))
        self.label_start.pack()
        
        self.label_target = tk.Label(self.root, text=f"Cible : {self.target_page_name.replace('_', ' ')}", font=("Arial", 12))
        self.label_target.pack()
        
        self.label_current = tk.Label(self.root, text=f"Actuellement : {self.current_page_name.replace('_', ' ')}", font=("Arial", 12))
        self.label_current.pack(pady=10)
        
        self.listbox_links = tk.Listbox(self.root, width=80, height=15)
        self.listbox_links.pack(pady=10)
        
        self.button_choose = tk.Button(self.root, text="Choisir", command=self.choose_link)
        self.button_choose.pack()
        
        self.label_timer = tk.Label(self.root, text="Temps restant : 10:00", font=("Arial", 12))
        self.label_timer.pack(pady=10)
        
        self.show_links()
    
    def get_random_page(self):
        # Obtenir une page Wikipédia aléatoire
        response = requests.get('https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard')
        page_title = response.url.split('/')[-1]
        return unquote(page_title)
    
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
            if self.current_page_name == self.target_page_name:
                self.stop_timer()
                messagebox.showinfo("Félicitations", f"Vous avez atteint la page {self.target_page_name.replace('_', ' ')} !")
        except IndexError:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un lien.")

    def start_timer(self, duration):
        self.remaining_time = duration
        self.update_timer()

    def update_timer(self):
        minutes = self.remaining_time // 60000
        seconds = (self.remaining_time // 1000) % 60
        self.label_timer.config(text=f"Temps restant : {minutes:02}:{seconds:02}")
        
        if self.remaining_time <= 0:
            messagebox.showinfo("Temps écoulé", "Temps écoulé ! La partie est terminée.")
            self.root.quit()
        else:
            self.remaining_time -= 1000
            self.root.after(1000, self.update_timer)

    def stop_timer(self):
        self.remaining_time = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = WikiGameGUI(root)
    root.mainloop()
