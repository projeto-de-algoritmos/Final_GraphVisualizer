import pygame
from cell import *
import sys

WIDTH = 700
HEIGHT = 700

RES = WIDTH, HEIGHT

MENU = 1
START = 2
OPTION = 3
CONTROL = 4

cols = 25
rows = 25

size_w = WIDTH // cols
size_h = HEIGHT // rows

pygame.init()
screen = pygame.display.set_mode(RES)
clock = pygame.time.Clock()
pygame.display.set_caption("Menu")

pygame.mixer.music.load('src/assets/bckg.wav')
pygame.mixer.music.play(-1)


def draw_error_rect_and_text():
    pygame.draw.rect(screen, (20, 20, 20), (150, 250, 400, 200))
    text = pygame.font.Font("src/assets/font.ttf",
                            17).render("O algoritmo não", True, (200, 200, 200))
    rect = text.get_rect(center=(335, 320))
    text2 = pygame.font.Font(
        "src/assets/font.ttf", 17).render("encontrou a solução...", True, (200, 200, 200))
    rect2 = text.get_rect(center=(300, 350))
    text3 = pygame.font.Font("src/assets/font.ttf", 9).render(
        "aperte R para retornar ao menu", True, (200, 200, 200))
    rect3 = text.get_rect(center=(330, 420))
    screen.blit(text, rect)
    screen.blit(text2, rect2)
    screen.blit(text3, rect3)


def draw_alpha_screen():
    rect = (0, 0, 700, 700)
    shape = pygame.Surface(pygame.Rect(rect).size)
    shape.set_alpha(50)
    pygame.draw.rect(shape, 'white', shape.get_rect())
    screen.blit(shape, rect)

def draw_help_box():
    rect = (500, 25, 190, 100)
    shape = pygame.Surface(pygame.Rect(rect).size)
    shape.set_alpha(100)
    pygame.draw.rect(shape, (200,250,250), shape.get_rect())
    screen.blit(shape, rect)
    text = pygame.font.Font("src/assets/font.ttf", 13).render("A -> DJIKSTRA", True, (0,250,250))
    rect = text.get_rect(center=(600, 50))
    text2 = pygame.font.Font("src/assets/font.ttf", 13).render("B -> BFS", True, (0,250,250))
    rect2 = text.get_rect(center=(600, 75))
    text3 = pygame.font.Font("src/assets/font.ttf", 13).render("R -> MENU", True, (0,250,250))
    rect3 = text.get_rect(center=(600, 100))
    screen.blit(text, rect)
    screen.blit(text2, rect2)
    screen.blit(text3, rect3)


def start():
    init_search = False
    bfs_search = False
    dfs_search = False
    is_target_set = False
    is_start_set = False
    search = True
    cells = []
    queue = []
    path = []

    for i in range(cols):
        temp = []
        for j in range(rows):
            temp.append(Cell(i, j, size_w, size_h, screen))
        cells.append(temp)

    for i in range(cols):
        for j in range(rows):
            cells[i][j].set_neighbours(cols, rows, cells)

    start_cell = cells[0][0]
    start_cell.start = True
    start_cell.visited = True
    queue.append(start_cell)

    while True:
        screen.fill(pygame.Color('darkslategrey'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    init_search = False
                    is_target_set = False
                    is_start_set = False
                    bfs_search = False
                    dfs_search = False
                    search = True
                    cells = []
                    start_cell = None
                    queue = []
                    return MENU
                if event.key == pygame.K_a and is_target_set:
                    init_search = True
                if event.key == pygame.K_b and is_target_set:
                    bfs_search = True
                if event.key == pygame.K_c and is_target_set:
                    dfs_search = True
            elif event.type == pygame.MOUSEMOTION:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                if event.buttons[0]:
                    i = x // size_w
                    j = y // size_h
                    cells[i][j].walls = True
                if event.buttons[1] and not is_start_set:
                    i = x // size_w
                    j = y // size_h
                    first_cell = cells[i][j]
                    first_cell.start = True
                if event.buttons[2] and not is_target_set:
                    i = x // size_w
                    j = y // size_h
                    last_cell = cells[i][j]
                    last_cell.target = True
                    is_target_set = True

        for i in range(cols):
            for j in range(rows):
                cell = cells[i][j]
                cell.draw_cell(path)

        if init_search:
            if len(queue) > 0 and search:
                current_cell = queue.pop(0)
                current_cell.visited = True
                if current_cell == last_cell:
                    search = False
                    while current_cell.prior != start_cell:
                        path.append(current_cell.prior)
                        current_cell = current_cell.prior
                else:
                    for neighbour in current_cell.neighbours:
                        if not neighbour.queue and not neighbour.walls:
                            neighbour.queue = True
                            neighbour.prior = current_cell
                            queue.append(neighbour)
            else:
                if search:
                    draw_alpha_screen()
                    draw_error_rect_and_text()

        elif bfs_search:
            if len(queue) > 0:
                cell = queue.pop(0)
                cell.visited = True
                for node in cell.neighbours:
                    if node.visited == False and node.walls == False:
                        node.visited = True
                        node.prior = cell
                        queue.append(node)
                    elif node == last_cell:
                        current_cell = node.prior
                        while current_cell != last_cell and current_cell != None:
                            path.append(current_cell)
                            current_cell = current_cell.prior
                        search = False
                        break
            else:
                if search:
                    draw_alpha_screen()
                    draw_error_rect_and_text()

        draw_help_box()               
        pygame.display.flip()


def options():
    global cols, rows, size_w, size_h

    while True:
        screen.fill((50, 50, 50))
        text = pygame.font.Font("src/assets/font.ttf",
                                90).render("OPÇÕES", True, "#ff5733")
        rect = text.get_rect(center=(350, 100))
        t_grid = pygame.font.Font("src/assets/font.ttf", 18).render(
            f"Quantidade de colunas e linhas = {cols}", True, '#a95ab8')
        r_grid = text.get_rect(center=(330, 250))
        text2 = pygame.font.Font(
            "src/assets/font.ttf", 22).render("Aperte A para aumentar o grid!", True, "#ffb500")
        rect2 = text.get_rect(center=(330, 350))
        text3 = pygame.font.Font(
            "src/assets/font.ttf", 22).render("Aperte D para diminuir o grid!", True, "#ff2a9e")
        rect3 = text.get_rect(center=(330, 450))
        text4 = pygame.font.Font(
            "src/assets/font.ttf", 23).render("Aperte Q para sair do jogo.", True, "#33ffb8")
        rect4 = text.get_rect(center=(330, 550))
        text5 = pygame.font.Font(
            "src/assets/font.ttf", 23).render("Aperte R para voltar ao menu.", True, "#33ff5b")
        rect5 = text.get_rect(center=(330, 650))

        screen.blit(text, rect)
        screen.blit(t_grid, r_grid)
        screen.blit(text2, rect2)
        screen.blit(text3, rect3)
        screen.blit(text4, rect4)
        screen.blit(text5, rect5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    if cols < 100:
                        cols *= 2
                        rows *= 2
                        size_w = WIDTH // cols
                        size_h = HEIGHT // rows

                elif event.key == pygame.K_d:
                    if cols > 25:
                        cols //= 2
                        rows //= 2
                        size_w = WIDTH // cols
                        size_h = HEIGHT // rows
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    return MENU
        pygame.display.update()


def controls():
    while True:
        screen.fill((50, 50, 50))
        text = pygame.font.Font("src/assets/font.ttf",
                                65).render("Controles", True, "#ff5733")
        rect = text.get_rect(center=(350, 150))
        text2 = pygame.font.Font("src/assets/font.ttf", 14).render(
            "Botão esquerdo do mouse -> criar obstáculos", True, "#ffb500")
        rect2 = text.get_rect(center=(370, 350))
        text3 = pygame.font.Font("src/assets/font.ttf", 14).render(
            "Botão direito do mouse -> marca célula alvo", True, "#ff2a9e")
        rect3 = text.get_rect(center=(375, 450))
        text4 = pygame.font.Font(
            "src/assets/font.ttf", 19).render("R para retornar ao menu", True, "#33ffb8")
        rect4 = text.get_rect(center=(450, 550))
        screen.blit(text, rect)
        screen.blit(text2, rect2)
        screen.blit(text3, rect3)
        screen.blit(text4, rect4)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return MENU
        pygame.display.update()


def menu():
    while True:
        screen.fill((50, 50, 50))
        text = pygame.font.Font("src/assets/font.ttf",
                                100).render("MENU", True, "#ff5733")
        rect = text.get_rect(center=(350, 150))
        text2 = pygame.font.Font(
            "src/assets/font.ttf", 22).render("Aperte A para comecar!", True, "#ffb500")
        rect2 = text.get_rect(center=(330, 350))
        text3 = pygame.font.Font(
            "src/assets/font.ttf", 22).render("Aperte O para opcoes", True, "#ff2a9e")
        rect3 = text.get_rect(center=(330, 450))
        text4 = pygame.font.Font(
            "src/assets/font.ttf", 22).render("Aperte Q para sair", True, "#33ffb8")
        rect4 = text.get_rect(center=(330, 550))
        text5 = pygame.font.Font(
            "src/assets/font.ttf", 22).render("Aperte C para controles", True, "#33ff5b")
        rect5 = text.get_rect(center=(330, 650))

        screen.blit(text, rect)
        screen.blit(text2, rect2)
        screen.blit(text3, rect3)
        screen.blit(text4, rect4)
        screen.blit(text5, rect5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    start()
                elif event.key == pygame.K_o:
                    options()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_c:
                    controls()
        pygame.display.update()


def main():
    while True:
        if scene == MENU:
            scene = menu()
        elif scene == START:
            scene = start()
        elif scene == OPTION:
            scene = options()
        elif scene == CONTROL:
            scene == controls()


if __name__ == '__main__':
    menu()
