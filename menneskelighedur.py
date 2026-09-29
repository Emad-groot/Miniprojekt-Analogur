import pygame
import math
from datetime import datetime


# Starter Pygame
pygame.init()


# ---------------------------------
# Vinduets størrelse og indstillinger
# ---------------------------------

WIDTH = 1100
HEIGHT = 900

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menneskelighedsuret")

clock = pygame.time.Clock()


# ---------------------------------
# Farver
# ---------------------------------

BLACK = (15, 15, 25)
WHITE = (245, 245, 245)
GREY = (150, 150, 160)
RED = (230, 70, 70)
BLUE = (80, 150, 255)
GOLD = (245, 190, 60)


# ---------------------------------
# Urets størrelse og centrum
# ---------------------------------

center_x = WIDTH // 2
center_y = HEIGHT // 2

center = (center_x, center_y)

clock_radius = 280
word_radius = 350


# ---------------------------------
# Skrifttyper
# ---------------------------------

title_font = pygame.font.SysFont("arial", 38, bold=True)
word_font = pygame.font.SysFont("arial", 22, bold=True)
time_font = pygame.font.SysFont("arial", 25)


# ---------------------------------
# De 12 menneskelige værdier
# ---------------------------------

menneskelige_vaerdier = [
    "Ærlighed",        # Klokken 1
    "Venskab",         # Klokken 2
    "Tålmodighed",     # Klokken 3
    "Nysgerrighed",    # Klokken 4
    "Retfærdighed",    # Klokken 5
    "Opdagelse",       # Klokken 6
    "Kærlighed",       # Klokken 7
    "Håb",             # Klokken 8
    "Lighed",          # Klokken 9
    "Empati",          # Klokken 10
    "Civilkurage",     # Klokken 11
    "Fantasi"          # Klokken 12
]


# ---------------------------------
# Funktion til beregning af punkter
# ---------------------------------

def beregn_punkt(vinkel, laengde):
    """
    Beregner et punkt omkring urets centrum.

    vinkel:
        Vinklen i grader.

    laengde:
        Afstanden fra urets centrum.
    """

    vinkel_i_radianer = math.radians(vinkel)

    x = center_x + laengde * math.cos(vinkel_i_radianer)
    y = center_y + laengde * math.sin(vinkel_i_radianer)

    return int(x), int(y)


# ---------------------------------
# Funktion til at tegne urskiven
# ---------------------------------

def tegn_urskive():

    # Tegner den store cirkel
    pygame.draw.circle(
        screen,
        WHITE,
        center,
        clock_radius,
        3
    )

    # Tegner de 12 markeringer
    for nummer in range(1, 13):

        vinkel = nummer * 30 - 90

        startpunkt = beregn_punkt(
            vinkel,
            clock_radius - 20
        )

        slutpunkt = beregn_punkt(
            vinkel,
            clock_radius
        )

        pygame.draw.line(
            screen,
            WHITE,
            startpunkt,
            slutpunkt,
            4
        )


# ---------------------------------
# Funktion til at tegne værdierne
# ---------------------------------

def tegn_vaerdier():

    for nummer, vaerdi in enumerate(
        menneskelige_vaerdier,
        start=1
    ):

        # Der er 30 grader mellem hvert klokkeslæt
        vinkel = nummer * 30 - 90

        x, y = beregn_punkt(
            vinkel,
            word_radius
        )

        # Kærlighed vises med rød farve
        if vaerdi == "Kærlighed":
            tekst_farve = RED

        # Håb vises med guldfarve
        elif vaerdi == "Håb":
            tekst_farve = GOLD

        else:
            tekst_farve = WHITE

        tekst = word_font.render(
            vaerdi,
            True,
            tekst_farve
        )

        tekst_firkant = tekst.get_rect(
            center=(x, y)
        )

        screen.blit(
            tekst,
            tekst_firkant
        )


# ---------------------------------
# Funktion til at tegne viserne
# ---------------------------------

def tegn_visere():

    # Henter computerens aktuelle tid
    nu = datetime.now()

    timer = nu.hour
    minutter = nu.minute
    sekunder = nu.second
    mikrosekunder = nu.microsecond

    # Gør sekundviserens bevægelse mere flydende
    praecise_sekunder = sekunder + mikrosekunder / 1_000_000

    # Beregner visernes vinkler
    sekund_vinkel = praecise_sekunder * 6 - 90

    minut_vinkel = (
        minutter + praecise_sekunder / 60
    ) * 6 - 90

    time_vinkel = (
        timer % 12 + minutter / 60
    ) * 30 - 90

    # Beregner visernes endepunkter
    sekund_slutpunkt = beregn_punkt(
        sekund_vinkel,
        245
    )

    minut_slutpunkt = beregn_punkt(
        minut_vinkel,
        210
    )

    time_slutpunkt = beregn_punkt(
        time_vinkel,
        145
    )

    # Timeviser
    pygame.draw.line(
        screen,
        WHITE,
        center,
        time_slutpunkt,
        9
    )

    # Minutviser
    pygame.draw.line(
        screen,
        BLUE,
        center,
        minut_slutpunkt,
        6
    )

    # Sekundviser
    pygame.draw.line(
        screen,
        RED,
        center,
        sekund_slutpunkt,
        3
    )

    # Cirkel i midten
    pygame.draw.circle(
        screen,
        GOLD,
        center,
        12
    )

    return nu


# ---------------------------------
# Programmets hovedløkke
# ---------------------------------

running = True

while running:

    # Undersøger hændelser
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    # Rydder det gamle billede
    screen.fill(BLACK)

    # Titel
    title = title_font.render(
        "Menneskelighedsuret",
        True,
        GOLD
    )

    title_rect = title.get_rect(
        center=(center_x, 40)
    )

    screen.blit(
        title,
        title_rect
    )

    # Tegner urets forskellige dele
    tegn_urskive()
    tegn_vaerdier()
    nu = tegn_visere()

    # Viser også tiden digitalt
    digital_tid = nu.strftime("%H:%M:%S")

    time_text = time_font.render(
        digital_tid,
        True,
        GREY
    )

    time_rect = time_text.get_rect(
        center=(center_x, center_y + 80)
    )

    screen.blit(
        time_text,
        time_rect
    )

    # Opdaterer vinduet
    pygame.display.flip()

    # Maksimalt 60 billeder pr. sekund
    clock.tick(60)


# Lukker Pygame
pygame.quit()