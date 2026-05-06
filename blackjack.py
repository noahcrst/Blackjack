import tkinter as tk
from tkinter import messagebox
import random

# ==========================================================
# PROJET INFORMATIQUE : BLACKJACK
# EQUIPE : Anil, Noah et Oualid
#
# ROLES OFFICIELS : 
# - Noah : Responsable GitHub (Hébergement, gestion et vérification des dépôts)
# - Anil : Responsable Qualité du Code (Respect des normes, explications, nommage)
# - Oualid : Responsable Interface Graphique (Tapis de jeu, cartes, design)
#
# DÉCLARATION D'UTILISATION D'IA (LLM) :
# Conformément aux consignes du projet, nous déclarons avoir été aidés par une IA pour :
# 1. La partie graphisme : apprentissage et syntaxe des méthodes Canvas de Tkinter.
# 2. Certaines parties logiques : conception de l'algorithme gérant la valeur de l'As.
# ==========================================================

# --- VARIABLES GLOBALES ---
valeurs_cartes = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'V', 'D', 'R', 'A']
couleurs_cartes = ['♥', '♦', '♣', '♠']

paquet = []
main_joueur = []
main_croupier = []

solde = 105
mise_actuelle = 0
partie_en_cours = False

# --- FONCTIONS LOGIQUES (Développées par Anil et Noah) ---

def creer_paquet():
    """Génère et mélange un nouveau jeu de 52 cartes."""
    global paquet
    paquet = []
    for couleur in couleurs_cartes:
        for valeur in valeurs_cartes:
            paquet.append((valeur, couleur))
    random.shuffle(paquet)

def obtenir_valeur_numerique(carte):
    """Convertit le symbole d'une carte en points (V/D/R = 10, A = 11)."""
    valeur = carte[0]
    if valeur in ['V', 'D', 'R']:
        return 10
    elif valeur == 'A':
        return 11
    else:
        return int(valeur)

def calculer_score(main):
    """Calcule le total de points d'une main en gérant la flexibilité de l'As."""
    score = 0
    nombre_as = 0
    for carte in main:
        score = score + obtenir_valeur_numerique(carte)
        if carte[0] == 'A':
            nombre_as = nombre_as + 1
            
    # Aide IA : La structure de cette boucle while pour faire passer la valeur 
    # de l'As de 11 à 1 en cas de dépassement de 21 nous a été suggérée par un LLM.
    while score > 21 and nombre_as > 0:
        score = score - 10
        nombre_as = nombre_as - 1
    return score

# --- FONCTIONS GRAPHIQUES (Développées par Oualid) ---

def dessiner_carte(x, y, carte, cachee=False):
    """Dessine visuellement une carte sur le tapis de jeu."""
    # Aide IA : L'utilisation exacte des coordonnées (create_rectangle, create_text) 
    # pour centrer les éléments a été générée avec l'appui d'une IA.
    tapis.create_rectangle(x, y, x + 60, y + 90, fill="white", outline="black", width=2)
    
    if cachee == True:
        # Dos de la carte dessiné en bleu
        tapis.create_rectangle(x + 5, y + 5, x + 55, y + 85, fill="#000080", outline="white")
    else:
        valeur = carte[0]
        couleur = carte[1]
        couleur_texte = "red" if couleur in ['♥', '♦'] else "black"
        
        tapis.create_text(x + 15, y + 20, text=valeur, font=("Arial", 14, "bold"), fill=couleur_texte)
        tapis.create_text(x + 30, y + 50, text=couleur, font=("Arial", 24), fill=couleur_texte)

def mettre_a_jour_affichage(cacher_croupier=True):
    """Actualise tous les éléments visuels du plateau de jeu."""
    label_argent.config(text="Banque : " + str(solde) + " €   |   Mise actuelle : " + str(mise_actuelle) + " €")
    tapis.delete("all")
    
    nom_croupier = "CROUPIER"
    nom_joueur = "JOUEUR"
    
    if partie_en_cours:
        score_j = calculer_score(main_joueur)
        nom_joueur = "JOUEUR (Score : " + str(score_j) + ")"
        
        if cacher_croupier == False:
            score_c = calculer_score(main_croupier)
            nom_croupier = "CROUPIER (Score : " + str(score_c) + ")"
            
    tapis.create_text(300, 30, text=nom_croupier, fill="white", font=("Arial", 14, "bold"))
    tapis.create_text(300, 200, text=nom_joueur, fill="white", font=("Arial", 14, "bold"))
    
    if partie_en_cours:
        # Cartes du Croupier
        x_c = 300 - (len(main_croupier) * 35)
        for i in range(len(main_croupier)):
            dessiner_carte(x_c + (i * 70), 50, main_croupier[i], (i == 1 and cacher_croupier))
            
        # Cartes du Joueur
        x_j = 300 - (len(main_joueur) * 35)
        for i in range(len(main_joueur)):
            dessiner_carte(x_j + (i * 70), 230, main_joueur[i], False)

    fenetre.update()

# --- ACTIONS DU JEU ---

def miser(montant):
    """Ajoute de l'argent à la mise en cours."""
    global solde, mise_actuelle
    if not partie_en_cours:
        if solde >= montant:
            solde = solde - montant
            mise_actuelle = mise_actuelle + montant
            mettre_a_jour_affichage()
        else:
            messagebox.showwarning("Fonds insuffisants", "Vous n'avez pas assez d'argent !")

def effacer_mise():
    """Annule la mise actuelle et restitue l'argent dans le solde du joueur."""
    global solde, mise_actuelle
    if not partie_en_cours:
        solde = solde + mise_actuelle
        mise_actuelle = 0
        mettre_a_jour_affichage()

def distribuer():
    """Lance une nouvelle manche et distribue les cartes initiales."""
    global partie_en_cours
    if mise_actuelle == 0:
        messagebox.showwarning("Action requise", "Veuillez placer une mise avant de jouer.")
        return
        
    creer_paquet()
    partie_en_cours = True
    main_joueur.clear()
    main_croupier.clear()
    
    # Distribution standard : 2 cartes chacun
    for _ in range(2):
        main_joueur.append(paquet.pop())
        main_croupier.append(paquet.pop())
    
    bouton_tirer.config(state="normal")
    bouton_rester.config(state="normal")
    bouton_abandonner.config(state="normal")
    bouton_jouer.config(state="disabled")
    
    mettre_a_jour_affichage()
    
    if calculer_score(main_joueur) == 21:
        fin_de_manche("Blackjack ! Victoire immédiate !", 2.5)

def abandonner():
    """Option d'abandon : le joueur récupère 50% de sa mise."""
    global solde, mise_actuelle, partie_en_cours
    solde = solde + int(mise_actuelle / 2)
    mettre_a_jour_affichage(cacher_croupier=False)
    messagebox.showinfo("Abandon", "Manche annulée. La moitié de votre mise vous est rendue.")
    cloturer_partie()

def tirer():
    """Le joueur demande une carte supplémentaire."""
    bouton_abandonner.config(state="disabled") 
    main_joueur.append(paquet.pop())
    mettre_a_jour_affichage()
    if calculer_score(main_joueur) > 21:
        fin_de_manche("Vous avez dépassé 21. La banque gagne !", 0)

def rester():
    """Le joueur s'arrête, le croupier joue selon la règle du 17."""
    bouton_abandonner.config(state="disabled")
    while calculer_score(main_croupier) < 17:
        main_croupier.append(paquet.pop())
        mettre_a_jour_affichage(cacher_croupier=False)
        
    score_j = calculer_score(main_joueur)
    score_c = calculer_score(main_croupier)
    
    if score_c > 21:
        fin_de_manche("Le croupier a sauté ! Vous gagnez !", 2)
    elif score_j > score_c:
        fin_de_manche("Votre score est supérieur. Vous gagnez !", 2)
    elif score_j < score_c:
        fin_de_manche("La banque a un meilleur score. Perdu !", 0)
    else:
        fin_de_manche("Égalité parfaite !", 1)

def fin_de_manche(message, multiplicateur):
    """Affiche le résultat et distribue les gains."""
    global solde, mise_actuelle
    mettre_a_jour_affichage(cacher_croupier=False)
    messagebox.showinfo("Résultat de la manche", message)
    solde = solde + int(mise_actuelle * multiplicateur)
    cloturer_partie()

def cloturer_partie():
    """Réinitialise l'état du jeu pour la manche suivante."""
    global mise_actuelle, partie_en_cours
    mise_actuelle = 0
    partie_en_cours = False
    bouton_tirer.config(state="disabled")
    bouton_rester.config(state="disabled")
    bouton_abandonner.config(state="disabled")
    bouton_jouer.config(state="normal")
    mettre_a_jour_affichage()

# ==========================================================
# ARCHIVES : TENTATIVES DE DÉVELOPPEMENT (En commentaires)
# ==========================================================
# Nous avons tenté d'implémenter la fonction "SPLIT" (Séparation).
# La logique mathématique était prête, mais l'affichage sur le Canvas
# ne permettait pas de gérer deux mains visuellement de façon propre.
#
# def tentative_split():
#     global main_joueur, solde, mise_actuelle
#     if len(main_joueur) == 2 and main_joueur[0][0] == main_joueur[1][0] and solde >= mise_actuelle:
#         pass # Rendu visuel trop complexe à intégrer proprement
# ==========================================================

# --- INTERFACE ---
fenetre = tk.Tk()
fenetre.title("Blackjack L1 MIASH - Anil / Noah / Oualid")
fenetre.geometry("650x550")
fenetre.configure(bg="#006400")

label_argent = tk.Label(fenetre, text="", font=("Arial", 12, "bold"), bg="#006400", fg="gold")
label_argent.pack(pady=10)

tapis = tk.Canvas(fenetre, width=600, height=350, bg="#004d00", highlightthickness=2, highlightbackground="gold")
tapis.pack()

cadre_mises = tk.Frame(fenetre, bg="#006400")
cadre_mises.pack(pady=10)

tk.Button(cadre_mises, text="+ 1 €", command=lambda: miser(1), width=8).grid(row=0, column=0, padx=5)
tk.Button(cadre_mises, text="+ 10 €", command=lambda: miser(10), width=8).grid(row=0, column=1, padx=5)
tk.Button(cadre_mises, text="+ 50 €", command=lambda: miser(50), width=8).grid(row=0, column=2, padx=5)
tk.Button(cadre_mises, text="Vider", command=effacer_mise, width=8).grid(row=0, column=3, padx=5)
bouton_jouer = tk.Button(cadre_mises, text="DISTRIBUER", command=distribuer, bg="gold", font=("Arial", 9, "bold"))
bouton_jouer.grid(row=0, column=4, padx=15)

cadre_actions = tk.Frame(fenetre, bg="#006400")
cadre_actions.pack(pady=5)

bouton_tirer = tk.Button(cadre_actions, text="Carte", command=tirer, state="disabled", width=12)
bouton_tirer.grid(row=0, column=0, padx=10)
bouton_rester = tk.Button(cadre_actions, text="Rester", command=rester, state="disabled", width=12)
bouton_rester.grid(row=0, column=1, padx=10)
bouton_abandonner = tk.Button(cadre_actions, text="Abandonner", command=abandonner, state="disabled", width=12)
bouton_abandonner.grid(row=0, column=2, padx=10)

mettre_a_jour_affichage()
fenetre.mainloop()
