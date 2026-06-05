import pygame
import sys
import os
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
pygame.display.set_caption("angSSatan v1.2")
clock = pygame.time.Clock()

font_title = pygame.font.SysFont("Consolas", 42, bold=True)
font_menu = pygame.font.SysFont("Consolas", 24)
font_tut = pygame.font.SysFont("Consolas", 18)
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
    except pygame.error: print("[AUDIO] Gagal memuat beberapa SFX In-Game.")

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

    video_frames_dir = os.path.join("assets", "video_frames")
    frame_files = []
    if os.path.exists(video_frames_dir):
        frame_files = sorted([f for f in os.listdir(video_frames_dir) if f.endswith(('.png', '.jpg', '.jpeg'))])
    current_frame_index = 0
    frame_timer = 0
    frame_duration = 40  
    cached_frame_img = None
    cached_frame_idx = -1

    # ==========================================
    # INITIALIZATION INTERACTIVE BUTTONS
    # ==========================================
    btn_menu_options = [
        Button(40, 220, 260, 50, "MULAI", (40, 45, 60), (60, 70, 100), font_size=22),
        Button(40, 290, 260, 50, "PENGATURAN", (40, 45, 60), (60, 70, 100), font_size=22),
        Button(40, 360, 260, 50, "CREDIT", (40, 45, 60), (60, 70, 100), font_size=22),
        Button(40, 430, 260, 50, "KELUAR", (40, 45, 60), (120, 40, 40), font_size=22)
    ]

    btn_bgm_minus = Button(480, 200, 40, 35, "-", (50, 60, 80), (80, 100, 140))
    btn_bgm_plus  = Button(540, 200, 40, 35, "+", (50, 60, 80), (80, 100, 140))
    btn_sfx_minus = Button(480, 250, 40, 35, "-", (50, 60, 80), (80, 100, 140))
    btn_sfx_plus  = Button(540, 250, 40, 35, "+", (50, 60, 80), (80, 100, 140))
    btn_fs_toggle = Button(480, 300, 100, 35, "UBAH", (50, 60, 80), (80, 100, 140))
    btn_settings_kembali = Button(SCREEN_WIDTH//2 - 150, 380, 300, 40, "KEMBALI KE MENU", (80, 80, 80), (50, 50, 50))
    btn_credit_kembali = Button(SCREEN_WIDTH//2 - 150, 480, 300, 40, "KEMBALI KE MENU", (80, 80, 80), (50, 50, 50))

    btn_modes = {
        'EASY':       Button(SCREEN_WIDTH//2 - 160, 150, 320, 40, "EASY", (30, 40, 50), (50, 70, 90)),
        'MEDIUM':     Button(SCREEN_WIDTH//2 - 160, 200, 320, 40, "MEDIUM", (30, 40, 50), (50, 70, 90)),
        'HARD':       Button(SCREEN_WIDTH//2 - 160, 250, 320, 40, "HARD", (30, 40, 50), (50, 70, 90)),
        'IMPOSSIBLE': Button(SCREEN_WIDTH//2 - 160, 300, 320, 40, "IMPOSSIBLE", (30, 40, 50), (50, 70, 90)),
        'UNLIMITED':  Button(SCREEN_WIDTH//2 - 160, 350, 320, 40, "UNLIMITED", (30, 40, 50), (50, 70, 90)),
    }
    btn_mode_kembali  = Button(SCREEN_WIDTH//2 - 160, 420, 320, 40, "KEMBALI", (80, 80, 80), (50, 50, 50))

    btn_game_merah    = Button(580, 120, 180, 40, "[R] MERAH", COLOR_RED, (150, 30, 30))
    btn_game_biru     = Button(580, 170, 180, 40, "[B] BIRU", COLOR_BLUE, (30, 60, 150))
    btn_game_kuning   = Button(580, 220, 180, 40, "[Y] KUNING", COLOR_YELLOW, (150, 140, 30))
    btn_game_hijau    = Button(580, 270, 180, 40, "[G] HIJAU", COLOR_GREEN, (30, 130, 30))
    
    btn_game_pop      = Button(580, 330, 180, 40, "[BACK] POP", (100, 100, 100), (70, 70, 70))
    btn_game_validate = Button(580, 380, 180, 40, "[ENTER] VALIDASI", (40, 140, 70), (20, 90, 45))
    btn_game_menyerah = Button(580, 440, 180, 40, "[M] MENYERAH", (180, 40, 40), (120, 30, 30))
    btn_game_keluar   = Button(580, 490, 180, 40, "[Q] MENU", (50, 50, 50), (30, 30, 30))

    btn_confirm_ya    = Button(SCREEN_WIDTH//2 - 130, 320, 110, 40, "YA [Y]", (140, 40, 40), (190, 50, 50))
    btn_confirm_tidak = Button(SCREEN_WIDTH//2 + 20, 320, 110, 40, "TIDAK [N]", (70, 70, 70), (100, 100, 100))

    btn_go_options = [
        Button(SCREEN_WIDTH//2 - 150, 280, 300, 40, "ULANG PERMAINAN", (40, 45, 60), (60, 70, 100)),
        Button(SCREEN_WIDTH//2 - 150, 340, 300, 40, "UBAH MODE KESULITAN", (40, 45, 60), (60, 70, 100)),
        Button(SCREEN_WIDTH//2 - 150, 400, 300, 40, "KEMBALI KE MENU", (40, 45, 60), (120, 40, 40))
    ]

    btn_tut_paham     = Button(SCREEN_WIDTH//2 - 130, 380, 110, 40, "PAHAM", (40, 120, 60), (50, 180, 80))
    btn_tut_lewati    = Button(SCREEN_WIDTH//2 + 20, 380, 110, 40, "LEWATI", (100, 100, 100), (60, 60, 60))

    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill((0, 0, 0))

    is_running = True

    while is_running:
        delta_time = clock.get_time()
        mouse_pos = pygame.mouse.get_pos() 
        
        # ==========================================
        # BGM MUTE SAAT FASE KONFIRMASI
        # ==========================================
        if manager.current_state in ['MAIN_MENU', 'SETTINGS_MENU', 'CREDIT', 'MODE_SELECT', 'TUTORIAL']:
            target_bgm_state = 'MENU'
        elif manager.current_state in ['PLAY', 'MEMORIZE', 'GAME_OVER']:
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
        # UPDATE ANIMASI FRAME VIDEO BACKGROUND LOOP
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
        elif manager.current_state == 'SETTINGS_MENU': active_buttons = [btn_bgm_minus, btn_bgm_plus, btn_sfx_minus, btn_sfx_plus, btn_fs_toggle, btn_settings_kembali]
        elif manager.current_state == 'CREDIT': active_buttons = [btn_credit_kembali]
        elif manager.current_state == 'MODE_SELECT': active_buttons = list(btn_modes.values()) + [btn_mode_kembali]
        elif manager.current_state == 'TUTORIAL': active_buttons = [btn_tut_paham, btn_tut_lewati]
        elif manager.current_state == 'PLAY': active_buttons = [btn_game_merah, btn_game_biru, btn_game_kuning, btn_game_hijau, btn_game_pop, btn_game_validate, btn_game_menyerah, btn_game_keluar]
        elif manager.current_state == 'CONFIRM': active_buttons = [btn_confirm_ya, btn_confirm_tidak]
        elif manager.current_state == 'GAME_OVER': active_buttons = btn_go_options

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
            for idx, btn in enumerate([btn_bgm_minus, btn_sfx_minus, btn_fs_toggle, btn_settings_kembali]):
                if btn.is_hovered: manager.settings_index = idx
        elif manager.current_state == 'MODE_SELECT':
            for idx, btn in enumerate(list(btn_modes.values())):
                if btn.is_hovered: manager.mode_index = idx
        elif manager.current_state == 'CONFIRM':
            if btn_confirm_ya.is_hovered: manager.confirm_index = 0
            elif btn_confirm_tidak.is_hovered: manager.confirm_index = 1
        elif manager.current_state == 'GAME_OVER':
            for idx, btn in enumerate(btn_go_options):
                if btn.is_hovered: manager.game_over_index = idx 

        # ==========================================
        # EVENT HANDLING (SINKRONISASI MOUSE + KEYBOARD)
        # ==========================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                
            # --- INPUT KENDALI MOUSE CLICK ---
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if manager.current_state in ['INTRO_STUDIO', 'INTRO_PRODUCER', 'INTRO_DISCLAIMER']:
                    manager.skip_intro()
                    
                elif manager.current_state == 'MAIN_MENU':
                    clicked = False
                    if btn_menu_options[0].is_clicked(event, mouse_pos): manager.current_state = 'MODE_SELECT'; clicked = True
                    elif btn_menu_options[1].is_clicked(event, mouse_pos): manager.current_state = 'SETTINGS_MENU'; clicked = True
                    elif btn_menu_options[2].is_clicked(event, mouse_pos): manager.current_state = 'CREDIT'; clicked = True
                    elif btn_menu_options[3].is_clicked(event, mouse_pos): manager.trigger_confirm('KELUAR_APP'); clicked = True
                    if clicked: play_click()
                    
                elif manager.current_state == 'SETTINGS_MENU':
                    clicked = True
                    if btn_bgm_minus.is_clicked(event, mouse_pos): manager.volume_bgm = max(0, manager.volume_bgm - 10)
                    elif btn_bgm_plus.is_clicked(event, mouse_pos):  manager.volume_bgm = min(100, manager.volume_bgm + 10)
                    elif btn_sfx_minus.is_clicked(event, mouse_pos): manager.volume_sfx = max(0, manager.volume_sfx - 10)
                    elif btn_sfx_plus.is_clicked(event, mouse_pos):  manager.volume_sfx = min(100, manager.volume_sfx + 10)
                    elif btn_fs_toggle.is_clicked(event, mouse_pos):
                        manager.is_fullscreen = not manager.is_fullscreen
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), (pygame.FULLSCREEN | pygame.SCALED) if manager.is_fullscreen else pygame.SCALED)
                    elif btn_settings_kembali.is_clicked(event, mouse_pos): manager.current_state = 'MAIN_MENU'
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
                    clicked = True
                    if btn_tut_paham.is_clicked(event, mouse_pos):
                        manager.tutorial_step += 1
                        if manager.tutorial_step >= len(manager.tutorial_messages): manager.current_state = 'MEMORIZE'
                    elif btn_tut_lewati.is_clicked(event, mouse_pos): manager.current_state = 'MEMORIZE'
                    else: clicked = False
                    if clicked: play_click()
                    
                elif manager.current_state == 'PLAY':
                    if btn_game_merah.is_clicked(event, mouse_pos):     player_stack.push("Merah"); play_push()
                    elif btn_game_biru.is_clicked(event, mouse_pos):    player_stack.push("Biru"); play_push()
                    elif btn_game_kuning.is_clicked(event, mouse_pos):  player_stack.push("Kuning"); play_push()
                    elif btn_game_hijau.is_clicked(event, mouse_pos):   player_stack.push("Hijau"); play_push()
                    elif btn_game_pop.is_clicked(event, mouse_pos):     player_stack.pop(); play_pop()
                    elif btn_game_menyerah.is_clicked(event, mouse_pos): manager.trigger_confirm('MENYERAH'); play_click()
                    elif btn_game_keluar.is_clicked(event, mouse_pos):   manager.trigger_confirm('KELUAR_MENU'); play_click()
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
                        elif manager.confirm_type == 'KELUAR_MENU':
                            manager.reset_to_menu()
                            player_stack.clear_stack() 
                        elif manager.confirm_type == 'KELUAR_APP': 
                            is_running = False
                    elif btn_confirm_tidak.is_clicked(event, mouse_pos): manager.cancel_confirm()
                    else: clicked = False
                    if clicked: play_click()
                            
                elif manager.current_state == 'GAME_OVER':
                    clicked = True
                    if btn_go_options[0].is_clicked(event, mouse_pos):   
                        manager.restart_level()
                        player_stack.clear_stack() 
                    elif btn_go_options[1].is_clicked(event, mouse_pos): 
                        manager.current_state = 'MODE_SELECT'
                        player_stack.clear_stack() 
                    elif btn_go_options[2].is_clicked(event, mouse_pos): 
                        manager.reset_to_menu()
                        player_stack.clear_stack() 
                    else: clicked = False
                    if clicked: play_click()

            # --- INPUT KENDALI KEYBOARD ---
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: is_running = False
                
                if manager.current_state in ['INTRO_STUDIO', 'INTRO_PRODUCER', 'INTRO_DISCLAIMER']:
                    if event.key in [pygame.K_RETURN, pygame.K_SPACE]: manager.skip_intro()
                
                elif manager.current_state == 'MAIN_MENU':
                    if event.key == pygame.K_DOWN:   manager.menu_index = (manager.menu_index + 1) % len(manager.menu_options); play_hover()
                    elif event.key == pygame.K_UP:   manager.menu_index = (manager.menu_index - 1) % len(manager.menu_options); play_hover()
                    elif event.key == pygame.K_RETURN:
                        play_click()
                        if manager.menu_index == 0:   manager.current_state = 'MODE_SELECT'
                        elif manager.menu_index == 1: manager.current_state = 'SETTINGS_MENU'
                        elif manager.menu_index == 2: manager.current_state = 'CREDIT'
                        elif manager.menu_index == 3: manager.trigger_confirm('KELUAR_APP')
                
                elif manager.current_state == 'SETTINGS_MENU':
                    if event.key == pygame.K_DOWN:   manager.settings_index = (manager.settings_index + 1) % len(manager.settings_options); play_hover()
                    elif event.key == pygame.K_UP:   manager.settings_index = (manager.settings_index - 1) % len(manager.settings_options); play_hover()
                    elif event.key == pygame.K_RIGHT:
                        play_click()
                        if manager.settings_index == 0: manager.volume_bgm = min(100, manager.volume_bgm + 10)
                        elif manager.settings_index == 1: manager.volume_sfx = min(100, manager.volume_sfx + 10)
                        elif manager.settings_index == 2: 
                            manager.is_fullscreen = True
                            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
                    elif event.key == pygame.K_LEFT:
                        play_click()
                        if manager.settings_index == 0: manager.volume_bgm = max(0, manager.volume_bgm - 10)
                        elif manager.settings_index == 1: manager.volume_sfx = max(0, manager.volume_sfx - 10)
                        elif manager.settings_index == 2: 
                            manager.is_fullscreen = False
                            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED)
                    elif event.key == pygame.K_RETURN and manager.settings_index == 3:
                        play_click(); manager.current_state = 'MAIN_MENU'
                
                elif manager.current_state in ['CREDIT']:
                    if event.key == pygame.K_RETURN: play_click(); manager.current_state = 'MAIN_MENU'
                
                elif manager.current_state == 'TUTORIAL':
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        play_click()
                        manager.tutorial_step += 1
                        if manager.tutorial_step >= len(manager.tutorial_messages): manager.current_state = 'MEMORIZE'
                    elif event.key == pygame.K_ESCAPE: manager.current_state = 'MEMORIZE'
                
                elif manager.current_state == 'MODE_SELECT':
                    if event.key == pygame.K_DOWN:   manager.mode_index = (manager.mode_index + 1) % (len(manager.modes_list) + 1); play_hover()
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
                
                elif manager.current_state == 'PLAY':
                    if event.key == pygame.K_r: player_stack.push("Merah"); play_push()
                    elif event.key == pygame.K_b: player_stack.push("Biru"); play_push()
                    elif event.key == pygame.K_y: player_stack.push("Kuning"); play_push()
                    elif event.key == pygame.K_g: player_stack.push("Hijau"); play_push()
                    elif event.key == pygame.K_BACKSPACE: player_stack.pop(); play_pop()
                    elif event.key == pygame.K_m: manager.trigger_confirm('MENYERAH'); play_click()
                    elif event.key == pygame.K_q: manager.trigger_confirm('KELUAR_MENU'); play_click()
                    elif event.key == pygame.K_RETURN:
                        player_stack.target_blueprint = manager.target_blueprint
                        if player_stack.check_match():
                            manager.handle_success()
                            player_stack.clear_stack()
                            play_success()
                        else:
                            manager.trigger_inner_monologue()
                            play_error()
                
                elif manager.current_state == 'CONFIRM':
                    if event.key == pygame.K_LEFT: manager.confirm_index = 0; play_hover()
                    elif event.key == pygame.K_RIGHT: manager.confirm_index = 1; play_hover()
                    elif event.key == pygame.K_y or (event.key == pygame.K_RETURN and manager.confirm_index == 0):
                        play_click()
                        if manager.confirm_type == 'MENYERAH': 
                            manager.trigger_game_over()
                        elif manager.confirm_type == 'KELUAR_MENU':
                            manager.reset_to_menu()
                            player_stack.clear_stack() 
                        elif manager.confirm_type == 'KELUAR_APP': 
                            is_running = False
                    elif event.key == pygame.K_n or event.key == pygame.K_ESCAPE or (event.key == pygame.K_RETURN and manager.confirm_index == 1):
                        play_click(); manager.cancel_confirm()
                
                elif manager.current_state == 'GAME_OVER':
                    if event.key == pygame.K_DOWN:   manager.game_over_index = (manager.game_over_index + 1) % len(manager.game_over_options); play_hover()
                    elif event.key == pygame.K_UP:   manager.game_over_index = (manager.game_over_index - 1) % len(manager.game_over_options); play_hover()
                    elif event.key == pygame.K_RETURN:
                        play_click()
                        if manager.game_over_index == 0:   
                            manager.restart_level()
                            player_stack.clear_stack() 
                        elif manager.game_over_index == 1: 
                            manager.current_state = 'MODE_SELECT'
                            player_stack.clear_stack() 
                        elif manager.game_over_index == 2: 
                            manager.reset_to_menu()
                            player_stack.clear_stack() 

        # ---- 3. LOGIKA UPDATE ----
        manager.update_timer(delta_time)
        if manager.current_state == 'PLAY':
            monster.update(manager.state_timer, manager.play_duration)
        elif manager.current_state == 'MEMORIZE':
            monster.current_x = monster.start_x

        # ---- 4. RENDER VISUAL V1.2 ----
        if manager.current_state in ['INTRO_STUDIO', 'INTRO_PRODUCER', 'INTRO_DISCLAIMER']:
            screen.fill((0, 0, 0)) 
        elif manager.current_state == 'MAIN_MENU':
            if cached_frame_img:
                screen.blit(cached_frame_img, (0, 0))
            else:
                screen.fill(COLOR_BG_SAFE) 
        elif manager.current_state == 'PLAY' and manager.state_timer < 15000:
            screen.fill(COLOR_BG_DANGER)
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
                title_text = font_title.render("angSSatan v1.2", True, COLOR_RED)
                screen.blit(title_text, (480, 100))
                
            for idx, btn in enumerate(btn_menu_options):
                if idx == manager.menu_index: btn.current_color = (60, 70, 100)
                btn.draw(screen)

            # ==========================================
            # CELAH TERPENUHI: MERENDER WATERMARK VERSI GAME (KANAN BAWAH)
            # ==========================================
            # Menggunakan font_tut (Consolas 18) berwarna abu-abu redup agar estetis dan tidak mendistrak menu utama
            version_text = font_tut.render("angSSatan v1.2.0", True, (130, 130, 140))
            # Menghitung koordinat sudut kanan bawah dengan padding aman 15 piksel dari tepi
            version_x = SCREEN_WIDTH - version_text.get_width() - 15
            version_y = SCREEN_HEIGHT - version_text.get_height() - 15
            screen.blit(version_text, (version_x, version_y))

        elif manager.current_state == 'SETTINGS_MENU':
            title_set = font_title.render("PENGATURAN", True, COLOR_YELLOW)
            screen.blit(title_set, (SCREEN_WIDTH//2 - title_set.get_width()//2, 80))
            txt_bgm = font_menu.render(f"BGM VOLUME: {manager.volume_bgm}%", True, COLOR_WHITE if manager.settings_index == 0 else (150, 150, 150))
            txt_sfx = font_menu.render(f"SFX VOLUME: {manager.volume_sfx}%", True, COLOR_WHITE if manager.settings_index == 1 else (150, 150, 150))
            txt_fs  = font_menu.render(f"FULLSCREEN: {'ON' if manager.is_fullscreen else 'OFF'}", True, COLOR_WHITE if manager.settings_index == 2 else (150, 150, 150))
            screen.blit(txt_bgm, (150, 205))
            screen.blit(txt_sfx, (150, 255))
            screen.blit(txt_fs,  (150, 305))
            if manager.settings_index == 0:
                btn_bgm_minus.current_color = (80, 100, 140)
                btn_bgm_plus.current_color = (80, 100, 140)
            btn_bgm_minus.draw(screen)
            btn_bgm_plus.draw(screen)
            if manager.settings_index == 1:
                btn_sfx_minus.current_color = (80, 100, 140)
                btn_sfx_plus.current_color = (80, 100, 140)
            btn_sfx_minus.draw(screen)
            btn_sfx_plus.draw(screen)
            if manager.settings_index == 2: btn_fs_toggle.current_color = (80, 100, 140)
            btn_fs_toggle.draw(screen)
            if manager.settings_index == 3: btn_settings_kembali.current_color = (100, 100, 100)
            btn_settings_kembali.draw(screen)

        elif manager.current_state == 'CREDIT':
            title_cred = font_title.render("TIM PENGEMBANG", True, COLOR_RED)
            screen.blit(title_cred, (SCREEN_WIDTH//2 - title_cred.get_width()//2, 80))
            for i, member in enumerate(manager.team_members):
                txt_mem = font_menu.render(member, True, COLOR_WHITE)
                screen.blit(txt_mem, (SCREEN_WIDTH//2 - txt_mem.get_width()//2, 180 + (i * 45)))
            btn_credit_kembali.draw(screen)

        elif manager.current_state == 'MODE_SELECT':
            title_mode = font_menu.render(f"PILIH TINGKAT KESULITAN (HIGH SCORE: {manager.high_score})", True, COLOR_YELLOW)
            screen.blit(title_mode, (SCREEN_WIDTH//2 - title_mode.get_width()//2, 70))
            for idx, (mode_name, btn) in enumerate(btn_modes.items()):
                is_locked = manager.get_lock_status(mode_name)
                req_points = manager.mode_requirements[mode_name]
                btn.text = f"{mode_name} (Butuh {req_points} Pts) [LOCKED]" if is_locked else mode_name
                if is_locked: btn.current_color = (40, 40, 40)
                elif idx == manager.mode_index: btn.current_color = (50, 70, 90)
                btn.draw(screen)
            if manager.mode_index == len(manager.modes_list): btn_mode_kembali.current_color = (50, 50, 50)
            btn_mode_kembali.draw(screen)

        elif manager.current_state == 'TUTORIAL':
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((10, 10, 15, 230)) 
            screen.blit(overlay, (0,0))
            pygame.draw.rect(screen, (30, 35, 50), (100, 150, 600, 300))
            pygame.draw.rect(screen, COLOR_YELLOW, (100, 150, 600, 300), 2)
            title_tut = font_menu.render(f"PANDUAN OPERASIONAL - LANGKAH {manager.tutorial_step + 1}/4", True, COLOR_YELLOW)
            screen.blit(title_tut, (SCREEN_WIDTH//2 - title_tut.get_width()//2, 175))
            lines = manager.tutorial_messages[manager.tutorial_step]
            for i, line_text in enumerate(lines):
                txt_render = font_tut.render(line_text, True, COLOR_WHITE if i > 0 else COLOR_YELLOW)
                screen.blit(txt_render, (SCREEN_WIDTH//2 - txt_render.get_width()//2, 230 + (i * 30)))
            btn_tut_paham.draw(screen)
            btn_tut_lewati.draw(screen)

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
            txt_go = font_title.render("SISTEM HANCUR (GAME OVER)", True, COLOR_RED)
            screen.blit(txt_go, (SCREEN_WIDTH//2 - txt_go.get_width()//2, 100))
            for idx, btn in enumerate(btn_go_options):
                if idx == manager.game_over_index: btn.current_color = (60, 70, 100)
                btn.draw(screen)

        elif manager.current_state in ['MEMORIZE', 'PLAY']:
            monster.draw(screen)
            if manager.current_state == 'MEMORIZE':
                tower_renderer.draw_player_tower(screen, manager.target_blueprint)
                state_desc = f"MODE: {manager.selected_mode} | INGAT CETAK BIRU!"
            elif manager.current_state == 'PLAY':
                tower_renderer.draw_player_tower(screen, player_stack.items)
                state_desc = f"MODE: {manager.selected_mode}"
                for btn in [btn_game_merah, btn_game_biru, btn_game_kuning, btn_game_hijau, 
                            btn_game_pop, btn_game_validate, btn_game_menyerah, btn_game_keluar]:
                    btn.draw(screen)
            if manager.inner_monologue_text != "":
                txt_batin_surf = font_batin.render(manager.inner_monologue_text, True, (255, 120, 120))
                screen.blit(txt_batin_surf, (SCREEN_WIDTH//2 - txt_batin_surf.get_width()//2, 560))
            if manager.indicator_light:
                lamp_color = (50, 255, 50) if manager.current_state == 'PLAY' else (255, 255, 50)
                pygame.draw.circle(screen, lamp_color, (750, 40), 15)
            seconds = manager.state_timer // 1000
            ms = manager.state_timer % 1000
            ui_text = font_menu.render(f"LV: {manager.level} | SCORE: {manager.score} | TIME: {seconds:02d}:{ms:03d}", True, COLOR_WHITE)
            info_text = font_menu.render(state_desc, True, COLOR_WHITE)
            screen.blit(ui_text, (20, 20))
            screen.blit(info_text, (20, 60))

        if manager.current_state in ['INTRO_STUDIO', 'INTRO_PRODUCER', 'INTRO_DISCLAIMER']:
            fade_surface.set_alpha(manager.fade_alpha)
            screen.blit(fade_surface, (0, 0))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()