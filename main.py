import pygame
import sys
from settings import *
from core.stack_logic import AbyssalStack
from core.game_manager import GameManager
from entities.tower import TowerRenderer
from entities.monster import AbyssalMonster

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("AngsSatan Project - Core Logic Scaffolding")
clock = pygame.time.Clock()

game_font = pygame.font.SysFont("Consolas", 28)

def main():
    # Inisialisasi Fondasi Utama
    manager = GameManager()
    player_stack = AbyssalStack(manager.target_blueprint)
    tower_renderer = TowerRenderer()
    monster = AbyssalMonster()

    is_running = True

    while is_running:
        delta_time = clock.get_time()
        
        # ---- 1. INPUT HANDLING ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_running = False
                
                # Input hanya diterima jika berada dalam State 'PLAY'
                if manager.current_state == 'PLAY':
                    if event.key == pygame.K_r:
                        player_stack.push("Merah")
                    elif event.key == pygame.K_b:
                        player_stack.push("Biru")
                    elif event.key == pygame.K_y:
                        player_stack.push("Kuning")
                    elif event.key == pygame.K_g:
                        player_stack.push("Hijau")
                    elif event.key == pygame.K_BACKSPACE:
                        player_stack.pop()
                    elif event.key == pygame.K_RETURN:
                        # Sinkronisasi Validasi ke Game Manager
                        player_stack.target_blueprint = manager.target_blueprint
                        if player_stack.check_match():
                            manager.handle_success()
                            player_stack.clear_stack()
                
                # Jika Game Over, tekan ENTER untuk reset permainan
                elif manager.current_state == 'GAME_OVER':
                    if event.key == pygame.K_RETURN:
                        manager.reset_game()
                        player_stack.clear_stack()

        # ---- 2. LOGIKA UPDATE ----
        # Update timer state machine
        manager.update_timer(delta_time)
        
        # Sinkronisasi pergerakan monster murni hanya di fase PLAY
        if manager.current_state == 'PLAY':
            monster.update(manager.state_timer, manager.play_duration)
        elif manager.current_state == 'MEMORIZE':
            monster.current_x = monster.start_x  # Monster mundur saat menghafal

        # ---- 3. RENDER VISUAL (FONDASI) ----
        # UX Teori Warna: Merah jika kritis di fase PLAY
        if manager.current_state == 'PLAY' and manager.state_timer < 15000:
            screen.fill(COLOR_BG_DANGER)
        else:
            screen.fill(COLOR_BG_SAFE)
            
        # Gambar Monster dan Stack
        monster.draw(screen)
        
        # Render objek berdasarkan State
        if manager.current_state == 'MEMORIZE':
            # Gambar Menara Target untuk dihafal pemain
            tower_renderer.draw_player_tower(screen, manager.target_blueprint)
            state_text = "FASE HAFALAN! INGAT URUTAN BLOK..."
        elif manager.current_state == 'PLAY':
            # Gambar Menara buatan pemain
            tower_renderer.draw_player_tower(screen, player_stack.items)
            state_text = f"FASE EKSEKUSI! SUSUN SEKARANG..."
        else:
            state_text = "SISTEM HANCUR. TEKAN ENTER UNTUK BANGKIT."
        
        # Render Teks Informasi Kendali Utama (UI Dasar yang sudah di-upgrade)
        seconds = manager.state_timer // 1000
        ms = manager.state_timer % 1000
        
        # Teks baris pertama: Menampilkan Level, Skor Aktif, dan HIGH SCORE Abadi
        ui_string = f"LV: {manager.level} | SCORE: {manager.score} | HIGH SCORE: {manager.high_score}"
        ui_text = game_font.render(ui_string, True, COLOR_WHITE)
        
        # Teks baris kedua: Menampilkan status waktu dan state permainan
        if manager.current_state == 'GAME_OVER':
            if manager.new_record_achieved:
                state_text = "LUAR BIASA! REKOR BARU TERCIPTA! Tekan ENTER..."
            else:
                state_text = "SISTEM HANCUR. Tekan ENTER untuk bangkit kembali..."
        else:
            time_string = f"TIME: {seconds:02d}:{ms:03d} | "
            if manager.current_state == 'MEMORIZE':
                state_text = time_string + "FASE HAFALAN! INGAT URUTAN..."
            else:
                state_text = time_string + "FASE EKSEKUSI! SUSUN STACK..."

        info_text = game_font.render(state_text, True, COLOR_WHITE)
        
        screen.blit(ui_text, (20, 20))
        screen.blit(info_text, (20, 60))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()