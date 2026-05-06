import tkinter as tk
from tkinter import messagebox
import random

# ==========================================================
# PROJET INFORMATIQUE : BLACKJACK
# EQUIPE : Anil, Noah et Oualid
# ROLES : 
# - Anil & Noah : Logique du jeu, calculs, règles spéciales (Surrender)
# - Oualid : Interface graphique, Canvas et système de mise
# ==========================================================

# --- VARIABLES GLOBALES ---
# (Initialisées par l'équipe)
cartes_valeurs = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'V', 'D', 'R', 'A']
cartes_couleurs = ['♥', '♦', '♣', '♠']

paquet = []
main_joueur = []
main_croupier = []

solde = 1000
mise_actuelle = 0
partie_en_cours = False

# --- FONCTIONS LOGIQUES (Développées par Anil et Noah) ---

def creer_paquet():
    """Génère et mélange un nouveau paquet de 52 cartes"""
    global paquet
    paquet = []
    for couleur in cartes_couleurs:
        for valeur in cartes_valeurs:
            paquet.append((valeur, couleur))
    random.shuffle(paquet)
    print("Debug: Paquet mélangé par Anil et Noah")

def valeur_carte(carte):
    """Détermine la valeur numérique d'une carte"""
    valeur = carte[0]
    if valeur in ['V', 'D', 'R']:
        return 10
    elif valeur == 'A':
        return 11
    else:
        return int(valeur)

def calculer_score(main):
    """Calcule le total d'une main avec la gestion de l'As"""
    score = 0
    nombre_as = 0
    for carte in main:
        score = score + valeur_carte(carte)
        if carte[0] == 'A':
            nombre_as = nombre_as + 1
            
    while score > 21 and nombre_as > 0:
        score = score - 10
        nombre_as = nombre_as - 1
    return score

# --- FONCTIONS GRAPHIQUES (Développées par Oualid, avec l'aide de Noah) ---

def dessiner_carte(x, y, carte, cachee=False):
    """Crée le visuel d'une carte sur le tapis (Travail de Oualid)"""
    tapis.create_rectangle(x, y, x + 60, y + 90, fill="white", outline="black", width=2)
    
    if cachee == True:
        # Dos de la carte dessiné par Oualid
        tapis.create_rectangle(x + 5, y + 5, x + 55, y + 85, fill="blue", outline="white")
    else:
        valeur = carte[0]
        couleur = carte[1]
        couleur_texte = "red" if couleur in ['♥', '♦'] else "black"
        
        tapis.create_text(x + 15, y + 20, text=valeur, font=("Arial", 14, "bold"), fill=couleur_texte)
        tapis.create_text(x + 30, y + 50, text=couleur, font=("Arial", 24), fill=couleur_texte)

def mettre_a_jour_affichage(cacher_croupier=True):
    """Gère l'actualisation du Canvas (Collaboration Oualid et Anil)"""
    label_argent.config(text="Banque: " + str(solde) + " €   |   Mise: " + str(mise_actuelle) + " €")
    tapis.delete("all")
    
    texte_croupier = "CROUPIER"
    texte_joueur = "JOUEUR"
    
    if partie_en_cours:
        score_j = calculer_score(main_joueur)
        texte_joueur = "JOUEUR (Score : " + str(score_j) + ")"
        
        if cacher_croupier == False:
            score_c = calculer_score(main_croupier)
            texte_croupier = "CROUPIER (Score : " + str(score_c) + ")"
            
    tapis.create_text(300, 30, text=texte_croupier, fill="white", font=("Arial", 14, "bold"))
    tapis.create_text(300, 200, text=texte_joueur, fill="white", font=("Arial", 14, "bold"))
    
    if partie_en_cours:
        # Affichage des cartes (Oualid)
        x_depart_c = 300 - (len(main_croupier) * 35)
        for index in range(len(main_croupier)):
            carte = main_croupier[index]
            est_cachee = (index == 1) and cacher_croupier 
            dessiner_carte(x_depart_c + (index * 70), 50, carte, est_cachee)
            
        x_depart_j = 300 - (len(main_joueur) * 35)
        for index in range(len(main_joueur)):
            carte = main_joueur[index]
            dessiner_carte(x_depart_j + (index * 70), 230, carte, cachee=False)

    fenetre.update()

# --- ACTIONS DU JEU (Collaboration de toute l'équipe) ---

def miser(montant):
    """Gestion des mises (Codé par Oualid)"""
    global solde, mise_actuelle
    if partie_en_cours == False:
        if solde >= montant:
            solde = solde - montant
            mise_actuelle = mise_actuelle + montant
            mettre_a_jour_affichage()
        else:
            messagebox.showinfo("Attention", "Solde insuffisant !")

def effacer_mise():
    global solde, mise_actuelle
    if partie_en_cours == False:
        solde = solde + mise_actuelle
        mise_actuelle = 0
        mettre_a_jour_affichage()

def distribuer():
    """Début de manche (Codé par Noah)"""
    global partie_en_cours
    if mise_actuelle == 0:
        messagebox.showinfo("Erreur", "Placez une mise !")
        return
        
    creer_paquet()
    partie_en_cours = True
    main_joueur.clear()
    main_croupier.clear()
    
    main_joueur.append(paquet.pop())
    main_croupier.append(paquet.pop())
    main_joueur.append(paquet.pop())
    main_croupier.append(paquet.pop())
    
    # Activation des boutons de jeu
    bouton_tirer.config(state="normal")
    bouton_rester.config(state="normal")
    bouton_abandonner.config(state="normal") # On peut abandonner au début
    bouton_distribuer.config(state="disabled")
    
    mettre_a_jour_affichage()
    
    if calculer_score(main_joueur) == 21:
        fin_de_partie("Blackjack ! Bravo !", 2.5)

def abandonner():
    """Règle Bonus : Le joueur abandonne et perd la moitié de sa mise (Anil)"""
    global solde, mise_actuelle, partie_en_cours
    
    moitie = int(mise_actuelle / 2)
    solde = solde + moitie # On rend la moitié au joueur
    
    mettre_a_jour_affichage(cacher_croupier=False)
    messagebox.showinfo("Résultat", "Vous avez abandonné. Vous récupérez la moitié de votre mise.")
    
    mise_actuelle = 0
    partie_en_cours = False
    
    bouton_tirer.config(state="disabled")
    bouton_rester.config(state="disabled")
    bouton_abandonner.config(state="disabled")
    bouton_distribuer.config(state="normal")
    
    mettre_a_jour_affichage()

def tirer():
    """Le joueur prend une carte (Codé par Anil)"""
    # Si on tire une carte, on n'a plus le droit d'abandonner
    bouton_abandonner.config(state="disabled") 
    
    main_joueur.append(paquet.pop())
    mettre_a_jour_affichage()
    
    if calculer_score(main_joueur) > 21:
        fin_de_partie("Bust ! Vous avez dépassé 21.", 0)

def rester():
    """Tour du croupier (Codé par Anil et Noah)"""
    bouton_abandonner.config(state="disabled") # Sécurité
    
    while calculer_score(main_croupier) < 17:
        main_croupier.append(paquet.pop())
        mettre_a_jour_affichage(cacher_croupier=False)
        
    score_j = calculer_score(main_joueur)
    score_c = calculer_score(main_croupier)
    
    if score_c > 21:
        fin_de_partie("Le croupier explose ! Gagné.", 2)
    elif score_j > score_c:
        fin_de_partie("Meilleur score ! Gagné.", 2)
    elif score_j < score_c:
        fin_de_partie("La banque gagne.", 0)
    else:
        fin_de_partie("Égalité !", 1)

def fin_de_partie(message, multiplicateur):
    """Clôture de la manche (Codé par Noah)"""
    global solde, mise_actuelle, partie_en_cours
    
    mettre_a_jour_affichage(cacher_croupier=False)
    messagebox.showinfo("Résultat", message)
    
    solde = solde + int(mise_actuelle * multiplicateur)
    mise_actuelle = 0
    partie_en_cours = False
    
    bouton_tirer.config(state="disabled")
    bouton_rester.config(state="disabled")
    bouton_abandonner.config(state="disabled")
    bouton_distribuer.config(state="normal")
    
    mettre_a_jour_affichage()

# --- INTERFACE (Mise en place par Oualid) ---

fenetre = tk.Tk()
fenetre.title("Projet Blackjack - Anil / Noah / Oualid")
fenetre.geometry("650x550")
fenetre.configure(bg="#006400")

label_argent = tk.Label(fenetre, text="", font=("Arial", 14, "bold"), bg="#006400", fg="gold")
label_argent.pack(pady=10)

tapis = tk.Canvas(fenetre, width=600, height=350, bg="#004d00", highlightthickness=2, highlightbackground="gold")
tapis.pack()

cadre_mises = tk.Frame(fenetre, bg="#006400")
cadre_mises.pack(pady=10)

tk.Button(cadre_mises, text="Miser 10 €", command=lambda: miser(10)).grid(row=0, column=0, padx=5)
tk.Button(cadre_mises, text="Miser 50 €", command=lambda: miser(50)).grid(row=0, column=1, padx=5)
tk.Button(cadre_mises, text="Effacer", command=effacer_mise).grid(row=0, column=2, padx=5)

bouton_distribuer = tk.Button(cadre_mises, text="JOUER", command=distribuer, font=("Arial", 10, "bold"), bg="gold")
bouton_distribuer.grid(row=0, column=3, padx=20)

cadre_actions = tk.Frame(fenetre, bg="#006400")
cadre_actions.pack(pady=5)

bouton_tirer = tk.Button(cadre_actions, text="Carte", command=tirer, state="disabled", width=12)
bouton_tirer.grid(row=0, column=0, padx=10)

bouton_rester = tk.Button(cadre_actions, text="Rester", command=rester, state="disabled", width=12)
bouton_rester.grid(row=0, column=1, padx=10)

# Nouveau bouton Abandonner (Surrender)
bouton_abandonner = tk.Button(cadre_actions, text="Abandonner", command=abandonner, state="disabled", width=12)
bouton_abandonner.grid(row=0, column=2, padx=10)

mettre_a_jour_affichage()
fenetre.mainloop()
