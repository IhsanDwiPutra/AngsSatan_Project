import pygame
from settings import *

class AbyssalMonster:
    def __init__(self):
        # Monster mulai dari luar layar sebelah kiri (koordinat X negatif)
        self.start_x = -100
        
        # Batas akhir monster (tepat di depan menara pemain)
        # Menara berada di tengah, jadi kita set batas deteksi cakar monster di dekatnya
        self.target_x = SCREEN_WIDTH // 2 - 150
        
        self.current_x = self.start_x

    def update(self, time_left_ms, total_time_ms):
        """
        Logika Cantik: Mengikat posisi X monster dengan laju milidetik waktu.
        Semakin sedikit waktu tersisa, monster semakin mendekati target_x.
        """
        if time_left_ms <= 0:
            self.current_x = self.target_x
        else:
            # Menghitung rasio waktu yang sudah berjalan (0.0 sampai 1.0)
            time_elapsed_ratio = (total_time_ms - time_left_ms) / total_time_ms
            
            # Formula Linear: Menggeser X berdasarkan rasio waktu
            self.current_x = self.start_x + (time_elapsed_ratio * (self.target_x - self.start_x))

    def draw(self, screen):
        """Menggambar manifestasi monster berupa bayangan hitam pekat dengan aura merah."""
        if self.current_x > self.start_x:
            # 1. Menggambar tubuh bayangan hitam dari ujung kiri layar hingga koordinat current_x
            shadow_rect = pygame.Rect(0, 0, int(self.current_x + 100), SCREEN_HEIGHT)
            pygame.draw.rect(screen, (10, 12, 18), shadow_rect)
            
            # 2. Menggambar "Garis Merah Darah" di depan bayangan sebagai indikator batas ancaman
            pygame.draw.line(
                screen, 
                (180, 0, 0), 
                (self.current_x + 100, 0), 
                (self.current_x + 100, SCREEN_HEIGHT), 
                4
            )