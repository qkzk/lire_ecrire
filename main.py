import random

from gtts import gTTS
import pgzrun
import pygame

from noms_communs import NOMS_COMMUNS


TITLE = "Ecouter Lire Ecrire"
WIDTH = 800
HEIGHT = 600


class JeuApprentissage:
    """Classe pour gérer le jeu de manière orientée objet"""

    def __init__(self):
        self.nom_a_trouver = ""
        self.nom_tape = ""
        self.image_bon = Actor("licorne")
        self.image_bon.pos = (200, 300)
        self.show_image = False
        self.callback_nouveau_nom = False
        self.callback_bravo = False
        self.choisir_nouveau_nom()

    def choisir_nouveau_nom(self):
        """Choisit un nom au hasard et lance la lecture avec gTTS."""
        print("choisir_nouveau_nom")
        self.nom_a_trouver = random.choice(NOMS_COMMUNS).lower()
        self.nom_tape = ""
        self.show_image = False
        self.callback_bravo = False
        self.jouer_nom(self.nom_a_trouver)

    def jouer_nom(self, nom):
        """Utilise gTTS pour lire le nom à l'écran."""
        tts = gTTS(text=nom, lang="fr")
        fichier_audio = "sons/nom.mp3"
        tts.save(fichier_audio)
        self.jouer_son(fichier_audio)

    def jouer_son(self, fichier_audio):
        """Joue le fichier audio donné."""
        try:
            pygame.mixer.music.load(fichier_audio)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Erreur lors de la lecture du son: {e}")

    def verifier_touche(self, touche: str):
        """Vérifie chaque lettre tapée, si correcte elle est ajoutée à self.nom_tape."""
        if len(self.nom_tape) >= len(self.nom_a_trouver):
            return
        if touche == self.nom_a_trouver[len(self.nom_tape)]:
            self.nom_tape += touche

        if self.nom_tape == self.nom_a_trouver:
            if not self.callback_bravo:
                clock.schedule_unique(self.jouer_bravo, 1.5)
                self.callback_bravo = True

    def jouer_bravo(self):
        """Affiche l'image et joue le son de félicitation."""
        self.show_image = True
        self.callback_nouveau_nom = False
        fichier_audio = "sons/bravo.mp3"
        self.jouer_son(fichier_audio)

    def mise_a_jour(self):
        """Remet le jeu à zéro après succès."""
        if self.show_image and not self.callback_nouveau_nom:
            clock.schedule_unique(self.choisir_nouveau_nom, 2.0)
            self.callback_nouveau_nom = True


# Initialisation du jeu
jeu = JeuApprentissage()


# Fonction appelée chaque frame par Pygame Zero
def draw():
    """Dessiner le jeu"""
    screen.fill((70, 20, 20))

    # Affiche le mot à trouver et le mot tapé jusqu'à présent
    screen.draw.text(
        f"Mot : {jeu.nom_a_trouver}", midtop=(400, 100), fontsize=50, color="white"
    )
    screen.draw.text(f"Votre saisie :", midtop=(400, 200), fontsize=50, color="orange")
    screen.draw.text(jeu.nom_tape, midtop=(400, 300), fontsize=50, color="pink")

    # Affiche l'image si le mot est correctement tapé
    if jeu.show_image:
        jeu.image_bon.draw()


def on_key_down(key):
    """Fonction appelée quand une touche est pressée"""
    if key == keys.ESCAPE:
        exit()
    touche = key.name.lower()
    if touche.isalpha() and len(touche) == 1:
        jeu.verifier_touche(touche)


def update():
    """Mise a jour du jeu"""
    jeu.mise_a_jour()


# Lancer le jeu Pygame Zero
pgzrun.go()
