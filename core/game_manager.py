import random
from settings import *
from core.score_manager import ScoreManager

class GameManager:
    def __init__(self):
        # STRUKTUR FSM V1.9.2: Rangkaian Intro Sinematik & Transisi Menu Universal
        # State: INTRO_STUDIO, INTRO_PRODUCER, INTRO_DISCLAIMER, MAIN_MENU, SETTINGS_MENU, CREDIT, MODE_SELECT, TUTORIAL, MEMORIZE, PLAY, GAME_OVER, CONFIRM
        self.current_state = 'INTRO_STUDIO'
        self.previous_state = 'INTRO_STUDIO'
        self.confirm_type = ''  # 'MENYERAH', 'KELUAR_MENU', 'KELUAR_APP'
        
        self.score = 0
        self.level = 1
        self.selected_mode = 'EASY'
        
        # Pengaturan Sistem Global
        self.volume_bgm = 70       
        self.volume_sfx = 80       
        self.is_fullscreen = False 
        
        self.settings_index = 0
        self.settings_options = ['BGM VOLUME', 'SFX VOLUME', 'FULLSCREEN', 'KEMBALI']
        
        self.score_sys = ScoreManager()
        self.high_score = self.score_sys.high_score
        self.new_record_achieved = False
        self.indicator_light = False 

        # CONFIGURATION DURASI INTRO DINAMIS SINKRON
        self.intro_durations = {
            'INTRO_STUDIO': 3000,      # 3 Detik Logo Studio
            'INTRO_PRODUCER': 3000,    # 3 Detik Logo Kampus
            'INTRO_DISCLAIMER': 8000   # 8 Detik Membaca Peringatan Medis
        }
        
        # Timer awal mengambil data durasi INTRO_STUDIO secara dinamis
        self.state_timer = self.intro_durations['INTRO_STUDIO']

        self.disclaimer_messages = [
            "PERINGATAN: GAME INI MENGANDUNG UNSUR HOROR",
            "",
            "Game ini ditujukan untuk audiens dewasa. Di dalamnya terdapat",
            "adegan kejutan mendadak (jumpscares), serta kilatan cahaya",
            "yang dapat memicu kejang bagi penderita epilepsi fotosensitif.",
            "",
            "Kebijaksanaan pemain sangat diharapkan. Jika Anda merasa",
            "tidak nyaman, harap segera hentikan permainan.",
            "",
            "",
            "",
            "<Tekan Dimana Saja Untuk Skip!>"
        ]

        # Data Tutorial Terstruktur Multiline (Mencegah Teks Keluar Kotak)
        self.tutorial_step = 0
        self.tutorial_messages = [
            ["FASE 1: HAFALAN", "Ingat baik-baik urutan warna menara target", "yang muncul di layar dalam beberapa detik!"],
            ["FASE 2: EKSEKUSI", "Gunakan tombol warna / Klik Mouse untuk", "membangun kembali menara dari bawah ke atas."],
            ["ATURAN STACK (LIFO)", "Jika salah susun, Anda WAJIB menekan POP", "untuk menghapus balok paling atas dahulu!"],
            ["VALIDASI AKHIR", "Jika susunan sudah yakin sama dengan target,", "klik VALIDASI atau tekan ENTER untuk menang!"]
        ]

        self.inner_monologue_text = ""
        self.inner_monologue_timer = 0 
        self.panic_phrases = [
            "Aduh, salah susun! Ingat prinsip LIFO balok teratas!",
            "Sial, bukan warna itu! Segera lakukan POP untuk membuangnya!",
            "Gawat, monster semakin dekat! Fokus hafalannya!",
            "Jangan panik! Buang balok atas yang salah dengan tombol POP!"
        ]

        self.memorize_duration = 5000  
        self.play_duration = 60000     
        self.available_colors = ["Merah", "Biru", "Kuning", "Hijau"]
        self.target_blueprint = []
        
        self.menu_options = ['MULAI', 'PENGATURAN', 'CREDIT', 'KELUAR']
        self.menu_index = 0
        
        self.mode_index = 0
        self.modes_list = ['EASY', 'MEDIUM', 'HARD', 'IMPOSSIBLE', 'UNLIMITED']
        self.mode_requirements = {'EASY': 0, 'MEDIUM': 1000, 'HARD': 3000, 'IMPOSSIBLE': 5000, 'UNLIMITED': 0}
        
        self.confirm_index = 1 
        self.game_over_index = 0
        self.game_over_options = ['ULANG PERMAINAN', 'UBAH MODE KESULITAN', 'KEMBALI KE MENU']

        self.team_members = [
            "1. Ihsan Dwi Putra (15250094)",
            "2. Muhammad Imam Baihaqi (15250004)",
            "3. Aldo Farisanrya. R (15250145)",
            "4. Andika Tri Sapto (15250146)",
            "5. Azlan (1250222)"
        ]

    def update_timer(self, delta_time):
        self.update_inner_timer(delta_time)
        
        if self.current_state in ['INTRO_STUDIO', 'INTRO_PRODUCER', 'INTRO_DISCLAIMER']:
            self.state_timer -= delta_time
            if self.state_timer <= 0:
                self.skip_intro()
                
        elif self.current_state in ['MEMORIZE', 'PLAY']:
            self.state_timer -= delta_time
            if self.state_timer <= 0:
                if self.current_state == 'MEMORIZE':
                    self.current_state = 'PLAY'
                    self.state_timer = self.play_duration
                    self.indicator_light = True
                elif self.current_state == 'PLAY':
                    self.trigger_game_over()

    def skip_intro(self):
        """Mekanisme lompat intro dinamis berdasarkan Dictionary Mapping."""
        if self.current_state == 'INTRO_STUDIO':
            self.current_state = 'INTRO_PRODUCER'
            self.state_timer = self.intro_durations['INTRO_PRODUCER']
        elif self.current_state == 'INTRO_PRODUCER':
            self.current_state = 'INTRO_DISCLAIMER'
            self.state_timer = self.intro_durations['INTRO_DISCLAIMER']
        elif self.current_state == 'INTRO_DISCLAIMER':
            self.current_state = 'MAIN_MENU'
            self.state_timer = 0

    def get_lock_status(self, mode_name):
        return self.high_score < self.mode_requirements[mode_name]

    def generate_new_level(self):
        self.target_blueprint = []
        if self.selected_mode == 'EASY':
            num_blocks = 3
            self.memorize_duration = 5000  
            self.play_duration = 60000     
        elif self.selected_mode == 'MEDIUM':
            num_blocks = 5
            self.memorize_duration = 6000  
            self.play_duration = 45000     
        elif self.selected_mode == 'HARD':
            num_blocks = 7                 
            self.memorize_duration = 7000  
            self.play_duration = 30000     
        elif self.selected_mode == 'IMPOSSIBLE':
            num_blocks = 10
            self.memorize_duration = 5000  
            self.play_duration = 15000     
        elif self.selected_mode == 'UNLIMITED':
            num_blocks = 3 + (self.level // 2)
            self.memorize_duration = max(3000, 5000 - (self.level * 200))
            self.play_duration = max(15000, 60000 - (self.level * 2000))

        for _ in range(num_blocks):
            self.target_blueprint.append(random.choice(self.available_colors))
        
        self.state_timer = self.memorize_duration
        self.indicator_light = True

    def trigger_inner_monologue(self):
        self.inner_monologue_text = random.choice(self.panic_phrases)
        self.inner_monologue_timer = 3000

    def update_inner_timer(self, delta_time):
        if self.inner_monologue_timer > 0:
            self.inner_monologue_timer -= delta_time
            if self.inner_monologue_timer <= 0:
                self.inner_monologue_text = ""

    def trigger_confirm(self, confirm_type):
        self.previous_state = self.current_state
        self.confirm_type = confirm_type
        self.confirm_index = 1 
        self.current_state = 'CONFIRM'

    def cancel_confirm(self):
        self.current_state = self.previous_state

    def trigger_game_over(self):
        self.current_state = 'GAME_OVER'
        self.state_timer = 0
        self.indicator_light = False
        self.inner_monologue_text = ""
        self.new_record_achieved = self.score_sys.update_high_score(self.score)

    def handle_success(self):
        multiplier = {'EASY': 100, 'MEDIUM': 200, 'HARD': 350, 'IMPOSSIBLE': 500, 'UNLIMITED': 150}
        self.score += multiplier.get(self.selected_mode, 100)
        self.level += 1
        self.current_state = 'MEMORIZE'
        self.generate_new_level()

    def restart_level(self):
        self.score = 0
        self.level = 1
        self.new_record_achieved = False
        self.generate_new_level()
        self.current_state = 'MEMORIZE'

    def reset_to_menu(self):
        self.score = 0
        self.level = 1
        self.new_record_achieved = False
        self.high_score = self.score_sys.load_high_score()
        self.current_state = 'MAIN_MENU'