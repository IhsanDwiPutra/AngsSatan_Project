import pygame
import sys
import os
import random
from settings import *
from core.stack_logic import AbyssalStack
from core.game_manager import GameManager
from core.ui_components import Button
from entities.tower import TowerRenderer
from entities.monster import AbyssalMonster

pygame.init()
pygame.font.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED)
pygame.display.set_caption("angSSatan v2.1.3")
clock = pygame.time.Clock()
font_title = pygame.font.SysFont("Consolas", 42, bold=True)
font_menu = pygame.font.SysFont("Consolas", 24)
font_tut = pygame.font.SysFont("Consolas", 18)
font_small = pygame.font.SysFont("Consolas", 14) 
font_batin = pygame.font.SysFont("Consolas", 20, italic=True)

def main():
    global screen 
    
    manager = GameManager()
    player_stack = AbyssalStack(manager.target_blueprint)
    tower_renderer = TowerRenderer()
    monster = AbyssalMonster()

    # ==========================================
    # PIPELINE INTEGRASI ASET AUDIO MULTI-CHANNEL
    # ==========================================
    audio_path = os.path.join("assets", "audio", "startup.mp3")
    if os.path.exists(audio_path):
        try:
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.set_volume(manager.volume_sfx / 100)
            pygame.mixer.music.play(0)
        except pygame.error: pass

    hover_sfx, click_sfx = None, None
    block_push_sfx, block_pop_sfx, success_sfx, error_sfx = None, None, None, None
    
    try:
        if os.path.exists(os.path.join("assets", "audio", "hover.wav")):
            hover_sfx = pygame.mixer.Sound(os.path.join("assets", "audio", "hover.wav"))
        if os.path.exists(os.path.join("assets", "audio", "click.wav")):
            click_sfx = pygame.mixer.Sound(os.path.join("assets", "audio", "click.wav"))
            
        if os.path.exists(os.path.join("assets", "audio", "block_push.wav")):
            block_push_sfx = pygame.mixer.Sound(os.path.join("assets", "audio", "block_push.wav"))
        if os.path.exists(os.path.join("assets", "audio", "block_pop.wav")):
            block_pop_sfx = pygame.mixer.Sound(os.path.join("assets", "audio", "block_pop.wav"))
        if os.path.exists(os.path.join("assets", "audio", "success.wav")):
            success_sfx = pygame.mixer.Sound(os.path.join("assets", "audio", "success.wav"))
        if os.path.exists(os.path.join("assets", "audio", "error.wav")):
            error_sfx = pygame.mixer.Sound(os.path.join("assets", "audio", "error.wav"))
    except pygame.error: pass

    def play_sfx(sound_obj):
        if sound_obj:
            sound_obj.set_volume(manager.volume_sfx / 100)
            sound_obj.play()

    def play_hover(): play_sfx(hover_sfx)
    def play_click(): play_sfx(click_sfx)
    def play_push(): play_sfx(block_push_sfx)
    def play_pop(): play_sfx(block_pop_sfx)
    def play_success(): play_sfx(success_sfx)
    def play_error(): play_sfx(error_sfx)

    current_bgm_state = 'INTRO'

    # ==========================================
    # PIPELINE GAMBAR & VIDEO BG LOOP
    # ==========================================
    img_studio_path = os.path.join("assets", "sprites", "studio_logo.png")
    studio_logo_image = None
    if os.path.exists(img_studio_path):
        try:
            studio_logo_image = pygame.image.load(img_studio_path).convert_alpha()
            studio_logo_image = pygame.transform.scale(studio_logo_image, (350, 250))
        except pygame.error: pass

    img_ubsi_path = os.path.join("assets", "sprites", "ubsi_logo.png")
    ubsi_logo_image = None
    if os.path.exists(img_ubsi_path):
        try:
            ubsi_logo_image = pygame.image.load(img_ubsi_path).convert_alpha()
            ubsi_logo_image = pygame.transform.scale(ubsi_logo_image, (150, 150))
        except pygame.error: pass

    img_menu_logo_path = os.path.join("assets", "sprites", "menu_logo.png")
    menu_logo_image = None
    if os.path.exists(img_menu_logo_path):
        try:
            menu_logo_image = pygame.image.load(img_menu_logo_path).convert_alpha()
            menu_logo_image = pygame.transform.scale(menu_logo_image, (320, 120))
        except pygame.error: pass

    img_mode_bg_path = os.path.join("assets", "sprites", "mode_bg.png")
    if not os.path.exists(img_mode_bg_path): 
        img_mode_bg_path = os.path.join("assets", "sprites", "mode_bg.jpg")
    mode_bg_image = None
    if os.path.exists(img_mode_bg_path):
        try:
            mode_bg_image = pygame.image.load(img_mode_bg_path).convert()
            mode_bg_image = pygame.transform.scale(mode_bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except pygame.error: pass

    img_settings_bg_path = os.path.join("assets", "sprites", "settings_bg.png")
    if not os.path.exists(img_settings_bg_path): 
        img_settings_bg_path = os.path.join("assets", "sprites", "settings_bg.jpg")
    settings_bg_image = None
    if os.path.exists(img_settings_bg_path):
        try:
            settings_bg_image = pygame.image.load(img_settings_bg_path).convert()
            settings_bg_image = pygame.transform.scale(settings_bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except pygame.error: pass
        
    # === S1: PEMUAT ASET MONSTER JUMPSCARE ===
    img_monster_path = os.path.join("assets", "sprites", "monster.png")
    if not os.path.exists(img_monster_path): img_monster_path = os.path.join("assets", "sprites", "monster.jpg")
    monster_image = None
    if os.path.exists(img_monster_path):
        try:
            # Menyimpan gambar mentah murni agar tidak pecah saat di-scale up
            monster_image = pygame.image.load(img_monster_path).convert_alpha()
        except pygame.error: pass    
    
    img_tutorial_bg_path = os.path.join("assets", "sprites", "tutorial_bg.png")
    if not os.path.exists(img_tutorial_bg_path): 
        img_tutorial_bg_path = os.path.join("assets", "sprites", "tutorial_bg.jpg")
    tutorial_bg_image = None
    # === S1: PEMUAT BACKGROUND MODE SPESIFIK ===
    bg_modes_images = {}
    for m in ['EASY', 'MEDIUM', 'HARD', 'IMPOSSIBLE', 'UNLIMITED']:
        # Fallback semua mode unlimited ke easy per instruksi Anda
        file_name = "easy_bg.png" if m == 'UNLIMITED' else f"{m.lower()}_bg.png"
        m_path = os.path.join("assets", "sprites", file_name)
        if not os.path.exists(m_path): m_path = os.path.join("assets", "sprites", file_name.replace('.png', '.jpg'))
        
        if os.path.exists(m_path):
            try:
                img = pygame.image.load(m_path).convert()
                bg_modes_images[m] = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
            except pygame.error: pass
        # === S1: BG FASE PENGINGAT (MEMORIZE) ===
        img_memorize_bg_path = os.path.join("assets", "sprites", "fase_memorize.png")
        if not os.path.exists(img_memorize_bg_path): 
            img_memorize_bg_path = os.path.join("assets", "sprites", "fase_memorize.jpg")
        memorize_bg_image = None
        if os.path.exists(img_memorize_bg_path):
            try:
                memorize_bg_image = pygame.image.load(img_memorize_bg_path).convert()
                memorize_bg_image = pygame.transform.scale(memorize_bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            except pygame.error: pass    
    if os.path.exists(img_tutorial_bg_path):
        try:
            tutorial_bg_image = pygame.image.load(img_tutorial_bg_path).convert()
            tutorial_bg_image = pygame.transform.scale(tutorial_bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except pygame.error: pass

    video_frames_dir = os.path.join("assets", "video_frames")
    frame_files = []
    if os.path.exists(video_frames_dir):
        frame_files = sorted([f for f in os.listdir(video_frames_dir) if f.endswith(('.png', '.jpg', '.jpeg'))])
    current_frame_index = 0
    frame_timer = 0
    frame_duration = 40  
    cached_frame_img = None
    cached_frame_idx = -1
    
    # Variabel Pemuat Ruang Bermain (Loading Screen)
    loading_timer = 0
    current_hint = ""

    # ==========================================
    # INITIALIZATION INTERACTIVE BUTTONS
    # ==========================================
    btn_menu_options = [
        Button(40, 220, 260, 50, "MULAI", (40, 45, 60), (60, 70, 100), font_size=22),
        Button(40, 290, 260, 50, "PENGATURAN", (40, 45, 60), (60, 70, 100), font_size=22),
        Button(40, 360, 260, 50, "CREDIT", (40, 45, 60), (60, 70, 100), font_size=22),
        Button(40, 430, 260, 50, "KELUAR", (40, 45, 60), (120, 40, 40), font_size=22)
    ]

    btn_bgm_slider = Button(350, 195, 180, 25, "", (0, 0, 0), (0, 0, 0)) 
    btn_sfx_slider = Button(350, 255, 180, 25, "", (0, 0, 0), (0, 0, 0)) 
    # --- RENOVASI v2.1.0: Tombol UBAH dan Kotak OFF dilebur menjadi SATU tombol lebar! ---
    # Teks sengaja dikosongkan ("") agar bisa kita render dinamis (ON/OFF) di perulangan visual
    btn_fs_toggle  = Button(350, 310, 160, 35, "", (50, 60, 80), (80, 100, 140))
    btn_settings_kembali = Button(SCREEN_WIDTH//2 - 120, 400, 240, 40, "KEMBALI KE MENU", (80, 80, 80), (50, 50, 50))
    btn_credit_kembali = Button(SCREEN_WIDTH//2 - 140, 490, 280, 50, "KEMBALI KE MENU", (40, 45, 60), (50, 50, 50), font_size=22)

    btn_modes = {
        'EASY':       Button(40, 150, 420, 60, "", (40, 45, 60), (60, 70, 100)),
        'MEDIUM':     Button(40, 220, 420, 60, "", (40, 45, 60), (60, 70, 100)),
        'HARD':       Button(40, 290, 420, 60, "", (40, 45, 60), (60, 70, 100)),
        'IMPOSSIBLE': Button(40, 360, 420, 60, "", (40, 45, 60), (60, 70, 100)),
        'UNLIMITED':  Button(40, 430, 420, 60, "", (40, 45, 60), (60, 70, 100)),
    }
    btn_mode_kembali  = Button(480, 430, 280, 60, "[ESC] KEMBALI", (40, 45, 60), (120, 40, 40), font_size=22)

    # === S2: REPOSISI TOMBOL GAMEPLAY ===
    # Tombol Tumpukan Warna di Kiri Bawah
    btn_game_merah    = Button(20, 260, 140, 35, "[R] MERAH", COLOR_RED, (150, 30, 30), font_size=16)
    btn_game_biru     = Button(20, 305, 140, 35, "[B] BIRU", COLOR_BLUE, (30, 60, 150), font_size=16)
    btn_game_kuning   = Button(20, 350, 140, 35, "[Y] KUNING", COLOR_YELLOW, (150, 140, 30), font_size=16)
    btn_game_hijau    = Button(20, 395, 140, 35, "[G] HIJAU", COLOR_GREEN, (30, 130, 30), font_size=16)
    btn_game_pop      = Button(20, 440, 140, 35, "[BACK] POP", (100, 100, 100), (70, 70, 70), font_size=16)
    
    # Tombol Validasi di Tengah Bawah (Menyatu dengan Panel Box nanti)
    btn_game_validate = Button(SCREEN_WIDTH//2 - 90, 465, 180, 35, "[ENTER] VALIDASI", (40, 140, 70), (20, 90, 45), font_size=16)
    
    # Tombol Menyerah & Jeda di Kanan Bawah
    btn_game_menyerah = Button(SCREEN_WIDTH - 180, 400, 160, 35, "[M] MENYERAH", (180, 40, 40), (120, 30, 30), font_size=16)
    btn_game_jeda     = Button(SCREEN_WIDTH - 180, 445, 160, 35, "[ESC] JEDA", (80, 60, 40), (120, 80, 50), font_size=16)

    # Membangun 4 Tombol Menu Jeda — posisi dihitung dari tengah panel (panel_h=420, panel_y=center)
    _pause_panel_y = SCREEN_HEIGHT//2 - 210  # = panel_y saat panel_h=420
    _pause_btn_x   = SCREEN_WIDTH//2 - 140
    btn_pause_options = [
        Button(_pause_btn_x, _pause_panel_y + 100, 280, 40, "LANJUTKAN", (40, 45, 60), (60, 70, 100)),
        Button(_pause_btn_x, _pause_panel_y + 155, 280, 40, "ULANG LEVEL", (40, 45, 60), (60, 70, 100)),
        Button(_pause_btn_x, _pause_panel_y + 210, 280, 40, "PENGATURAN", (40, 45, 60), (60, 70, 100)),
        Button(_pause_btn_x, _pause_panel_y + 265, 280, 40, "KEMBALI KE MENU", (40, 45, 60), (120, 40, 40))
    ]

    btn_confirm_ya    = Button(SCREEN_WIDTH//2 - 130, 320, 110, 40, "YA [Y]", (140, 40, 40), (190, 50, 50))
    btn_confirm_tidak = Button(SCREEN_WIDTH//2 + 20, 320, 110, 40, "TIDAK [N]", (70, 70, 70), (100, 100, 100))

    btn_go_options = [
        Button(SCREEN_WIDTH//2 - 150, 280, 300, 40, "ULANG PERMAINAN", (40, 45, 60), (60, 70, 100)),
        Button(SCREEN_WIDTH//2 - 150, 340, 300, 40, "UBAH MODE KESULITAN", (40, 45, 60), (60, 70, 100)),
        Button(SCREEN_WIDTH//2 - 150, 400, 300, 40, "KEMBALI KE MENU", (40, 45, 60), (120, 40, 40))
    ]

    # === S4 MEMORIZE PHASE (FASE PENGINGAT) BUTTONS ===
    # Layout tombol berjarak lebar di bagian bawah layar per FASE PENGINGAT.jpg
    btn_mem_kembali = Button(SCREEN_WIDTH//2 - 200, 520, 180, 45, "[ESC] KEMBALI", (40, 45, 60), (120, 50, 50), font_size=18)
    btn_mem_lanjut  = Button(SCREEN_WIDTH//2 + 20, 520, 180, 45, "[ENTER] LANJUT", (40, 45, 60), (60, 120, 80), font_size=18)
    # ==================================================
    btn_tut_kembali   = Button(SCREEN_WIDTH//2 - 160, 480, 140, 45, "[ESC] KEMBALI", (40, 45, 60), (150, 50, 50), font_size=18)
    btn_tut_lanjut    = Button(SCREEN_WIDTH//2 + 20, 480, 140, 45, "[ENTER] LANJUT", (40, 45, 60), (60, 150, 80), font_size=18)

    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill((0, 0, 0))

    dragging_slider = None 
    input_active = None    
    input_text = ""
    rect_bgm_input = pygame.Rect(545, 192, 50, 30) 
    rect_sfx_input = pygame.Rect(545, 252, 50, 30)
    # Sistem tahan-tekan slider keyboard
    held_key_slider = None      # 'LEFT' atau 'RIGHT'
    held_key_timer  = 0         # Akumulator sebelum repeat mulai
    held_key_repeat = 0         # Akumulator antar repeat
    HELD_DELAY      = 400       # ms sebelum repeat mulai
    HELD_INTERVAL   = 80        # ms antar setiap tick repeat
    
    # Variabel Index Navigasi (Untuk Sinkronisasi Keyboard & Mouse)
    tutorial_btn_index = 1  # 0: Kembali, 1: Lanjut
    memorize_btn_index = 1  # 0: Kembali, 1: Lanjut
    # Wasit Navigasi Gameplay — 3 Kolom
    # 0: Kiri (MERAH/BIRU/KUNING/HIJAU/POP), 1: Tengah (VALIDASI), 2: Kanan (MENYERAH/JEDA)
    play_col_index = 0
    play_row_index = 0
    # Penyimpan state PLAY agar LANJUTKAN selalu kembali ke gameplay
    play_return_state = 'PLAY'
    # Akumulator waktu bermain aktif (hanya dihitung saat PLAY, bukan PAUSE/MEMORIZE)
    total_play_time_ms = 0

    is_running = True 

    while is_running:
        delta_time = clock.get_time()
        mouse_pos = pygame.mouse.get_pos() 
        
        # ==========================================
        # BGM CONTROLLER
        # ==========================================
        if manager.current_state in ['MAIN_MENU', 'SETTINGS_MENU', 'CREDIT', 'MODE_SELECT', 'TUTORIAL']:
            target_bgm_state = 'MENU'
        # Memasukkan PAUSE ke grup PLAY agar lagu horor tetap berputar saat game dijeda!
        elif manager.current_state in ['PLAY', 'MEMORIZE', 'GAME_OVER', 'PAUSE']:
            target_bgm_state = 'PLAY'
        elif manager.current_state == 'CONFIRM':
            target_bgm_state = 'SILENT' 
        else:
            target_bgm_state = 'INTRO'
            
        if current_bgm_state != target_bgm_state:
            if target_bgm_state == 'MENU':
                bgm_path = os.path.join("assets", "audio", "bgm_menu.mp3")
                if os.path.exists(bgm_path):
                    pygame.mixer.music.load(bgm_path)
                    pygame.mixer.music.set_volume(manager.volume_bgm / 100)
                    pygame.mixer.music.play(-1) 
            elif target_bgm_state == 'PLAY':
                bgm_game_path = os.path.join("assets", "audio", "bgm_game.mp3")
                if os.path.exists(bgm_game_path):
                    pygame.mixer.music.load(bgm_game_path)
                    pygame.mixer.music.set_volume(manager.volume_bgm / 100)
                    pygame.mixer.music.play(-1) 
                else:
                    pygame.mixer.music.stop() 
            elif target_bgm_state == 'SILENT':
                pygame.mixer.music.stop() 
                
            current_bgm_state = target_bgm_state
            
        if manager.current_state == 'SETTINGS_MENU':
            pygame.mixer.music.set_volume(manager.volume_bgm / 100)
        
        # ==========================================
        # VIDEO BG LOOP 
        # ==========================================
        if len(frame_files) > 0 and manager.current_state == 'MAIN_MENU':
            frame_timer += delta_time
            if frame_timer >= frame_duration:
                current_frame_index = (current_frame_index + 1) % len(frame_files)
                frame_timer = 0
            
            if current_frame_index != cached_frame_idx:
                try:
                    raw_img = pygame.image.load(os.path.join(video_frames_dir, frame_files[current_frame_index])).convert()
                    cached_frame_img = pygame.transform.scale(raw_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                    cached_frame_idx = current_frame_index
                except pygame.error: pass

        # ==========================================
        # HOVER SINKRONISASI UPDATE + SFX TRIGGER
        # ==========================================
        active_buttons = []
        if manager.current_state == 'MAIN_MENU': active_buttons = btn_menu_options
        elif manager.current_state == 'SETTINGS_MENU': active_buttons = [btn_bgm_slider, btn_sfx_slider, btn_fs_toggle, btn_settings_kembali]
        elif manager.current_state == 'CREDIT': active_buttons = [btn_credit_kembali]
        elif manager.current_state == 'MODE_SELECT': active_buttons = list(btn_modes.values()) + [btn_mode_kembali]
        elif manager.current_state == 'TUTORIAL': active_buttons = [btn_tut_kembali, btn_tut_lanjut]
        elif manager.current_state == 'MEMORIZE': active_buttons = [btn_mem_lanjut, btn_mem_kembali] # Incision!
        elif manager.current_state == 'PLAY': active_buttons = [btn_game_merah, btn_game_biru, btn_game_kuning, btn_game_hijau, btn_game_pop, btn_game_validate, btn_game_menyerah, btn_game_jeda]
        elif manager.current_state == 'CONFIRM': active_buttons = [btn_confirm_ya, btn_confirm_tidak]
        elif manager.current_state == 'GAME_OVER': active_buttons = btn_go_options
        elif manager.current_state == 'PAUSE': active_buttons = btn_pause_options

        for btn in active_buttons:
            was_hovered = btn.is_hovered
            btn.update(mouse_pos)
            if not was_hovered and btn.is_hovered:
                play_hover()

        old_menu, old_set, old_mode, old_conf, old_go = manager.menu_index, manager.settings_index, manager.mode_index, manager.confirm_index, manager.game_over_index
        
        if manager.current_state == 'MAIN_MENU':
            for idx, btn in enumerate(btn_menu_options):
                if btn.is_hovered: manager.menu_index = idx  
        elif manager.current_state == 'SETTINGS_MENU':
            for idx, btn in enumerate([btn_bgm_slider, btn_sfx_slider, btn_fs_toggle, btn_settings_kembali]):
                if btn.is_hovered: manager.settings_index = idx
        elif manager.current_state == 'MODE_SELECT':
            for idx, btn in enumerate(list(btn_modes.values())):
                if btn.is_hovered: manager.mode_index = idx
            if btn_mode_kembali.is_hovered: manager.mode_index = len(manager.modes_list)
        # --- SINKRONISASI INDEX MOUSE KONSISTEN ---
        elif manager.current_state == 'TUTORIAL':
            for idx, btn in enumerate([btn_tut_kembali, btn_tut_lanjut]):
                if btn.is_hovered: tutorial_btn_index = idx
        elif manager.current_state == 'MEMORIZE':
            for idx, btn in enumerate([btn_mem_kembali, btn_mem_lanjut]):
                if btn.is_hovered: memorize_btn_index = idx
        # --- SUNTIKAN v2.1.3: SYNC MOUSE GAMEPLAY 3 KOLOM DINAMIS ---
        elif manager.current_state == 'PLAY':
            # Kolom 0 (Kiri): Warna + POP
            for idx, btn in enumerate([btn_game_merah, btn_game_biru, btn_game_kuning, btn_game_hijau, btn_game_pop]):
                if btn.is_hovered: play_col_index = 0; play_row_index = idx
            # Kolom 1 (Tengah): Validasi
            if btn_game_validate.is_hovered: play_col_index = 1; play_row_index = 0
            # Kolom 2 (Kanan): Menyerah, Jeda
            for idx, btn in enumerate([btn_game_menyerah, btn_game_jeda]):
                if btn.is_hovered: play_col_index = 2; play_row_index = idx
        # ------------------------------------------
        elif manager.current_state == 'CONFIRM':
            if btn_confirm_ya.is_hovered: manager.confirm_index = 0
            elif btn_confirm_tidak.is_hovered: manager.confirm_index = 1
        elif manager.current_state == 'GAME_OVER':
            for idx, btn in enumerate(btn_go_options):
                if btn.is_hovered: manager.game_over_index = idx 
        elif manager.current_state == 'PAUSE':
            for idx, btn in enumerate(btn_pause_options):
                if btn.is_hovered: manager.pause_index = idx
        elif manager.current_state == 'PLAY':
            for idx, btn in enumerate([btn_game_merah, btn_game_biru, btn_game_kuning, btn_game_hijau, btn_game_pop]):
                if btn.is_hovered: play_col_index = 0; play_row_index = idx
            if btn_game_validate.is_hovered: play_col_index = 1; play_row_index = 0
            for idx, btn in enumerate([btn_game_menyerah, btn_game_jeda]):
                if btn.is_hovered: play_col_index = 2; play_row_index = idx

        # ==========================================
        # EVENT HANDLING (INPUT GANDA + SLIDER & TYPING v1.2.5)
        # ==========================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                
            # --- EVENT: TETIKUS DITEKAN TAHAN ---
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if manager.current_state in ['INTRO_STUDIO', 'INTRO_PRODUCER', 'INTRO_DISCLAIMER']:
                    manager.skip_intro()
                    
                elif manager.current_state == 'MAIN_MENU':
                    clicked = False
                    if btn_menu_options[0].is_clicked(event, mouse_pos): manager.current_state = 'MODE_SELECT'; clicked = True
                    elif btn_menu_options[1].is_clicked(event, mouse_pos): manager.previous_state = manager.current_state; manager.current_state = 'SETTINGS_MENU'; clicked = True
                    elif btn_menu_options[2].is_clicked(event, mouse_pos): manager.current_state = 'CREDIT'; clicked = True
                    elif btn_menu_options[3].is_clicked(event, mouse_pos): manager.trigger_confirm('KELUAR?'); clicked = True
                    if clicked: play_click()
                    
                elif manager.current_state == 'SETTINGS_MENU':
                    clicked = True
                    # Logika Fokus Ketik Angka
                    if rect_bgm_input.collidepoint(mouse_pos):
                        input_active = 'BGM'
                        input_text = str(manager.volume_bgm)
                    elif rect_sfx_input.collidepoint(mouse_pos):
                        input_active = 'SFX'
                        input_text = str(manager.volume_sfx)
                    else:
                        # Jika klik di luar kotak, simpan nilai yang sudah diketik
                        if input_active:
                            if input_active == 'BGM': manager.volume_bgm = max(0, min(100, int(input_text) if input_text else 0))
                            elif input_active == 'SFX': manager.volume_sfx = max(0, min(100, int(input_text) if input_text else 0))
                            input_active = None

                        # Logika Tarik Slider Mouse Down
                        if btn_bgm_slider.rect.collidepoint(mouse_pos):
                            dragging_slider = 'BGM'
                            rel_x = mouse_pos[0] - btn_bgm_slider.rect.x
                            manager.volume_bgm = max(0, min(100, int((rel_x / btn_bgm_slider.rect.width) * 100)))
                        elif btn_sfx_slider.rect.collidepoint(mouse_pos):
                            dragging_slider = 'SFX'
                            rel_x = mouse_pos[0] - btn_sfx_slider.rect.x
                            manager.volume_sfx = max(0, min(100, int((rel_x / btn_sfx_slider.rect.width) * 100)))
                        elif btn_fs_toggle.is_clicked(event, mouse_pos):
                            manager.is_fullscreen = not manager.is_fullscreen
                            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), (pygame.FULLSCREEN | pygame.SCALED) if manager.is_fullscreen else pygame.SCALED)
                        elif btn_settings_kembali.is_clicked(event, mouse_pos): manager.current_state = manager.previous_state
                        else: clicked = False
                    if clicked: play_click()
                    
                elif manager.current_state == 'CREDIT':
                    if btn_credit_kembali.is_clicked(event, mouse_pos): manager.current_state = 'MAIN_MENU'; play_click()
                    
                elif manager.current_state == 'MODE_SELECT':
                    clicked = False
                    if btn_mode_kembali.is_clicked(event, mouse_pos): manager.current_state = 'MAIN_MENU'; clicked = True
                    for mode_name, btn in btn_modes.items():
                        if btn.is_clicked(event, mouse_pos) and not manager.get_lock_status(mode_name):
                            manager.selected_mode = mode_name
                            manager.generate_new_level()
                            player_stack.target_blueprint = manager.target_blueprint
                            player_stack.clear_stack() 
                            manager.current_state = 'TUTORIAL'
                            manager.tutorial_step = 0
                            clicked = True
                    if clicked: play_click()
                            
                elif manager.current_state == 'TUTORIAL':
                    clicked = False
                    if btn_tut_kembali.is_clicked(event, mouse_pos): 
                        manager.current_state = 'MODE_SELECT'
                        clicked = True
                    elif btn_tut_lanjut.is_clicked(event, mouse_pos): 
                        # Lempar ke Layar Loading terlebih dahulu!
                        manager.current_state = 'LOADING'
                        loading_timer = 0
                        current_hint = random.choice([
                            "PETUNJUK: Suara kecil sering lebih menyeramkan dari suara keras.", 
                            "PETUNJUK: Balok terakhir masuk adalah yang pertama keluar (LIFO).", 
                            "PETUNJUK: Jangan biarkan monster menembus batas kewarasanmu."
                        ])
                        clicked = True
                    if clicked: play_click()
                    
                # === S4 MEMORIZE CLICKS (MOUSE) ===
                elif manager.current_state == 'MEMORIZE':
                    clicked = False
                    if btn_mem_kembali.is_clicked(event, mouse_pos): 
                        # ESCituharus Kembali pada bagian PEMILIHAN MODE per user prompt
                        manager.current_state = 'MODE_SELECT'
                        clicked = True
                    elif btn_mem_lanjut.is_clicked(event, mouse_pos):
                        # Tombol speedrun: Masuk gameplay tanpa menunggu waktu habis
                        manager.current_state = 'PLAY'
                        # manager.generate_new_level() -> HAPUS INI JIKA ADA! Gunakan level yang sudah di-generate tutorial/intro
                        manager.state_timer = manager.play_duration # Reset timer untuk fase gameplay
                        manager.indicator_light = True
                        clicked = True
                    if clicked: play_click()    
                    
                elif manager.current_state == 'PLAY':
                    if btn_game_merah.is_clicked(event, mouse_pos):     player_stack.push("Merah"); play_push()
                    elif btn_game_biru.is_clicked(event, mouse_pos):    player_stack.push("Biru"); play_push()
                    elif btn_game_kuning.is_clicked(event, mouse_pos):  player_stack.push("Kuning"); play_push()
                    elif btn_game_hijau.is_clicked(event, mouse_pos):   player_stack.push("Hijau"); play_push()
                    elif btn_game_pop.is_clicked(event, mouse_pos):     player_stack.pop(); play_pop()
                    elif btn_game_menyerah.is_clicked(event, mouse_pos): manager.trigger_confirm('MENYERAH'); play_click()
                    elif btn_game_jeda.is_clicked(event, mouse_pos):     play_return_state = 'PLAY'; manager.previous_state = manager.current_state; manager.current_state = 'PAUSE'; play_click()
                    elif btn_game_validate.is_clicked(event, mouse_pos):
                        player_stack.target_blueprint = manager.target_blueprint
                        if player_stack.check_match():
                            manager.handle_success()
                            player_stack.clear_stack()
                            play_success()  
                        else:
                            manager.trigger_inner_monologue()
                            play_error()    
                            
                elif manager.current_state == 'CONFIRM':
                    clicked = True
                    if btn_confirm_ya.is_clicked(event, mouse_pos):
                        if manager.confirm_type == 'MENYERAH': 
                            manager.trigger_game_over()
                        elif manager.confirm_type == 'KELUAR MENU?':
                            manager.reset_to_menu()
                            player_stack.clear_stack()
                            total_play_time_ms = 0 
                        elif manager.confirm_type == 'KELUAR?': 
                            is_running = False
                    elif btn_confirm_tidak.is_clicked(event, mouse_pos): manager.cancel_confirm()
                    else: clicked = False
                    if clicked: play_click()
                            
                elif manager.current_state == 'GAME_OVER':
                    clicked = True
                    if btn_go_options[0].is_clicked(event, mouse_pos):   
                        manager.restart_level()
                        player_stack.clear_stack()
                        total_play_time_ms = 0 
                    elif btn_go_options[1].is_clicked(event, mouse_pos): 
                        manager.current_state = 'MODE_SELECT'
                        player_stack.clear_stack() 
                    elif btn_go_options[2].is_clicked(event, mouse_pos): 
                        manager.reset_to_menu()
                        player_stack.clear_stack() 
                    else: clicked = False
                    if clicked: play_click()
                    
                elif manager.current_state == 'PAUSE':
                    clicked = True
                    if btn_pause_options[0].is_clicked(event, mouse_pos): manager.current_state = play_return_state
                    elif btn_pause_options[1].is_clicked(event, mouse_pos): manager.restart_level(); player_stack.clear_stack(); total_play_time_ms = 0
                    elif btn_pause_options[2].is_clicked(event, mouse_pos): manager.previous_state = 'PAUSE'; manager.current_state = 'SETTINGS_MENU'
                    elif btn_pause_options[3].is_clicked(event, mouse_pos): manager.trigger_confirm('KELUAR MENU?')
                    else: clicked = False
                    if clicked: play_click()

            # --- EVENT: TETIKUS DILEPAS (STOP DRAGGING) ---
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging_slider = None

            # --- EVENT: TETIKUS BERGESER (DRAGGING FLUIDA) ---
            elif event.type == pygame.MOUSEMOTION:
                if manager.current_state == 'SETTINGS_MENU':
                    if dragging_slider == 'BGM':
                        rel_x = mouse_pos[0] - btn_bgm_slider.rect.x
                        manager.volume_bgm = max(0, min(100, int((rel_x / btn_bgm_slider.rect.width) * 100)))
                    elif dragging_slider == 'SFX':
                        rel_x = mouse_pos[0] - btn_sfx_slider.rect.x
                        manager.volume_sfx = max(0, min(100, int((rel_x / btn_sfx_slider.rect.width) * 100)))

            # --- EVENT: TOMBOL DILEPAS (STOP TAHAN-TEKAN SLIDER) ---
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    held_key_slider = None
                    held_key_timer  = 0
                    held_key_repeat = 0

            # --- INPUT KENDALI KEYBOARD ---
            elif event.type == pygame.KEYDOWN:
                if manager.current_state in ['INTRO_STUDIO', 'INTRO_PRODUCER', 'INTRO_DISCLAIMER']:
                    if event.key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE]: manager.skip_intro()
                
                elif manager.current_state == 'MAIN_MENU':
                    if event.key == pygame.K_ESCAPE: manager.trigger_confirm('KELUAR?'); play_click()
                    elif event.key == pygame.K_DOWN:   manager.menu_index = (manager.menu_index + 1) % len(manager.menu_options); play_hover()
                    elif event.key == pygame.K_UP:   manager.menu_index = (manager.menu_index - 1) % len(manager.menu_options); play_hover()
                    elif event.key == pygame.K_RETURN:
                        play_click()
                        if manager.menu_index == 0:   manager.current_state = 'MODE_SELECT'
                        elif manager.menu_index == 1: manager.previous_state = manager.current_state; manager.current_state = 'SETTINGS_MENU'
                        elif manager.menu_index == 2: manager.current_state = 'CREDIT'
                        elif manager.menu_index == 3: manager.trigger_confirm('KELUAR?')
                
                elif manager.current_state == 'SETTINGS_MENU':
                    # Logika Pemrosesan Angka Input Langsung
                    if input_active:
                        if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                            play_click()
                            if input_active == 'BGM': manager.volume_bgm = max(0, min(100, int(input_text) if input_text else 0))
                            elif input_active == 'SFX': manager.volume_sfx = max(0, min(100, int(input_text) if input_text else 0))
                            input_active = None
                        elif event.key == pygame.K_BACKSPACE:
                            input_text = input_text[:-1]
                            play_click()
                        elif event.unicode.isdigit():
                            if len(input_text) < 3 or (len(input_text) == 3 and input_text == "100"): 
                                input_text += event.unicode
                                play_click()
                    else:
                        # Logika Keyboard Normal
                        if event.key == pygame.K_ESCAPE: play_click(); manager.current_state = 'MAIN_MENU'
                        elif event.key == pygame.K_DOWN:   manager.settings_index = (manager.settings_index + 1) % len(manager.settings_options); play_hover()
                        elif event.key == pygame.K_UP:   manager.settings_index = (manager.settings_index - 1) % len(manager.settings_options); play_hover()
                        elif event.key == pygame.K_RIGHT:
                            if manager.settings_index in [0, 1]:
                                held_key_slider = 'RIGHT'
                                held_key_timer  = 0
                                held_key_repeat = 0
                                if manager.settings_index == 0: manager.volume_bgm = min(100, manager.volume_bgm + 5)
                                elif manager.settings_index == 1: manager.volume_sfx = min(100, manager.volume_sfx + 5)
                                play_click()
                            elif manager.settings_index == 2:
                                manager.is_fullscreen = True
                                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
                                play_click()
                        elif event.key == pygame.K_LEFT:
                            if manager.settings_index in [0, 1]:
                                held_key_slider = 'LEFT'
                                held_key_timer  = 0
                                held_key_repeat = 0
                                if manager.settings_index == 0: manager.volume_bgm = max(0, manager.volume_bgm - 5)
                                elif manager.settings_index == 1: manager.volume_sfx = max(0, manager.volume_sfx - 5)
                                play_click()
                            elif manager.settings_index == 2:
                                manager.is_fullscreen = False
                                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED)
                                play_click()
                        elif event.key == pygame.K_RETURN:
                            play_click()
                            if manager.settings_index == 2:
                                manager.is_fullscreen = not manager.is_fullscreen
                                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED) if manager.is_fullscreen else pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED)
                            elif manager.settings_index == 3: manager.current_state = manager.previous_state
                
                elif manager.current_state in ['CREDIT']:
                    if event.key in [pygame.K_RETURN, pygame.K_ESCAPE]: play_click(); manager.current_state = 'MAIN_MENU'
                
                elif manager.current_state == 'TUTORIAL':
                    # Logika Panah Kiri dan Kanan Terpusat
                    if event.key == pygame.K_LEFT: tutorial_btn_index = 0; play_hover()
                    elif event.key == pygame.K_RIGHT: tutorial_btn_index = 1; play_hover()
                    # Eksekusi tombol berdasarkan tombol mana yang sedang 'Stand Out'
                    elif event.key == pygame.K_ESCAPE or (event.key == pygame.K_RETURN and tutorial_btn_index == 0): 
                        play_click()
                        manager.current_state = 'MODE_SELECT'
                    elif event.key in [pygame.K_RETURN, pygame.K_SPACE] and tutorial_btn_index == 1: 
                        play_click()
                        manager.current_state = 'LOADING'
                        loading_timer = 0
                        current_hint = random.choice([
                            "PETUNJUK: Suara kecil sering lebih menyeramkan dari suara keras.", 
                            "PETUNJUK: Balok terakhir masuk adalah yang pertama keluar (LIFO).", 
                            "PETUNJUK: Jangan biarkan monster menembus batas kewarasanmu."
                        ])
                
                elif manager.current_state == 'MODE_SELECT':
                    if event.key == pygame.K_ESCAPE: play_click(); manager.current_state = 'MAIN_MENU'
                    elif event.key == pygame.K_DOWN:   manager.mode_index = (manager.mode_index + 1) % (len(manager.modes_list) + 1); play_hover()
                    elif event.key == pygame.K_UP:   manager.mode_index = (manager.mode_index - 1) % (len(manager.modes_list) + 1); play_hover()
                    elif event.key == pygame.K_RETURN:
                        play_click()
                        if manager.mode_index == len(manager.modes_list): manager.current_state = 'MAIN_MENU'
                        else:
                            target_mode = manager.modes_list[manager.mode_index]
                            if not manager.get_lock_status(target_mode):
                                manager.selected_mode = target_mode
                                manager.generate_new_level()
                                player_stack.target_blueprint = manager.target_blueprint
                                player_stack.clear_stack() 
                                manager.current_state = 'TUTORIAL'
                                manager.tutorial_step = 0
                                
                elif manager.current_state == 'MEMORIZE':
                    # Logika Kiri Kanan Terpusat
                    if event.key == pygame.K_LEFT: memorize_btn_index = 0; play_hover()
                    elif event.key == pygame.K_RIGHT: memorize_btn_index = 1; play_hover()
                    elif event.key == pygame.K_ESCAPE or (event.key == pygame.K_RETURN and memorize_btn_index == 0): 
                        manager.current_state = 'MODE_SELECT'
                        play_click()
                    elif event.key in [pygame.K_RETURN, pygame.K_SPACE] and memorize_btn_index == 1:
                        manager.current_state = 'PLAY'
                        manager.state_timer = manager.play_duration 
                        manager.indicator_light = True
                        play_click()
                
                # --- RENOVASI v2.1.3: LOGIKA NAVIGASI GAMEPLAY ---
                elif manager.current_state == 'PLAY':
                    # Shortcut Murni (Tetap aktif)
                    if event.key == pygame.K_ESCAPE: play_return_state = 'PLAY'; manager.previous_state = manager.current_state; manager.current_state = 'PAUSE'; play_click()
                    elif event.key == pygame.K_r: player_stack.push("Merah"); play_push()
                    elif event.key == pygame.K_b: player_stack.push("Biru"); play_push()
                    elif event.key == pygame.K_y: player_stack.push("Kuning"); play_push()
                    elif event.key == pygame.K_g: player_stack.push("Hijau"); play_push()
                    elif event.key == pygame.K_BACKSPACE: player_stack.pop(); play_pop()
                    elif event.key == pygame.K_m: manager.trigger_confirm('MENYERAH'); play_click()
                    elif event.key == pygame.K_q: manager.trigger_confirm('KELUAR MENU?'); play_click()
                    
                  # --- LOGIKA NAVIGASI GRID 3 KOLOM ---
                    # Kiri(0): MERAH/BIRU/KUNING/HIJAU/POP  Tengah(1): VALIDASI  Kanan(2): MENYERAH/JEDA
                    elif event.key == pygame.K_LEFT:
                        if play_col_index > 0:
                            play_col_index -= 1
                            # Saat kembali ke kiri, row tetap (clamp agar tidak out of range)
                            if play_col_index == 0: play_row_index = min(play_row_index, 4)
                            elif play_col_index == 1: play_row_index = 0  # Tengah hanya 1 tombol
                        play_hover()
                    elif event.key == pygame.K_RIGHT:
                        if play_col_index < 2:
                            play_col_index += 1
                            # Saat pindah kolom, reset row ke 0 agar selalu valid
                            if play_col_index == 1: play_row_index = 0  # Tengah hanya 1 tombol
                            elif play_col_index == 2: play_row_index = 0
                        play_hover()
                    elif event.key == pygame.K_UP:
                        if play_col_index == 0: play_row_index = (play_row_index - 1) % 5
                        elif play_col_index == 1: play_row_index = 0  # Tengah tetap di 0
                        elif play_col_index == 2: play_row_index = (play_row_index - 1) % 2
                        play_hover()
                    elif event.key == pygame.K_DOWN:
                        if play_col_index == 0: play_row_index = (play_row_index + 1) % 5
                        elif play_col_index == 1: play_row_index = 0  # Tengah tetap di 0
                        elif play_col_index == 2: play_row_index = (play_row_index + 1) % 2
                        play_hover()

                    elif event.key == pygame.K_RETURN:
                        if play_col_index == 0:  # Eksekusi Kolom Kiri
                            if play_row_index == 0: player_stack.push("Merah"); play_push()
                            elif play_row_index == 1: player_stack.push("Biru"); play_push()
                            elif play_row_index == 2: player_stack.push("Kuning"); play_push()
                            elif play_row_index == 3: player_stack.push("Hijau"); play_push()
                            elif play_row_index == 4: player_stack.pop(); play_pop()
                        elif play_col_index == 1:  # Eksekusi Kolom Tengah
                            player_stack.target_blueprint = manager.target_blueprint
                            if player_stack.check_match(): manager.handle_success(); player_stack.clear_stack(); play_success()
                            else: manager.trigger_inner_monologue(); play_error()
                        elif play_col_index == 2:  # Eksekusi Kolom Kanan
                            if play_row_index == 0: manager.trigger_confirm('MENYERAH'); play_click()
                            elif play_row_index == 1: play_return_state = 'PLAY'; manager.previous_state = manager.current_state; manager.current_state = 'PAUSE'; play_click()
                
                elif manager.current_state == 'CONFIRM':
                    if event.key == pygame.K_ESCAPE: play_click(); manager.cancel_confirm()
                    elif event.key == pygame.K_LEFT: manager.confirm_index = 0; play_hover()
                    elif event.key == pygame.K_RIGHT: manager.confirm_index = 1; play_hover()
                    elif event.key == pygame.K_y or (event.key == pygame.K_RETURN and manager.confirm_index == 0):
                        play_click()
                        if manager.confirm_type == 'MENYERAH': 
                            manager.trigger_game_over()
                        elif manager.confirm_type == 'KELUAR MENU?':
                            manager.reset_to_menu()
                            player_stack.clear_stack() 
                        elif manager.confirm_type == 'KELUAR?': 
                            is_running = False
                    elif event.key == pygame.K_n or (event.key == pygame.K_RETURN and manager.confirm_index == 1):
                        play_click(); manager.cancel_confirm()
                
                elif manager.current_state == 'GAME_OVER':
                    if event.key == pygame.K_DOWN:   manager.game_over_index = (manager.game_over_index + 1) % len(manager.game_over_options); play_hover()
                    elif event.key == pygame.K_UP:   manager.game_over_index = (manager.game_over_index - 1) % len(manager.game_over_options); play_hover()
                    elif event.key == pygame.K_RETURN:
                        play_click()
                        if manager.game_over_index == 0:   
                            manager.restart_level()
                            player_stack.clear_stack()
                            total_play_time_ms = 0 
                        elif manager.game_over_index == 1: 
                            manager.current_state = 'MODE_SELECT'
                            player_stack.clear_stack() 
                        elif manager.game_over_index == 2: 
                            manager.reset_to_menu()
                            player_stack.clear_stack()
                            
               # --- LOGIKA KEYBOARD LAYAR JEDA ---
                elif manager.current_state == 'PAUSE':
                    if event.key == pygame.K_ESCAPE: play_click(); manager.current_state = play_return_state
                    elif event.key == pygame.K_DOWN: manager.pause_index = (manager.pause_index + 1) % len(manager.pause_options); play_hover()
                    elif event.key == pygame.K_UP: manager.pause_index = (manager.pause_index - 1) % len(manager.pause_options); play_hover()
                    elif event.key == pygame.K_RETURN:
                        play_click()
                        if manager.pause_index == 0: manager.current_state = play_return_state
                        elif manager.pause_index == 1: manager.restart_level(); player_stack.clear_stack(); total_play_time_ms = 0
                        elif manager.pause_index == 2: manager.previous_state = 'PAUSE'; manager.current_state = 'SETTINGS_MENU'
                        elif manager.pause_index == 3: manager.trigger_confirm('KELUAR MENU?') 

        # ---- LOGIKA TAHAN-TEKAN SLIDER KEYBOARD ----
        if held_key_slider and manager.current_state == 'SETTINGS_MENU' and not input_active:
            if manager.settings_index in [0, 1]:
                held_key_timer += delta_time
                if held_key_timer >= HELD_DELAY:
                    held_key_repeat += delta_time
                    if held_key_repeat >= HELD_INTERVAL:
                        held_key_repeat = 0
                        if held_key_slider == 'RIGHT':
                            if manager.settings_index == 0: manager.volume_bgm = min(100, manager.volume_bgm + 1)
                            elif manager.settings_index == 1: manager.volume_sfx = min(100, manager.volume_sfx + 1)
                        elif held_key_slider == 'LEFT':
                            if manager.settings_index == 0: manager.volume_bgm = max(0, manager.volume_bgm - 1)
                            elif manager.settings_index == 1: manager.volume_sfx = max(0, manager.volume_sfx - 1)
            else:
                # Bukan slider (misal index 2 fullscreen), langsung reset agar tidak mengulang
                held_key_slider = None
        
        # ---- 3. LOGIKA UPDATE ----
        # Cegat logika waktu GameManager dan buat simulasi pemuatan memori 3 Detik!
        if manager.current_state == 'LOADING':
            loading_timer += delta_time
            if loading_timer >= 3000: # 3000 milidetik = 3 Detik Loading
                manager.current_state = 'MEMORIZE'
                loading_timer = 0
        else:
            manager.update_timer(delta_time)

        # Akumulasi waktu aktif — berhenti saat PAUSE/JEDA
        if manager.current_state == 'PLAY':
            total_play_time_ms += delta_time

        if manager.current_state == 'PLAY':
            monster.update(manager.state_timer, manager.play_duration)
        elif manager.current_state == 'MEMORIZE':
            monster.current_x = monster.start_x

        # ---- 4. RENDER VISUAL (FIX ISOLASI BACKGROUND) ----
        if manager.current_state in ['INTRO_STUDIO', 'INTRO_PRODUCER', 'INTRO_DISCLAIMER']:
            screen.fill((0, 0, 0)) 
        elif manager.current_state == 'MAIN_MENU':
            if cached_frame_img: screen.blit(cached_frame_img, (0, 0))
            else: screen.fill(COLOR_BG_SAFE) 
        elif manager.current_state == 'MODE_SELECT':
            if mode_bg_image: screen.blit(mode_bg_image, (0, 0))
            else: screen.fill(COLOR_BG_SAFE)
        elif manager.current_state == 'SETTINGS_MENU':
            if settings_bg_image: screen.blit(settings_bg_image, (0, 0))
            else: screen.fill(COLOR_BG_SAFE)
        elif manager.current_state == 'TUTORIAL':
            if tutorial_bg_image:
                screen.blit(tutorial_bg_image, (0, 0))
            elif mode_bg_image: # Fallback pakai bg mode jika bg tutorial kosong
                screen.blit(mode_bg_image, (0, 0))
            else:
                screen.fill(COLOR_BG_SAFE)
        elif manager.current_state == 'LOADING':
            # Ambil sisa background dari tutorial atau mode agar transisinya mulus
            if tutorial_bg_image: screen.blit(tutorial_bg_image, (0, 0))
            elif mode_bg_image: screen.blit(mode_bg_image, (0, 0))
            else: screen.fill(COLOR_BG_SAFE)
            
        elif manager.current_state == 'CREDIT':
            # Jika Anda nanti punya file credit_bg.png, bisa dimasukkan ke pipeline seperti mode_bg
            # Untuk sekarang kita set Fallback murni
            if mode_bg_image: screen.blit(mode_bg_image, (0, 0)) # Fallback sementara pakai BG Mode
            else: screen.fill(COLOR_BG_SAFE)
        # === S3: BACKGROUND MODE SPESIFIK SAAT GAMEPLAY ===
        elif manager.current_state in ['PLAY', 'PAUSE', 'GAME_OVER']:
            # Panggil gambar spesifik berdasarkan mode yang sedang aktif
            mode_img = bg_modes_images.get(manager.selected_mode)
            if mode_img: screen.blit(mode_img, (0, 0))
            else: screen.fill(COLOR_BG_SAFE)
            
            # Tetap pertahankan aura horor merah berkedip saat waktu kritis!
            if manager.state_timer < 15000:
                danger_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                danger_surf.fill((150, 0, 0, 80)) # Transparan merah darah
                screen.blit(danger_surf, (0,0))
        else:
            screen.fill(COLOR_BG_SAFE)
        
        if manager.current_state == 'INTRO_STUDIO':
            if studio_logo_image:
                logo_rect = studio_logo_image.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
                screen.blit(studio_logo_image, logo_rect)
            else:
                txt_studio_title = font_title.render("Aureum V Studios", True, COLOR_RED)
                txt_studio_sub = font_menu.render("[ Logo Image Placeholder ]", True, COLOR_WHITE)
                screen.blit(txt_studio_title, (SCREEN_WIDTH//2 - txt_studio_title.get_width()//2, SCREEN_HEIGHT//2 - 40))
                screen.blit(txt_studio_sub, (SCREEN_WIDTH//2 - txt_studio_sub.get_width()//2, SCREEN_HEIGHT//2 + 20))

        elif manager.current_state == 'INTRO_PRODUCER':
            txt_prod_1 = font_menu.render("Produced by", True, (150, 150, 150))
            txt_prod_2 = font_menu.render("Universitas Bina Sarana Informatika Pontianak", True, COLOR_WHITE)
            screen.blit(txt_prod_1, (SCREEN_WIDTH//2 - txt_prod_1.get_width()//2, SCREEN_HEIGHT//2 - 80))
            screen.blit(txt_prod_2, (SCREEN_WIDTH//2 - txt_prod_2.get_width()//2, SCREEN_HEIGHT//2 - 30))
            if ubsi_logo_image:
                ubsi_rect = ubsi_logo_image.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 70))
                screen.blit(ubsi_logo_image, ubsi_rect)
            else:
                pygame.draw.rect(screen, COLOR_BLUE, (SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT//2 + 20, 100, 100), 2)
                txt_logo_placeholder = font_tut.render("[ LOGO UBSI ]", True, COLOR_BLUE)
                screen.blit(txt_logo_placeholder, (SCREEN_WIDTH//2 - txt_logo_placeholder.get_width()//2, SCREEN_HEIGHT//2 + 60))

        elif manager.current_state == 'INTRO_DISCLAIMER':
            for i, line in enumerate(manager.disclaimer_messages):
                color = COLOR_RED if "PERINGATAN" in line else COLOR_WHITE
                txt_disc = font_tut.render(line, True, color)
                screen.blit(txt_disc, (SCREEN_WIDTH//2 - txt_disc.get_width()//2, 120 + (i * 32)))

        elif manager.current_state == 'MAIN_MENU':
            if menu_logo_image:
                screen.blit(menu_logo_image, (440, 60))
            else:
                title_text = font_title.render("angSSatan v2.1.3", True, COLOR_RED)
                screen.blit(title_text, (480, 100))
                
            for idx, btn in enumerate(btn_menu_options):
                if idx == manager.menu_index: btn.current_color = (60, 70, 100)
                btn.draw(screen)

            version_text = font_tut.render("angSSatan v2.1.3", True, (130, 130, 140))
            version_x = SCREEN_WIDTH - version_text.get_width() - 15
            version_y = SCREEN_HEIGHT - version_text.get_height() - 15
            screen.blit(version_text, (version_x, version_y))

        elif manager.current_state == 'SETTINGS_MENU':
            panel_x, panel_y, panel_w, panel_h = 150, 100, 500, 400
            pygame.draw.rect(screen, (40, 45, 60), (panel_x, panel_y, panel_w, panel_h))
            pygame.draw.rect(screen, COLOR_WHITE, (panel_x, panel_y, panel_w, panel_h), 2)
            pygame.draw.rect(screen, (20, 20, 30), (panel_x+5, panel_y+5, panel_w, panel_h), 2) 

            title_set = font_title.render("PENGATURAN", True, COLOR_YELLOW)
            screen.blit(title_set, (SCREEN_WIDTH//2 - title_set.get_width()//2, panel_y + 20))

            # --- BARIS 1: BGM SLIDER ---
            bgm_txt = font_menu.render("BGM VOLUME", True, COLOR_WHITE)
            screen.blit(bgm_txt, (panel_x + 40, 195))
            
            track_bgm = btn_bgm_slider.rect
            pygame.draw.rect(screen, (60, 60, 70), track_bgm) 
            fill_w_bgm = int((manager.volume_bgm / 100) * track_bgm.width)
            pygame.draw.rect(screen, (220, 80, 80), (track_bgm.x, track_bgm.y, fill_w_bgm, track_bgm.height)) 
            pygame.draw.rect(screen, COLOR_WHITE, (track_bgm.x + fill_w_bgm - 5, track_bgm.y - 2, 10, track_bgm.height + 4)) 
            
            if manager.settings_index == 0:
                pygame.draw.rect(screen, COLOR_RED, (track_bgm.x - 2, track_bgm.y - 2, track_bgm.width + 4, track_bgm.height + 4), 2)

            if input_active == 'BGM':
                pygame.draw.rect(screen, (80, 80, 80), rect_bgm_input)
                pygame.draw.rect(screen, COLOR_YELLOW, rect_bgm_input, 1)
                bgm_pct_surf = font_small.render(f"{input_text}_", True, COLOR_YELLOW)
            else:
                bgm_pct_surf = font_small.render(f"{manager.volume_bgm}%", True, COLOR_WHITE)
            screen.blit(bgm_pct_surf, (rect_bgm_input.x + 8, rect_bgm_input.y + 6))

            # --- BARIS 2: SFX SLIDER ---
            sfx_txt = font_menu.render("SFX VOLUME", True, COLOR_WHITE)
            screen.blit(sfx_txt, (panel_x + 40, 255))

            track_sfx = btn_sfx_slider.rect
            pygame.draw.rect(screen, (60, 60, 70), track_sfx) 
            fill_w_sfx = int((manager.volume_sfx / 100) * track_sfx.width)
            pygame.draw.rect(screen, (220, 80, 80), (track_sfx.x, track_sfx.y, fill_w_sfx, track_sfx.height)) 
            pygame.draw.rect(screen, COLOR_WHITE, (track_sfx.x + fill_w_sfx - 5, track_sfx.y - 2, 10, track_sfx.height + 4)) 
            
            if manager.settings_index == 1:
                pygame.draw.rect(screen, COLOR_RED, (track_sfx.x - 2, track_sfx.y - 2, track_sfx.width + 4, track_sfx.height + 4), 2)

            if input_active == 'SFX':
                pygame.draw.rect(screen, (80, 80, 80), rect_sfx_input)
                pygame.draw.rect(screen, COLOR_YELLOW, rect_sfx_input, 1)
                sfx_pct_surf = font_small.render(f"{input_text}_", True, COLOR_YELLOW)
            else:
                sfx_pct_surf = font_small.render(f"{manager.volume_sfx}%", True, COLOR_WHITE)
            screen.blit(sfx_pct_surf, (rect_sfx_input.x + 8, rect_sfx_input.y + 6))

            # --- BARIS 3: FULLSCREEN TOGGLE (RENOVASI v2.1.0) ---
            fs_txt = font_menu.render("FULLSCREEN", True, COLOR_WHITE)
            screen.blit(fs_txt, (panel_x + 40, 315))
            
            # Logika pewarnaan saat tombol di-hover (pakai mouse atau panah keyboard)
            if manager.settings_index == 2:
                btn_fs_toggle.current_color = (60, 70, 100)
                pygame.draw.rect(screen, COLOR_RED, (btn_fs_toggle.rect.x - 2, btn_fs_toggle.rect.y - 2, btn_fs_toggle.rect.width + 4, btn_fs_toggle.rect.height + 4), 2)
            else:
                btn_fs_toggle.current_color = (40, 45, 60)
            
            # Render tombol fisik utama
            btn_fs_toggle.draw(screen)
            pygame.draw.rect(screen, COLOR_WHITE, btn_fs_toggle.rect, 1)
            
            # Trik Visual: Cetak teks ON atau OFF secara dinamis tepat di tengah tombol!
            status_str = "ON" if manager.is_fullscreen else "OFF"
            status_color = COLOR_YELLOW if manager.is_fullscreen else COLOR_WHITE
            status_surf = font_menu.render(status_str, True, status_color)
            
            # Rumus matematika untuk 'Absolute Center Alignment' teks di dalam kotak tombol
            text_x = btn_fs_toggle.rect.x + (btn_fs_toggle.rect.width - status_surf.get_width()) // 2
            text_y = btn_fs_toggle.rect.y + 6
            screen.blit(status_surf, (text_x, text_y))

            # --- BARIS 4: KEMBALI KE MENU ---
            if manager.settings_index == 3:
                btn_settings_kembali.current_color = (60, 70, 100)
                pygame.draw.rect(screen, COLOR_RED, (btn_settings_kembali.rect.x - 2, btn_settings_kembali.rect.y - 2, btn_settings_kembali.rect.width + 4, btn_settings_kembali.rect.height + 4), 2)
            else:
                btn_settings_kembali.current_color = (40, 45, 60)
            btn_settings_kembali.draw(screen)
            pygame.draw.rect(screen, COLOR_WHITE, (btn_settings_kembali.rect.x, btn_settings_kembali.rect.y, btn_settings_kembali.rect.width, btn_settings_kembali.rect.height), 1)

        # ==========================================
        # CUSTOM RENDER LAYAR KREDIT (HIERARKI PS1 UI v1.2.7)
        # ==========================================
        elif manager.current_state == 'CREDIT':
            pygame.draw.rect(screen, (25, 30, 45), (0, 20, SCREEN_WIDTH, 60))
            pygame.draw.line(screen, COLOR_WHITE, (0, 20), (SCREEN_WIDTH, 20), 2) 
            pygame.draw.line(screen, COLOR_WHITE, (0, 80), (SCREEN_WIDTH, 80), 2) 

            title_cred = font_title.render("TIM PENGEMBANG", True, COLOR_YELLOW)
            screen.blit(title_cred, (SCREEN_WIDTH//2 - title_cred.get_width()//2, 30))

            # Injeksi Data Tim Spesifik (Sesuai Koreksi Data Terbaru)
            team_info = [
                ("1. Ihsan Dwi Putra", "15250094", "Programmer"),
                ("2. Azlan", "15250222", "UI/Logic"),
                ("3. Aldo Farisanrya. R", "15250145", "Desain & Integrasi"),
                ("4. Andika Tri Sapto", "15250146", "Desain & Integrasi"),
                ("5. Muhammad Imam Baihaqi", "15250004", "Asset Support") 
            ]

            start_y = 100
            box_h = 60
            spacing = 15
            for i, (name, nim, role) in enumerate(team_info):
                y = start_y + i * (box_h + spacing)
                # Render Panel Luar
                pygame.draw.rect(screen, (40, 45, 60), (60, y, SCREEN_WIDTH - 120, box_h))
                pygame.draw.rect(screen, COLOR_WHITE, (60, y, SCREEN_WIDTH - 120, box_h), 1)
                
                # Render NAMA
                n_txt = font_menu.render(name, True, COLOR_WHITE)
                screen.blit(n_txt, (80, y + 18))
                
                # Render NIM
                nim_txt = font_small.render(nim, True, (180, 180, 180))
                screen.blit(nim_txt, (SCREEN_WIDTH//2, y + 25))
                
                # Render KOTAK ROLE (BADGE)
                role_w, role_h = 180, 35
                role_x = SCREEN_WIDTH - 60 - role_w - 20
                role_y = y + 12
                pygame.draw.rect(screen, (60, 60, 70), (role_x, role_y, role_w, role_h))
                pygame.draw.rect(screen, COLOR_WHITE, (role_x, role_y, role_w, role_h), 1)
                r_txt = font_small.render(role, True, COLOR_WHITE)
                screen.blit(r_txt, (role_x + (role_w - r_txt.get_width())//2, role_y + (role_h - r_txt.get_height())//2))

            # Rendering Tombol Kembali Kredit dengan Efek Hover Merah
            btn_credit_kembali.current_color = (60, 70, 100) if btn_credit_kembali.is_hovered else (40, 45, 60)
            btn_credit_kembali.draw(screen)
            pygame.draw.rect(screen, COLOR_WHITE, (btn_credit_kembali.rect.x, btn_credit_kembali.rect.y, btn_credit_kembali.rect.width, btn_credit_kembali.rect.height), 1)
            if btn_credit_kembali.is_hovered:
                pygame.draw.rect(screen, COLOR_RED, (btn_credit_kembali.rect.x - 2, btn_credit_kembali.rect.y - 2, btn_credit_kembali.rect.width + 4, btn_credit_kembali.rect.height + 4), 2)

        elif manager.current_state == 'MODE_SELECT':
            pygame.draw.rect(screen, (25, 30, 45), (0, 20, SCREEN_WIDTH, 60))
            pygame.draw.line(screen, COLOR_WHITE, (0, 20), (SCREEN_WIDTH, 20), 2) 
            pygame.draw.line(screen, COLOR_WHITE, (0, 80), (SCREEN_WIDTH, 80), 2) 

            header_str = f"PILIH TINGKAT KESULITAN  |  HIGH SCORE: {manager.high_score}"
            header_txt = font_menu.render(header_str, True, COLOR_YELLOW)
            screen.blit(header_txt, (40, 35))

            subtitles = {
                'EASY': "Santai, pola lambat",
                'MEDIUM': "Lebih cepat, skor x1.5",
                'HARD': f"Butuh {manager.mode_requirements['HARD']} pts",
                'IMPOSSIBLE': f"Butuh {manager.mode_requirements['IMPOSSIBLE']} pts",
                'UNLIMITED': "Mode skor tanpa akhir"
            }

            for idx, (mode_name, btn) in enumerate(btn_modes.items()):
                is_locked = manager.get_lock_status(mode_name)
                
                if is_locked:
                    btn.current_color = (60, 60, 60) 
                else:
                    if idx == manager.mode_index:
                        btn.current_color = (60, 70, 100) 
                        pygame.draw.rect(screen, COLOR_RED, (btn.rect.x - 2, btn.rect.y - 2, btn.rect.width + 4, btn.rect.height + 4), 2)
                    else:
                        btn.current_color = (40, 45, 60) 

                btn.draw(screen) 
                pygame.draw.rect(screen, COLOR_WHITE, (btn.rect.x, btn.rect.y, btn.rect.width, btn.rect.height), 1)

                text_color = (150, 150, 150) if is_locked else COLOR_WHITE
                mode_txt = font_menu.render(mode_name, True, text_color)
                sub_txt = font_small.render(subtitles[mode_name], True, (150, 150, 150))
                
                screen.blit(mode_txt, (btn.rect.x + 20, btn.rect.y + 10))
                screen.blit(sub_txt, (btn.rect.x + 20, btn.rect.y + 35))

                badge_w, badge_h = 80, 25
                badge_x = btn.rect.x + btn.rect.width - badge_w - 15
                badge_y = btn.rect.y + (btn.rect.height - badge_h) // 2
                
                if is_locked:
                    pygame.draw.rect(screen, (180, 50, 50), (badge_x, badge_y, badge_w, badge_h))
                    badge_txt = font_small.render("LOCKED", True, COLOR_WHITE)
                else:
                    pygame.draw.rect(screen, (80, 180, 80), (badge_x, badge_y, badge_w, badge_h))
                    badge_txt = font_small.render("TERBUKA", True, COLOR_WHITE)
                
                screen.blit(badge_txt, (badge_x + (badge_w - badge_txt.get_width())//2, badge_y + (badge_h - badge_txt.get_height())//2))

            panel_x, panel_y, panel_w, panel_h = 480, 150, 280, 250
            pygame.draw.rect(screen, (40, 45, 60), (panel_x, panel_y, panel_w, panel_h))
            pygame.draw.rect(screen, COLOR_WHITE, (panel_x, panel_y, panel_w, panel_h), 2)
            
            panel_title = font_menu.render("VALIDASI MODE", True, COLOR_YELLOW)
            screen.blit(panel_title, (panel_x + 20, panel_y + 20))
            
            info_bullets = [
                "EASY untuk demo dosen",
                "MEDIUM terasa paling adil",
                "HARD dibuka dari skor",
                "LOCKED jangan ditumpuk teks",
                "Tombol back wajib jelas"
            ]
            for i, bullet in enumerate(info_bullets):
                b_txt = font_small.render(f"* {bullet}", True, COLOR_WHITE)
                screen.blit(b_txt, (panel_x + 20, panel_y + 70 + (i * 30)))

            if manager.mode_index == len(manager.modes_list):
                btn_mode_kembali.current_color = (150, 50, 50)
            else:
                btn_mode_kembali.current_color = (40, 45, 60)
            btn_mode_kembali.draw(screen)
            pygame.draw.rect(screen, COLOR_WHITE, (btn_mode_kembali.rect.x, btn_mode_kembali.rect.y, btn_mode_kembali.rect.width, btn_mode_kembali.rect.height), 1)

        elif manager.current_state == 'TUTORIAL':
            # Header Banner Gelap
            pygame.draw.rect(screen, (25, 30, 45), (0, 20, SCREEN_WIDTH, 60))
            pygame.draw.line(screen, COLOR_WHITE, (0, 20), (SCREEN_WIDTH, 20), 2) 
            pygame.draw.line(screen, COLOR_WHITE, (0, 80), (SCREEN_WIDTH, 80), 2) 

            header_str = "TUTORIAL SINGKAT: SUSUN BLOK, INGAT WARNA, JANGAN PANIK"
            header_txt = font_menu.render(header_str, True, COLOR_YELLOW)
            screen.blit(header_txt, (40, 35))

            # Panel Kiri (CARA MAIN)
            left_panel = pygame.Rect(40, 100, 340, 360)
            pygame.draw.rect(screen, (40, 45, 60), left_panel)
            pygame.draw.rect(screen, COLOR_WHITE, left_panel, 2)
            
            c_main_txt = font_title.render("CARA MAIN", True, COLOR_YELLOW)
            screen.blit(c_main_txt, (left_panel.x + 20, left_panel.y + 20))

            rules = [
                "1. Perhatikan warna target.",
                "2. Tekan tombol warna.",
                "3. POP untuk hapus blok terakhir.",
                "4. VALIDASI saat urutan benar.",
                "5. Garis merah = zona bahaya."
            ]
            for i, rule in enumerate(rules):
                screen.blit(font_small.render(rule, True, COLOR_WHITE), (left_panel.x + 20, left_panel.y + 80 + (i * 45)))

            # Panel Kanan (KONTROL)
            right_panel = pygame.Rect(420, 100, 340, 360)
            pygame.draw.rect(screen, (40, 45, 60), right_panel)
            pygame.draw.rect(screen, COLOR_WHITE, right_panel, 2)

            kontrol_txt = font_title.render("KONTROL", True, COLOR_YELLOW)
            screen.blit(kontrol_txt, (right_panel.x + 20, right_panel.y + 20))

            controls = [
                ((220, 80, 80), "R", "MERAH"),
                ((80, 140, 220), "B", "BIRU"),
                ((220, 180, 80), "Y", "KUNING"),
                ((80, 220, 80), "G", "HIJAU"),
                ((120, 120, 130), "BACKSPACE", "POP"),
                ((50, 160, 80), "ENTER", "VALIDASI"),
                ((180, 60, 60), "M", "MENYERAH")
            ]
            
            for i, (col, key, desc) in enumerate(controls):
                cy = right_panel.y + 70 + (i * 40)
                pygame.draw.rect(screen, col, (right_panel.x + 20, cy, 100, 30))
                pygame.draw.rect(screen, COLOR_WHITE, (right_panel.x + 20, cy, 100, 30), 1)
                k_txt = font_small.render(key, True, COLOR_WHITE)
                screen.blit(k_txt, (right_panel.x + 20 + (100 - k_txt.get_width())//2, cy + 8))
                d_txt = font_small.render(desc, True, COLOR_WHITE)
                screen.blit(d_txt, (right_panel.x + 140, cy + 8))

            # --- RENOVASI VISUAL STAND OUT TUTORIAL ---
            btn_tut_kembali.current_color = (180, 60, 60) if tutorial_btn_index == 0 else (40, 45, 60)
            btn_tut_lanjut.current_color = (60, 180, 80) if tutorial_btn_index == 1 else (40, 45, 60)

            # Efek Stand Out: Outline tebal dan Panah Retro!
            if tutorial_btn_index == 1:
                pygame.draw.rect(screen, COLOR_GREEN, (btn_tut_lanjut.rect.x - 2, btn_tut_lanjut.rect.y - 2, btn_tut_lanjut.rect.width + 4, btn_tut_lanjut.rect.height + 4), 2)
                screen.blit(font_menu.render(">", True, COLOR_GREEN), (btn_tut_lanjut.rect.x - 25, btn_tut_lanjut.rect.y + 10))
            elif tutorial_btn_index == 0:
                pygame.draw.rect(screen, COLOR_RED, (btn_tut_kembali.rect.x - 2, btn_tut_kembali.rect.y - 2, btn_tut_kembali.rect.width + 4, btn_tut_kembali.rect.height + 4), 2)
                screen.blit(font_menu.render(">", True, COLOR_RED), (btn_tut_kembali.rect.x - 25, btn_tut_kembali.rect.y + 10))

            btn_tut_kembali.draw(screen)
            pygame.draw.rect(screen, COLOR_WHITE, btn_tut_kembali.rect, 1)
            btn_tut_lanjut.draw(screen)
            pygame.draw.rect(screen, COLOR_WHITE, btn_tut_lanjut.rect, 1)
            
            # ==========================================
        # CUSTOM RENDER LAYAR LOADING (PS1 UI v1.2.8)
        # ==========================================
        elif manager.current_state == 'LOADING':
            # Efek Gelap Transparan Overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((15, 15, 20, 240)) 
            screen.blit(overlay, (0,0))
            
            # Garis Putih Dekoratif PS1
            pygame.draw.line(screen, COLOR_WHITE, (100, 100), (SCREEN_WIDTH - 100, 100), 3) 
            pygame.draw.line(screen, COLOR_WHITE, (100, 500), (SCREEN_WIDTH - 100, 500), 3) 

            # Render Logo angSSatan (Menyerap Menu Logo)
            if menu_logo_image:
                logo_rect = menu_logo_image.get_rect(center=(SCREEN_WIDTH//2, 180))
                screen.blit(menu_logo_image, logo_rect)
            else:
                logo_txt = font_title.render("angSSatan", True, COLOR_RED)
                screen.blit(logo_txt, (SCREEN_WIDTH//2 - logo_txt.get_width()//2, 150))

            # Kotak Utama Loading
            load_box_w, load_box_h = 500, 90
            load_box_x = SCREEN_WIDTH//2 - load_box_w//2
            load_box_y = 300
            pygame.draw.rect(screen, (50, 55, 70), (load_box_x, load_box_y, load_box_w, load_box_h))
            pygame.draw.rect(screen, COLOR_WHITE, (load_box_x, load_box_y, load_box_w, load_box_h), 2)
            
            load_txt = font_menu.render("MEMUAT RUANG BERMAIN...", True, COLOR_WHITE)
            screen.blit(load_txt, (load_box_x + 20, load_box_y + 15))
            
            # Progress Bar Bergerak Merah Horor
            bar_w, bar_h = 460, 20
            bar_x, bar_y = load_box_x + 20, load_box_y + 55
            pygame.draw.rect(screen, (30, 35, 45), (bar_x, bar_y, bar_w, bar_h)) 
            pygame.draw.rect(screen, COLOR_WHITE, (bar_x, bar_y, bar_w, bar_h), 1) 
            
            fill_width = int((loading_timer / 3000) * bar_w)
            pygame.draw.rect(screen, (220, 80, 80), (bar_x, bar_y, fill_width, bar_h))
            
            # Teks Petunjuk Misterius (Hints)
            hint_txt = font_small.render(current_hint, True, (150, 150, 150))
            screen.blit(hint_txt, (SCREEN_WIDTH//2 - hint_txt.get_width()//2, 420))

        elif manager.current_state == 'CONFIRM':
            txt_ask = font_title.render("APAKAH ANDA YAKIN?", True, COLOR_WHITE)
            txt_desc = font_menu.render(f"AKSI: {manager.confirm_type}", True, COLOR_YELLOW)
            screen.blit(txt_ask, (SCREEN_WIDTH//2 - txt_ask.get_width()//2, 180))
            screen.blit(txt_desc, (SCREEN_WIDTH//2 - txt_desc.get_width()//2, 240))
            btn_confirm_ya.current_color = (190, 50, 50) if manager.confirm_index == 0 else (140, 40, 40)
            btn_confirm_tidak.current_color = (100, 100, 100) if manager.confirm_index == 1 else (70, 70, 70)
            btn_confirm_ya.draw(screen)
            btn_confirm_tidak.draw(screen)

        elif manager.current_state == 'GAME_OVER':
            pass # UI Game Over lama dihancurkan, diganti dengan Overlay Visual PS1 di bagian bawah

        # ==========================================
        # CUSTOM RENDER FASE PENGINGAT (MEMORIZE PHASE v1.2.9)
        # ==========================================
        elif manager.current_state == 'MEMORIZE':
            # Render Background Khusus Fase Ini
            if memorize_bg_image: screen.blit(memorize_bg_image, (0, 0))
            else: screen.fill(COLOR_BG_SAFE)
            
            mem_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            mem_overlay.fill((10, 10, 15, 200)) # Aura gelap 
            screen.blit(mem_overlay, (0,0))
            
            # --- 1. BAGIAN KIRI ATAS & KANAN ATAS (HUD) ---
            txt_fase = font_menu.render("FASE: MEMORIZE", True, (150, 150, 150))
            screen.blit(txt_fase, (30, 25))
            
            txt_hud_right = font_menu.render(f"LV: {manager.level}   SCORE: {manager.score}", True, COLOR_WHITE)
            screen.blit(txt_hud_right, (SCREEN_WIDTH - 30 - txt_hud_right.get_width(), 25))

            # --- 2. WAKTU RAKSASA (TENGAH ATAS) ---
            # Menggunakan desimal agar lebih presisi dan estetik seperti "4.0s"
            sec_float = max(0.0, manager.state_timer / 1000.0)
            txt_time = font_title.render(f"{sec_float:.1f}s", True, COLOR_RED)
            screen.blit(txt_time, (SCREEN_WIDTH//2 - txt_time.get_width()//2, 20))

            # Garis Pembatas Atas ala Retro UI
            pygame.draw.line(screen, (80, 80, 90), (0, 70), (SCREEN_WIDTH, 70), 2)

            # --- 3. TEKS PANDUAN (TENGAH ATAS BAWAH GARIS) ---
            t_mem = font_title.render("MEMORIZE", True, COLOR_WHITE)
            t_hafalk = font_small.render("PERHATIKAN DAN HAFALKAN URUTAN TOWER", True, (180, 180, 180))
            screen.blit(t_mem, (SCREEN_WIDTH//2 - t_mem.get_width()//2, 85))
            screen.blit(t_hafalk, (SCREEN_WIDTH//2 - t_hafalk.get_width()//2, 135))

            # --- 4. TOWER DRAWING DINAMIS (TENGAH-TENGAH) ---
            blueprint = manager.target_blueprint
            max_blocks = max(7, len(blueprint))
            
            # Kalkulasi cerdas agar menara selalu di tengah (Tidak tembus teks atas/bawah)
            # Area render aman untuk blok: Y=170 sampai Y=380 (Tinggi 210px)
            block_w = 140
            block_h = min(40, int(200 / max_blocks)) # Jika blok banyak (misal 15), tinggi akan otomatis gepeng!
            spacing = block_h + 3
            
            # Menghitung titik awal Y agar tumpukannya selalu "Center-Aligned" secara vertikal
            total_stack_height = len(blueprint) * spacing
            center_y_area = 170 + (210 // 2) 
            start_y = center_y_area + (total_stack_height // 2) - block_h
            start_x = SCREEN_WIDTH // 2 - block_w // 2
            
            color_map = {"Merah": COLOR_RED, "Biru": COLOR_BLUE, "Kuning": COLOR_YELLOW, "Hijau": COLOR_GREEN}

            for i, color_name in enumerate(blueprint):
                y = start_y - (i * spacing)
                color = color_map.get(color_name, COLOR_WHITE)
                rect = pygame.Rect(start_x, y, block_w, block_h)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, COLOR_WHITE, rect, 2) 

            # --- 5. PANEL TEKS BOX (TENGAH BAWAH) ---
            panel_w, panel_h = 440, 75
            panel_x = SCREEN_WIDTH//2 - panel_w//2
            panel_y = 415
            pygame.draw.rect(screen, (20, 20, 25), (panel_x, panel_y, panel_w, panel_h))
            pygame.draw.rect(screen, (150, 50, 50), (panel_x, panel_y, panel_w, panel_h), 2)
            
            t_hafalkan = font_menu.render("HAFALKAN URUTAN INI!", True, COLOR_RED)
            t_will_vanish = font_small.render("Tower akan hilang setelah Waktu habis.", True, COLOR_WHITE)
            screen.blit(t_hafalkan, (SCREEN_WIDTH//2 - t_hafalkan.get_width()//2, panel_y + 15))
            screen.blit(t_will_vanish, (SCREEN_WIDTH//2 - t_will_vanish.get_width()//2, panel_y + 45))

            # --- BAGIAN BAWAH (TOMBOL KEMBALI & LANJUT) Dinamis ---
            btn_mem_kembali.current_color = (180, 60, 60) if memorize_btn_index == 0 else (40, 45, 60)
            btn_mem_lanjut.current_color = (60, 180, 80) if memorize_btn_index == 1 else (40, 45, 60)
            
            if memorize_btn_index == 1:
                pygame.draw.rect(screen, COLOR_GREEN, (btn_mem_lanjut.rect.x - 2, btn_mem_lanjut.rect.y - 2, btn_mem_lanjut.rect.width + 4, btn_mem_lanjut.rect.height + 4), 2)
                screen.blit(font_menu.render(">", True, COLOR_GREEN), (btn_mem_lanjut.rect.x - 25, btn_mem_lanjut.rect.y + 10))
            elif memorize_btn_index == 0:
                pygame.draw.rect(screen, COLOR_RED, (btn_mem_kembali.rect.x - 2, btn_mem_kembali.rect.y - 2, btn_mem_kembali.rect.width + 4, btn_mem_kembali.rect.height + 4), 2)
                screen.blit(font_menu.render(">", True, COLOR_RED), (btn_mem_kembali.rect.x - 25, btn_mem_kembali.rect.y + 10))

            btn_mem_kembali.draw(screen); pygame.draw.rect(screen, COLOR_WHITE, btn_mem_kembali.rect, 1)
            btn_mem_lanjut.draw(screen); pygame.draw.rect(screen, COLOR_WHITE, btn_mem_lanjut.rect, 1)

        # ==========================================
        # RESTORE LOGIKA PLAY DAN PAUSE ORIGINAL
        # ==========================================
        # ==========================================
        # CUSTOM RENDER GAMEPLAY (THE NEW CORE HUD v1.2.9)
        # ==========================================
        elif manager.current_state in ['PLAY', 'PAUSE']:
            # AMKPUTASI: monster.draw(screen) dimatikan agar garis hitam lama menghilang!
            
            # --- EFEK VIGNETTE & MONSTER DINAMIS (MATEMATIKA EKSPONENSIAL) ---
            jarak_pct = max(0.0, min(1.0, 1.0 - (manager.state_timer / manager.play_duration)))
            
            # KUNCI JUMPSCARE: Pangkat 5 membuat ukuran SANGAT LAMBAT membesar di awal,
            # lalu tiba-tiba meledak menjadi raksasa di detik-detik terakhir!
            efek_kejutan = jarak_pct ** 5 
            
            alpha_vignette = int(50 + (efek_kejutan * 180)) # Merah pekat tertunda
            vignette = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            vignette.fill((50, 0, 0, alpha_vignette)) 
            screen.blit(vignette, (0, 0))

            # --- RENDER MONSTER SCALE-UP ---
            if monster_image:
                # Skala dibatasi ketat: Awal 5% (0.05), Maksimal 250% (2.5) HANYA saat waktu habis!
                scale_factor = min(2.5, 0.05 + (2.45 * efek_kejutan)) 
                new_w = int(monster_image.get_width() * scale_factor)
                new_h = int(monster_image.get_height() * scale_factor)
                scaled_monster = pygame.transform.scale(monster_image, (new_w, new_h))
                
                mon_x = SCREEN_WIDTH//2 - new_w//2
                mon_y = SCREEN_HEIGHT//2 - new_h//2 - 40 
                screen.blit(scaled_monster, (mon_x, mon_y))
            
            if manager.current_state == 'PLAY':
                # --- 1. HUD KIRI ATAS ---
                txt_lv = font_menu.render(f"LV: {manager.level}", True, COLOR_WHITE)
                txt_skor = font_menu.render(f"SKOR: {manager.score}", True, COLOR_WHITE)
                txt_mode = font_menu.render(f"MODE: {manager.selected_mode}", True, COLOR_YELLOW)
                screen.blit(txt_lv, (20, 20))
                screen.blit(txt_skor, (20, 50))
                screen.blit(txt_mode, (20, 80))

                # --- 2. TUGAS AKTIF (KIRI TENGAH) ---
                txt_tugas = font_small.render("TUGAS AKTIF", True, COLOR_WHITE)
                txt_val_pola = font_small.render("[X] Validasi pola warna", True, (255, 100, 100))
                txt_susun = font_small.render("    Susun urutan warna", True, (180, 180, 180))
                txt_sesuai = font_small.render("    sesuai target.", True, (180, 180, 180))
                screen.blit(txt_tugas, (20, 150))
                screen.blit(txt_val_pola, (20, 170))
                screen.blit(txt_susun, (20, 190))
                screen.blit(txt_sesuai, (20, 210))

                # --- 3. WAKTU HOROR (TENGAH ATAS) ---
                seconds = max(0, manager.state_timer // 1000)
                ms = max(0, manager.state_timer % 1000)
                txt_waktu = font_title.render(f"{seconds:02d}:{ms:03d}", True, COLOR_RED)
                # Diberi efek bayangan hitam agar jelas di background apapun
                shadow_waktu = font_title.render(f"{seconds:02d}:{ms:03d}", True, (0, 0, 0))
                screen.blit(shadow_waktu, (SCREEN_WIDTH//2 - shadow_waktu.get_width()//2 + 2, 32))
                screen.blit(txt_waktu, (SCREEN_WIDTH//2 - txt_waktu.get_width()//2, 30))

                # --- 4. SKOR TERTINGGI (KANAN ATAS) ---
                txt_hi_label = font_small.render("SKOR TERTINGGI:", True, (180, 180, 180))
                txt_hi_val = font_menu.render(str(manager.high_score), True, COLOR_WHITE)
                screen.blit(txt_hi_label, (SCREEN_WIDTH - 20 - txt_hi_label.get_width(), 20))
                screen.blit(txt_hi_val, (SCREEN_WIDTH - 20 - txt_hi_val.get_width(), 40))

                # --- 5. RENOVASI TOTAL: PANEL VALIDASI POLA WARNA (TENGAH BAWAH) ---
                # Panel dibuat lebih tinggi (h=220 dari h=175 lama) agar stack ngga terhalang tombol!
                panel_val = pygame.Rect(SCREEN_WIDTH//2 - 120, 290, 240, 220)
                pygame.draw.rect(screen, (20, 20, 25, 220), panel_val) 
                pygame.draw.rect(screen, (150, 80, 80), panel_val, 2)
                
                txt_val_title = font_small.render("VALIDASI POLA WARNA", True, COLOR_RED)
                screen.blit(txt_val_title, (SCREEN_WIDTH//2 - txt_val_title.get_width()//2, 300))

                txt_stackmu = font_small.render("STACK-MU", True, COLOR_WHITE)
                screen.blit(txt_stackmu, (SCREEN_WIDTH//2 - txt_stackmu.get_width()//2, 330))

                # Render Visual Stack Dinamis: Jarak Aman Mutlak dari Tombol Validasi!
                color_map = {"Merah": COLOR_RED, "Biru": COLOR_BLUE, "Kuning": COLOR_YELLOW, "Hijau": COLOR_GREEN}
                
                # Ruang aman stack dibatasi dari Y=350 sampai Y=445 (Tinggi = 95px). 
                # Tombol validasi ada di Y=465, jadi tidak akan pernah bertabrakan!
                max_stack = max(5, len(manager.target_blueprint))
                block_h = min(15, int(90 / max_stack)) # Otomatis mengecil jika tumpukan belasan!
                spacing = block_h + 2
                visual_stack_y_base = 445 # Titik fondasi paling bawah (Aman dari tombol)
                
                for i, c_name in enumerate(player_stack.items):
                    b_y = visual_stack_y_base - (i * spacing) 
                    if b_y > 345: # Mencegah stack tumpah ke luar batas atas panel
                        pygame.draw.rect(screen, color_map.get(c_name, COLOR_WHITE), (SCREEN_WIDTH//2 - 60, b_y, 120, block_h))
                        pygame.draw.rect(screen, COLOR_WHITE, (SCREEN_WIDTH//2 - 60, b_y, 120, block_h), 1) # Outline retro

                # --- 6. RENDER TOMBOL 3 KOLOM ---
                # Kolom 0 = Kiri, Kolom 1 = Tengah (VALIDASI saja), Kolom 2 = Kanan
                left_col_btns   = [btn_game_merah, btn_game_biru, btn_game_kuning, btn_game_hijau, btn_game_pop]
                mid_col_btns    = [btn_game_validate]
                right_col_btns  = [btn_game_menyerah, btn_game_jeda]

                for idx, btn in enumerate(left_col_btns):
                    btn.draw(screen)
                    if play_col_index == 0 and play_row_index == idx:
                        pygame.draw.rect(screen, COLOR_WHITE, (btn.rect.x - 2, btn.rect.y - 2, btn.rect.width + 4, btn.rect.height + 4), 2)
                        screen.blit(font_menu.render(">", True, COLOR_WHITE), (btn.rect.x - 20, btn.rect.y + 5))
                    else:
                        pygame.draw.rect(screen, (100, 100, 100), btn.rect, 1)

                for idx, btn in enumerate(mid_col_btns):
                    btn.draw(screen)
                    if play_col_index == 1:
                        pygame.draw.rect(screen, COLOR_WHITE, (btn.rect.x - 2, btn.rect.y - 2, btn.rect.width + 4, btn.rect.height + 4), 2)
                        screen.blit(font_menu.render(">", True, COLOR_WHITE), (btn.rect.x - 20, btn.rect.y + 5))
                    else:
                        pygame.draw.rect(screen, (100, 100, 100), btn.rect, 1)

                for idx, btn in enumerate(right_col_btns):
                    btn.draw(screen)
                    if play_col_index == 2 and play_row_index == idx:
                        pygame.draw.rect(screen, COLOR_WHITE, (btn.rect.x - 2, btn.rect.y - 2, btn.rect.width + 4, btn.rect.height + 4), 2)
                        screen.blit(font_menu.render(">", True, COLOR_WHITE), (btn.rect.x - 20, btn.rect.y + 5))
                    else:
                        pygame.draw.rect(screen, (100, 100, 100), btn.rect, 1)

                # --- 7. RADAR JARAK MONSTER (BAWAH TENGAH) ---
                jarak_pct = max(0.0, min(1.0, 1.0 - (manager.state_timer / manager.play_duration)))
                bar_w, bar_h = 500, 15
                bar_x = SCREEN_WIDTH//2 - bar_w//2 + 60
                bar_y = SCREEN_HEIGHT - 35
                
                txt_jarak = font_small.render("JARAK MONSTER", True, COLOR_RED)
                screen.blit(txt_jarak, (bar_x - 120, bar_y + 1))
                
                # Dasar Radar Gelap
                pygame.draw.rect(screen, (40, 20, 20), (bar_x, bar_y, bar_w, bar_h))
                # Isi Darah Mendekat
                pygame.draw.rect(screen, (180, 40, 40), (bar_x, bar_y, int(bar_w * jarak_pct), bar_h))
                pygame.draw.rect(screen, COLOR_RED, (bar_x, bar_y, bar_w, bar_h), 1)
                
                # Garis Scanner Radar
                for i in range(1, 25):
                    pygame.draw.line(screen, (80, 30, 30), (bar_x + (i * 20), bar_y), (bar_x + (i * 20), bar_y + bar_h))
                
                txt_pct = font_small.render(f"{int(jarak_pct * 100)}%", True, COLOR_WHITE)
                screen.blit(txt_pct, (bar_x + bar_w + 10, bar_y + 1))

            # Dialog Batin Karakter saat Salah Susun
            if manager.inner_monologue_text != "":
                txt_batin_surf = font_batin.render(manager.inner_monologue_text, True, (255, 120, 120))
                screen.blit(txt_batin_surf, (SCREEN_WIDTH//2 - txt_batin_surf.get_width()//2, 530))
            
            # Lampu Indikator Kecil di Pojok Kanan Atas
            if manager.indicator_light:
                lamp_color = (180, 40, 40) if manager.state_timer < 15000 else (50, 200, 50)
                pygame.draw.circle(screen, lamp_color, (SCREEN_WIDTH - 30, 80), 8)
                
            # Render HUD Polos khusus saat layar tertimpa Menu PAUSE
            if manager.current_state == 'PAUSE':
                info_text = font_menu.render("DIJEDA", True, COLOR_WHITE)
                screen.blit(info_text, (20, 20))

        if manager.current_state in ['INTRO_STUDIO', 'INTRO_PRODUCER', 'INTRO_DISCLAIMER']:
            fade_surface.set_alpha(manager.fade_alpha)
            screen.blit(fade_surface, (0, 0))
        
        # ==========================================
        # CUSTOM RENDER PAUSE MENU (PS1 RETRO UI)
        # ==========================================
        if manager.current_state == 'PAUSE':
            # Dimmed Background Overlay 60% Opacity untuk menahan ketegangan horor
            pause_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            pause_overlay.fill((10, 10, 15, 160)) 
            screen.blit(pause_overlay, (0,0))
            
            panel_w, panel_h = 420, 360
            panel_x = SCREEN_WIDTH//2 - panel_w//2
            panel_y = SCREEN_HEIGHT//2 - panel_h//2
            
            pygame.draw.rect(screen, (35, 40, 55), (panel_x, panel_y, panel_w, panel_h))
            pygame.draw.rect(screen, COLOR_WHITE, (panel_x, panel_y, panel_w, panel_h), 2)
            pygame.draw.rect(screen, (20, 20, 30), (panel_x+5, panel_y+5, panel_w, panel_h), 2)

            pause_title = font_title.render("PERMAINAN DIJEDA", True, COLOR_YELLOW)
            screen.blit(pause_title, (SCREEN_WIDTH//2 - pause_title.get_width()//2, panel_y + 30))
            
            # Kalimat Psikologis Horor
            pause_sub = font_small.render("napas dulu, manusia rapuh", True, (160, 160, 160))
            screen.blit(pause_sub, (SCREEN_WIDTH//2 - pause_sub.get_width()//2, panel_y + 70))

            for idx, btn in enumerate(btn_pause_options):
                if idx == manager.pause_index: 
                    btn.current_color = (120, 50, 50) # Merah redup mencekam
                    pygame.draw.rect(screen, COLOR_RED, (btn.rect.x - 2, btn.rect.y - 2, btn.rect.width + 4, btn.rect.height + 4), 2)
                    # Ornamen panah kecil ala retro UI
                    arrow = font_menu.render(">", True, COLOR_RED)
                    screen.blit(arrow, (btn.rect.x - 25, btn.rect.y + 10))
                else: 
                    btn.current_color = (50, 55, 75)
                btn.draw(screen)
                pygame.draw.rect(screen, COLOR_WHITE, btn.rect, 1)

            footer_txt = font_small.render("ESC: KEMBALI  |  ENTER: PILIH", True, (130, 130, 140))
            screen.blit(footer_txt, (SCREEN_WIDTH//2 - footer_txt.get_width()//2, panel_y + panel_h - 30))
        
        # ==========================================
        # CUSTOM RENDER GAME OVER (PS1 RETRO UI)
        # ==========================================
        if manager.current_state == 'GAME_OVER':
            # Dimmed Background Overlay 78% Opacity (Lebih pekat dari menu Jeda)
            go_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            go_overlay.fill((15, 15, 20, 200)) 
            screen.blit(go_overlay, (0,0))

            # Header Judul
            title_go_1 = font_title.render("SISTEM HANCUR", True, (220, 80, 80)) 
            title_go_2 = font_menu.render("( GAME OVER )", True, (220, 80, 80))
            screen.blit(title_go_1, (SCREEN_WIDTH//2 - title_go_1.get_width()//2, 60))
            screen.blit(title_go_2, (SCREEN_WIDTH//2 - title_go_2.get_width()//2, 110))

            # Panel Kotak Statistik Skor dan Waktu
            panel_w, panel_h = 340, 80
            panel_x = SCREEN_WIDTH//2 - panel_w//2
            panel_y = 160
            pygame.draw.rect(screen, (50, 55, 65), (panel_x, panel_y, panel_w, panel_h))
            pygame.draw.rect(screen, COLOR_WHITE, (panel_x, panel_y, panel_w, panel_h), 2)
            
            skor_txt = font_menu.render(f"SKOR AKHIR : {manager.score}", True, COLOR_WHITE)
            total_sec = total_play_time_ms // 1000
            total_min = total_sec // 60
            sisa_sec  = total_sec % 60
            waktu_txt = font_menu.render(f"WAKTU      : {total_min:02d}:{sisa_sec:02d}", True, COLOR_WHITE)
            
            screen.blit(skor_txt, (panel_x + 20, panel_y + 15))
            screen.blit(waktu_txt, (panel_x + 20, panel_y + 45))

            # Rendering Tombol Retro dengan Panah Merah
            for idx, btn in enumerate(btn_go_options):
                if idx == manager.game_over_index: 
                    btn.current_color = (120, 50, 50) 
                    pygame.draw.rect(screen, COLOR_RED, (btn.rect.x - 2, btn.rect.y - 2, btn.rect.width + 4, btn.rect.height + 4), 2)
                    arrow = font_menu.render(">", True, COLOR_RED)
                    screen.blit(arrow, (btn.rect.x - 25, btn.rect.y + 10))
                else: 
                    btn.current_color = (40, 45, 60)
                btn.draw(screen)
                pygame.draw.rect(screen, COLOR_WHITE, btn.rect, 1)

            # Footer Teks Psikologis Redup
            hint_go = font_small.render("petunjuk: jangan asal validasi saat panik", True, (150, 150, 150))
            screen.blit(hint_go, (SCREEN_WIDTH//2 - hint_go.get_width()//2, 480))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()