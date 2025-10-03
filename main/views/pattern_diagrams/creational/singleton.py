import pygame
import sys
import os
import time

pygame.init()

# ================== PODEŠAVANJE EKRANA ==================
BASE_WIDTH, BASE_HEIGHT = 1280, 720
screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Singleton - Printer Triangle Loop Animation")

WHITE = (255, 255, 255)

# ================== UČITAVANJE SLIKA ==================
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# relativni path do resources
BASE_PATH = os.path.normpath(os.path.join(CURRENT_DIR, "../../../../main/resources/diagrams/creational_patterns/singleton/"))

printer_img_orig = pygame.image.load(os.path.join(BASE_PATH, "printer.png"))
man_img_orig = pygame.image.load(os.path.join(BASE_PATH, "man.png"))
woman_img_orig = pygame.image.load(os.path.join(BASE_PATH, "woman.png"))
document_img_orig = pygame.image.load(os.path.join(BASE_PATH, "document.png"))

# ================== POZICIJE (bazne za 1280x720) ==================
printer_pos_orig = (BASE_WIDTH//2 - 75, 50)
man_pos_orig = (150, BASE_HEIGHT - 250)
woman_pos_orig = (BASE_WIDTH - 270, BASE_HEIGHT - 250)
doc1_pos_orig = [man_pos_orig[0] + 80, man_pos_orig[1] + 40]   # dokument mana
doc2_pos_orig = [woman_pos_orig[0] + 50, woman_pos_orig[1] + 40] # dokument žene

# ================== SKALIRANJE ==================
def scale_elements():
    current_w, current_h = screen.get_size()
    scale_x = current_w / BASE_WIDTH
    scale_y = current_h / BASE_HEIGHT

    man_img = pygame.transform.scale(man_img_orig, (int(150*scale_x), int(200*scale_y)))
    woman_img = pygame.transform.scale(woman_img_orig, (int(120*scale_x), int(150*scale_y)))
    printer_img = pygame.transform.scale(printer_img_orig, (int(150*scale_x), int(150*scale_y)))
    document_img = pygame.transform.scale(document_img_orig, (int(60*scale_x), int(80*scale_y)))

    printer_pos = (int(printer_pos_orig[0]*scale_x), int(printer_pos_orig[1]*scale_y))
    man_pos = (int(man_pos_orig[0]*scale_x), int(man_pos_orig[1]*scale_y))
    woman_pos = (int(woman_pos_orig[0]*scale_x), int(woman_pos_orig[1]*scale_y))

    return man_img, man_pos, woman_img, woman_pos, printer_img, printer_pos, document_img

# ================== POMOĆNA FUNKCIJA ==================
def move_towards(current, target, step):
    """Pomiče current prema target sa maksimalnim korakom step po osi"""
    if current < target:
        current += min(step, target - current)
    elif current > target:
        current -= min(step, current - target)
    return current

# ================== MAIN LOOP ==================
clock = pygame.time.Clock()
running = True
speed = 5  # brzina dokumenata

# trenutne pozicije dokumenata
doc1_pos = list(doc1_pos_orig)
doc2_pos = list(doc2_pos_orig)

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # skaliraj slike i pozicije
    man_img, man_pos, woman_img, woman_pos, printer_img, printer_pos, document_img = scale_elements()

    # crtanje statičnih objekata
    screen.blit(man_img, man_pos)
    screen.blit(woman_img, woman_pos)
    screen.blit(printer_img, printer_pos)

    # ================== POMAK DOKUMENATA ==================
    # Dokument od muskarca prema printeru
    doc1_pos[0] = move_towards(doc1_pos[0], printer_pos[0] + 60, speed)
    doc1_pos[1] = move_towards(doc1_pos[1], printer_pos[1] + 40, speed)

    # Dokument od žene prema printeru
    doc2_pos[0] = move_towards(doc2_pos[0], printer_pos[0] + 60, speed)
    doc2_pos[1] = move_towards(doc2_pos[1], printer_pos[1] + 40, speed)

    # crtanje dokumenata
    screen.blit(document_img, doc1_pos)
    screen.blit(document_img, doc2_pos)

    # ================== LOOP ANIMACIJA ==================
    # Ako su oba dokumenta na printeru, čekaj 2 sekunde i resetiraj
    if (doc1_pos[0] == printer_pos[0] + 60 and doc1_pos[1] == printer_pos[1] + 40 and
            doc2_pos[0] == printer_pos[0] + 60 and doc2_pos[1] == printer_pos[1] + 40):
        pygame.display.flip()  # prikaz trenutne pozicije
        pygame.time.delay(2000)  # čekanje 2 sekunde
        doc1_pos = list(doc1_pos_orig)
        doc2_pos = list(doc2_pos_orig)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
