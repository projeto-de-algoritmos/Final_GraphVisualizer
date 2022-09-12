import pygame

class Cell:
    def __init__(self, x, y, size_w, size_h, screen):
        self.x = x
        self.y = y
        self.size_w = size_w
        self.size_h = size_h
        self.screen = screen
        self.walls = False
        self.target = False
        self.start = False
        self.queue = False
        self.visited = False
        self.neighbours = []
        self.prior = None

    def draw(self, win, color):
        pygame.draw.rect(win, color, (self.x * self.size_w, self.y * self.size_h, self.size_w-2, self.size_h-2))

    def draw_cell(self, path):
        x = self.x * self.size_w
        y = self.y * self.size_h

        
        if self.walls:
            pygame.draw.rect(self.screen, (200,250,250), (x, y, self.size_w - 2, self.size_h - 2))
        else:
            pygame.draw.rect(self.screen, (20,20,20), (x, y, self.size_w - 2, self.size_h - 2))
        if self.queue:
            pygame.draw.rect(self.screen, (200, 0, 0), (x, y, self.size_w - 2, self.size_h - 2))
        if self.visited:
            pygame.draw.rect(self.screen, (0, 200, 0), (x, y, self.size_w - 2, self.size_h - 2))
        if self in path:
            pygame.draw.rect(self.screen, (0, 0, 200), (x, y, self.size_w - 2, self.size_h - 2))
        if self.start:
            pygame.draw.rect(self.screen, (0, 200, 200), (x, y, self.size_w - 2, self.size_h - 2))
        if self.target:
            pygame.draw.rect(self.screen, (200, 200, 0), (x, y, self.size_w - 2, self.size_h - 2))
            
    
    def set_neighbours(self, cols, rows, cells):
            if self.x > 0:
                self.neighbours.append(cells[self.x - 1][self.y])
            if self.x < cols - 1:
                self.neighbours.append(cells[self.x + 1][self.y])
            if self.y > 0:
                self.neighbours.append(cells[self.x][self.y - 1])
            if self.y < rows - 1:
                self.neighbours.append(cells[self.x][self.y + 1])
            
