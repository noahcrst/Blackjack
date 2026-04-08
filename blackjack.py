import tkinter as tk
from tkinter import messagebox
import random

# ==========================================
# PARTIE BACKEND & LOGIQUE (ANIL & OUALID)
# ==========================================

class Carte:
    def __init__(self, valeur, couleur):
        self.valeur = valeur
        self.couleur = couleur

    def get_points(self):
        if self.valeur in ['Valet', 'Dame', 'Roi']:
            return 10
        elif self.valeur == 'As':
            return 11 # Géré dynamiquement dans la main
        else:
            return int(self.valeur)

class Sabot:
    def __init__(self):
        couleurs = ['Cœur', 'Carreau', 'Trèfle', 'Pique']
        valeurs = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Valet', 'Dame', 'Roi', 'As']
        self.cartes = [Carte(v, c) for c in couleurs for v in valeurs]
        random.shuffle(self.cartes)

    def tirer(self):
        return self.cartes.pop() if self.cartes else None

class Main:
    def __init__(self):
        self.cartes = []

    def ajouter_carte(self, carte):
        self.cartes.append(carte)

    def valeur_totale(self):
        total = sum(carte.get_points() for carte in self.cartes)
        nb_as = sum(1 for carte in self.cartes if carte.valeur == 'As')
        
        # Ajustement des As si on dépasse 21 (11 devient 1)
        while total > 21 and nb_as > 0:
            total -= 10
            nb_as -= 1
        return total

# ==========================================
# PARTIE INTERFACE GRAPHIQUE (NOAH & ABDERRAMAN)
# ==========================================

class BlackjackGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack - Évaluation Intermédiaire")
        self.root.geometry("800x600")
        self.root.configure(bg="#2E8B57") # Vert tapis de casino

        self.sabot = None
        self.main_joueur = None
        self.main_croupier = None

        # --- Éléments de l'interface ---
        self.info_label = tk.Label(root, text="Bienvenue au Blackjack !", font=("Helvetica", 16), bg="#2E8B57", fg="white")
        self.info_label.pack(pady=10)

        self.canvas_croupier = tk.Canvas(root, width=600, height=150, bg="#2E8B57", highlightthickness=0)
        self.canvas_croupier.pack(pady=10)
        
        self.canvas_joueur = tk.Canvas(root, width=600, height=150, bg="#2E8B57", highlightthickness=0)
        self.canvas_joueur.pack(pady=10)

        # Boutons
        frame_boutons = tk.Frame(root, bg="#2E8B57")
        frame_boutons.pack(pady=20)

        self.btn_tirer = tk.Button(frame_boutons, text="Carte ! (Hit)", command=self.joueur_tire, font=("Helvetica", 12), state=tk.DISABLED)
        self.btn_tirer.grid(row=0, column=0, padx=10)

        self.btn_rester = tk.Button(frame_boutons, text="Je reste (Stand)", command=self.joueur_reste, font=("Helvetica", 12), state=tk.DISABLED)
        self.btn_rester.grid(row=0, column=1, padx=10)

        self.btn_nouvelle = tk.Button(frame_boutons, text="Nouvelle Partie", command=self.nouvelle_partie, font=("Helvetica", 12))
        self.btn_nouvelle.grid(row=0, column=2, padx=10)

    def dessiner_carte(self, canvas, carte, x, y, cachee=False):
        # Dessine un rectangle simple pour représenter la carte
        canvas.create_rectangle(x, y, x+80, y+120, fill="white" if not cachee else "blue", outline="black", width=2)
        if not cachee:
            couleur_texte = "red" if carte.couleur in ['Cœur', 'Carreau'] else "black"
            canvas.create_text(x+40, y+60, text=f"{carte.valeur}\nde\n{carte.couleur}", fill=couleur_texte, font=("Helvetica", 10, "bold"), justify=tk.CENTER)

    def maj_affichage(self, fin_partie=False):
        self.canvas_croupier.delete("all")
        self.canvas_joueur.delete("all")

        # Affichage Croupier (Une carte face visible, une face cachée sauf si fin de partie)
        for i, carte in enumerate(self.main_croupier.cartes):
            cachee = (i == 1 and not fin_partie)
            self.dessiner_carte(self.canvas_croupier, carte, 20 + i*90, 15, cachee)
        
        # Affichage Joueur (Deux cartes visibles dès le début)
        for i, carte in enumerate(self.main_joueur.cartes):
            self.dessiner_carte(self.canvas_joueur, carte, 20 + i*90, 15)

        valeur_j = self.main_joueur.valeur_totale()
        texte_info = f"Votre score: {valeur_j}"
        
        if fin_partie:
            texte_info += f" | Score Croupier: {self.main_croupier.valeur_totale()}"
            
        self.info_label.config(text=texte_info)

    def nouvelle_partie(self):
        self.sabot = Sabot()
        self.main_joueur = Main()
        self.main_croupier = Main()

        # Distribution initiale
        self.main_joueur.ajouter_carte(self.sabot.tirer())
        self.main_croupier.ajouter_carte(self.sabot.tirer())
        self.main_joueur.ajouter_carte(self.sabot.tirer())
        self.main_croupier.ajouter_carte(self.sabot.tirer())

        self.btn_tirer.config(state=tk.NORMAL)
        self.btn_rester.config(state=tk.NORMAL)
        
        self.maj_affichage()
        
        # Vérification Blackjack initial (As + Bûche)
        if self.main_joueur.valeur_totale() == 21:
            self.fin_de_partie("Blackjack ! Vous avez gagné.")

    def joueur_tire(self):
        self.main_joueur.ajouter_carte(self.sabot.tirer())
        self.maj_affichage()
        
        if self.main_joueur.valeur_totale() > 21:
            self.fin_de_partie("Vous avez brûlé (>21) ! La banque gagne.")

    def joueur_reste(self):
        # Service du croupier : la banque tire à 16, reste à 17
        while self.main_croupier.valeur_totale() < 17:
            self.main_croupier.ajouter_carte(self.sabot.tirer())
            
        score_j = self.main_joueur.valeur_totale()
        score_c = self.main_croupier.valeur_totale()
        
        if score_c > 21:
            msg = "Le croupier a brûlé ! Vous gagnez."
        elif score_j > score_c:
            msg = "Vous avez gagné !"
        elif score_j < score_c:
            msg = "La banque gagne."
        else:
            msg = "Égalité (Push)."
            
        self.fin_de_partie(msg)

    def fin_de_partie(self, message):
        self.maj_affichage(fin_partie=True)
        self.btn_tirer.config(state=tk.DISABLED)
        self.btn_rester.config(state=tk.DISABLED)
        messagebox.showinfo("Résultat", message)

if __name__ == "__main__":
    root = tk.Tk()
    app = BlackjackGame(root)
    root.mainloop()
