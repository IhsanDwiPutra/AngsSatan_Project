import pygame
from settings import *

class TowerRenderer:
    def __init__(self):
        # Dimensi satu blok di layar
        self.block_width = 200
        self.block_height = 40
        
        # Posisi horizontal tengah layar
        self.center_x = SCREEN_WIDTH // 2 - (self.block_width // 2)
        
        # Batas bawah/dasar menara berdiri di layar
        self.base_y = 500 

        # Mapping string warna ke warna RGB asli dari settings.py
        self.color_map = {
            "Merah": COLOR_RED,
            "Biru": COLOR_BLUE,
            "Kuning": COLOR_YELLOW,
            "Hijau": COLOR_GREEN
        }

    def draw_player_tower(self, screen, player_stack_items):
        """
        Menggambar tumpukan stack pemain dari bawah ke atas.
        Elemen pertama di dalam list (index 0) menjadi dasar menara.
        """
        for index, block_color_name in enumerate(player_stack_items):
            # Mengambil warna RGB berdasarkan teks nama warna
            rgb_color = self.color_map.get(block_color_name, COLOR_WHITE)
            
            # Kalkulasi Cantik: Mengurangi Y berdasarkan indeks agar menumpuk ke atas
            current_y = self.base_y - (index * (self.block_height + 5))
            
            # Membuat objek kotak (Rect) Pygame
            block_rect = pygame.Rect(self.center_x, current_y, self.block_width, self.block_height)
            
            # Menggambar kotak ke layar
            pygame.draw.rect(screen, rgb_color, block_rect)
            
            # Opsional: Memberi garis tepi hitam tipis agar antar-blok terlihat terpisah
            pygame.draw.rect(screen, (0, 0, 0), block_rect, 2)