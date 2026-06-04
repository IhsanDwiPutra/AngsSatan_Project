import random
from settings import *
from core.score_manager import ScoreManager  # Injeksi Modul Baru

class GameManager:
    def __init__(self):
        self.current_state = 'MEMORIZE'
        self.score = 0
        self.level = 1
        
        # Inisialisasi Score Manager
        self.score_sys = ScoreManager()
        self.high_score = self.score_sys.high_score
        self.new_record_achieved = False # Indikator psikologis untuk UI

        self.memorize_duration = 3000  
        self.play_duration = 60000      
        self.state_timer = self.memorize_duration
        
        self.available_colors = ["Merah", "Biru", "Kuning", "Hijau"]
        self.target_blueprint = []
        self.generate_new_level()

    def generate_new_level(self):
        self.target_blueprint = []
        if self.level <= 2:
            num_blocks = 3  
        elif self.level <= 5:
            num_blocks = 5  
        else:
            num_blocks = 7  
            
        for _ in range(num_blocks):
            self.target_blueprint.append(random.choice(self.available_colors))
        print(f"[SISTEM] Level {self.level} Dimulai! Target: {self.target_blueprint}")

    def update_timer(self, delta_time):
        self.state_timer -= delta_time
        
        if self.state_timer <= 0:
            if self.current_state == 'MEMORIZE':
                self.current_state = 'PLAY'
                self.state_timer = self.play_duration
            elif self.current_state == 'PLAY':
                self.current_state = 'GAME_OVER'
                self.state_timer = 0
                # AUDIT SKOR: Cek apakah skor akhir memecahkan rekor lokal
                self.new_record_achieved = self.score_sys.update_high_score(self.score)

    def handle_success(self):
        self.score += 100
        self.level += 1
        self.current_state = 'MEMORIZE'
        self.state_timer = self.memorize_duration
        self.generate_new_level()

    def reset_game(self):
        self.score = 0
        self.level = 1
        self.new_record_achieved = False
        # Ambil kembali high score terbaru dari file untuk refresh data
        self.high_score = self.score_sys.load_high_score()
        self.current_state = 'MEMORIZE'
        self.state_timer = self.memorize_duration
        self.generate_new_level()