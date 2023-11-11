import time
import pygame
import pandas as pd
import sys


def le_excel(local, sheet_name=0):
    df = pd.read_excel(local, sheet_name=sheet_name)
    return df.values.T.tolist()


def load_database(file_path):
    columns = le_excel(file_path)
    campos = ["nome", "droid", "humano", "alien", "jedi", "sith", "filme", "serie", "politico", "clone", "rebelde",
              "mandaloriano", "imperial", "morto", "defeituoso", "militar", "entendivel", "corpo incompleto", "grupo",
              "renegado", "2 caras", "genio", "piloto", "crianca/adolescente", "cacador"]

    database = []

    for j in range(45):
        dic = {campos[i]: columns[i][j] for i in range(25)}
        database.append(dic)

    return database


def verifica(carac, database):
    return any(d[carac] for d in database)


def take_chance(answer, prop, database):
    ans = answer == "y"
    to_remove = [d for d in database if d[prop] != ans]

    if prop == "droid" and ans:
        to_remove += [d for d in database if d["humano"] or d["alien"] or d["jedi"] or d["politico"]]
    elif prop == "humano" and ans:
        to_remove += [d for d in database if d["alien"]]
    elif prop == "jedi" and ans:
        to_remove += [d for d in database if d["clone"] or d["cacador"] or d["defeituoso"]]

    database[:] = [e for e in database if e not in to_remove]

    if len(database) == 1:
        print("\nO seu personagem é " + database[0]["nome"])


def draw_button(text, color, x, y, width, height):
    pygame.draw.rect(screen, color, (x, y, width, height), border_radius=3)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text_surface, text_rect)


def draw_question_screen(question):
    screen.fill(WHITE)
    screen.blit(background_image, (0, 0))
    text_surface = font.render(question.title(), True, WHITE)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 8))
    screen.blit(text_surface, text_rect)
    imagem = pygame.image.load('yoda.png')
    imagem = pygame.transform.scale(imagem, (300, 400))
    image_rect = imagem.get_rect(center=(WIDTH // 2, HEIGHT * 3 // 6))
    screen.blit(imagem, image_rect)
    draw_button("Sim", GREEN, 150, 500, 80, 40)
    draw_button("Não", RED, 550, 500, 80, 40)


def handle_mouse_click(propriedade, answer, database):
    if answer == "y":
        take_chance("y", propriedade, database)
        respostas.append("y")
    else:
        take_chance("n", propriedade, database)
        respostas.append("n")


def game_loop(database, perguntas):
    question_number = 0
    running = True

    while running and len(database):
        while question_number < len(perguntas) and len(database) > 1:
            question, propriedade = perguntas[question_number]
            if verifica(propriedade, database):
                draw_question_screen(question)
                answered = False

                while not answered:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            x, y = event.pos
                            if 150 <= x <= 250 and 500 <= y <= 550:
                                handle_mouse_click(propriedade, "y", database)
                                answered = True
                            elif 650 >= x >= 550 >= y >= 500:
                                handle_mouse_click(propriedade, "n", database)
                                answered = True

                    pygame.display.flip()
                    clock.tick(60)

            question_number += 1

        if len(database) == 1:
            result_text = "O seu personagem é " + database[0]["nome"]
        else:
            result_text = "Não foi possível adivinhar."

        screen.fill(WHITE)
        screen.blit(background_image, (0, 0))
        text_surface = font.render(result_text, True, WHITE)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        time.sleep(2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


if __name__ == '__main__':
    pygame.init()

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (31, 165, 0)
    RED = (210, 28, 28)
    WIDTH, HEIGHT = 800, 600

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Akinator Star Wars')

    font = pygame.font.Font(None, 36)
    respostas = []

    background_image = pygame.image.load('fundo.png').convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    perguntas = [
        ("É droid? ", "droid"),
        ("É humano? ", "humano"),
        ("É alien? ", "alien"),
        ("É/Foi jedi? ", "jedi"),
        ("É/Foi sith? ", "sith"),
        ("Esteve em filme? ", "filme"),
        ("Esteve em serie? ", "serie"),
        ("É/Foi politico? ", "politico"),
        ("É clone? ", "clone"),
        ("É/Foi rebelde? ", "rebelde"),
        ("É mandaloriano? ", "mandaloriano"),
        ("É/Foi imperial? ", "imperial"),
        ("Morto em tela? ", "morto"),
        ("É defeituoso? ", "defeituoso"),
        ("É militar? ", "militar"),
        ("É entendível? ", "entendivel"),
        ("Tem corpo incompleto? ", "corpo incompleto"),
        ("Faz parte de um grupo? ", "grupo"),
        ("Foi exilado ou se revoltou? ", "renegado"),
        ("É 2 caras? ", "2 caras"),
        ("É genio? ", "genio"),
        ("É piloto? ", "piloto"),
        ("Aparece como criança/adolescente? ", "crianca/adolescente"),
        ("É/Foi caçador de recompensas? ", "cacador")
    ]

    clock = pygame.time.Clock()

    database = load_database('Akinator.txt.xlsx')

    if not database:
        screen.fill(WHITE)
        text_surface = font.render("Não há personagens na base de dados.", True, BLACK)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        pygame.quit()
        sys.exit()
    else:
        game_loop(database, perguntas)
