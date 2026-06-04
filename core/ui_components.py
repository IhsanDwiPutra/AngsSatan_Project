import pygame
from settings import *

class Button:
    def __init__(self, x, y, width, height, text, base_color, hover_color, font_size=24):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.base_color = base_color
        self.hover_color = hover_color
        self.current_color = base_color
        self.font = pygame.font.SysFont("Consolas", font_size)
        
        # Status internal tombol
        self.is_hovered = False

    def update(self, mouse_pos):
        """Memeriksa apakah mouse sedang berada di atas tombol (Hover Effect)."""
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hover_color
            self.is_hovered = True
        else:
            self.current_color = self.base_color
            self.is_hovered = False

    def draw(self, screen):
        """Menggambar kotak tombol dan teks di tengahnya."""
        pygame.draw.rect(screen, self.current_color, self.rect)
        pygame.draw.rect(screen, COLOR_WHITE, self.rect, 2) # Garis tepi putih
        
        text_surf = self.font.render(self.text, True, COLOR_WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event, mouse_pos):
        """Memeriksa apakah tombol ini diklik oleh mouse kiri."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(mouse_pos):
                return True
        return False