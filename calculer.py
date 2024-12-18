import random
import os

from gtts import gTTS
import pgzrun
import pygame

from pgzero.actor import Actor
from pgzero.keyboard import Keyboard
from pgzero.screen import Screen
from pygame import Rect

screen: Screen
keyboard: Keyboard

os.environ["SDL_VIDEO_CENTERED"] = "1"


TITLE = "Ecouter Calculer"
WIDTH = 1920
HEIGHT = 1080


class Calculer:
    """Classe pour gérer le jeu de manière orientée objet"""

    NUM_RECTS = [
        Rect(i * WIDTH / 12, 3 * HEIGHT / 4, WIDTH / 14, WIDTH / 14)
        for i in range(1, 10)
    ]

    def __init__(self):
        self.calcul = ""
        self.solution: int
        self.text: str
        self.image_bon = Actor("licorne")
        self.image_bon.pos = (300, 400)
        self.show_image = False
        self.callback_nouveau_calcul = False
        self.callback_bravo = False
        self.choisir_nouveau_calcul()

    def choisir_nouveau_calcul(self):
        """Choisit un calcul aléatoire et lance la lecture avec gTTS."""
        a = random.randint(1, 5)
        b = random.randint(1, 4)
        op = random.choice(("+", "-"))
        if a < b and op == "-":
            a, b = b, a
        if a == b and op == "-":
            a += 1
        self.calcul = f"{a} {op} {b}"
        self.solution = a + b if op == "+" else a - b
        self.text = self.calcul if op == "+" else f"{a} moins {b}"
        self.show_image = False
        self.callback_bravo = False
        self.jouer_calcul(self.text)

    def jouer_calcul(self, text):
        """Utilise gTTS pour lire le nom à l'écran."""
        tts = gTTS(text=text, lang="fr")
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

    def verifier(self, pos: tuple):
        """Vérifie chaque lettre tapée, si correcte elle est ajoutée à self.nom_tape."""
        choice = 0
        for index, rect in enumerate(self.NUM_RECTS):
            if rect.collidepoint(*pos):
                choice = index + 1
        if self.solution == choice:
            if not self.callback_bravo:
                clock.schedule_unique(self.jouer_bravo, 1.5)
                self.callback_bravo = True

    def jouer_bravo(self):
        """Affiche l'image et joue le son de félicitation."""
        self.show_image = True
        self.callback_nouveau_calcul = False
        fichier_audio = "sons/bravo.mp3"
        self.jouer_son(fichier_audio)

    def mise_a_jour(self):
        """Remet le jeu à zéro après succès."""
        if self.show_image and not self.callback_nouveau_calcul:
            clock.schedule_unique(self.choisir_nouveau_calcul, 2.0)
            self.callback_nouveau_calcul = True


jeu = Calculer()


def draw():
    """Dessiner le jeu"""
    screen.fill("#836fff")

    # Affiche le mot à trouver et le mot tapé jusqu'à présent
    screen.draw.text(
        jeu.calcul,
        center=(WIDTH / 2, HEIGHT / 3),
        fontsize=144,
        ocolor="black",
        owidth=0.5,
        color="#00ff7f",
    )
    screen.draw.text(
        f"Bouge la souris sur la réponse :",
        center=(WIDTH / 2, HEIGHT / 2),
        fontsize=50,
        color="#00ff7f",
    )
    for i in range(1, 10):
        screen.draw.filled_rect(Calculer.NUM_RECTS[i - 1], "#ff7f00")
        screen.draw.text(
            str(i),
            center=(i * WIDTH / 12 + WIDTH / 28, 3 * HEIGHT / 4 + WIDTH / 28),
            color="#00ff7f",
            ocolor="black",
            owidth=0.5,
            fontsize=144,
        )

    # Affiche l'image si le mot est correctement tapé
    if jeu.show_image:
        jeu.image_bon.draw()


def on_key_down(key):
    """Fonction appelée quand une touche est pressée"""
    if key == keys.ESCAPE:
        exit()


def on_mouse_move(pos):
    jeu.verifier(pos)


def update():
    """Mise a jour du jeu"""
    jeu.mise_a_jour()


# Lancer le jeu Pygame Zero
pgzrun.go()
