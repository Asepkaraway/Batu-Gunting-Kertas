import pygame  # Pygame: library untuk membuat jendela, menangani event/input, dan menggambar grafik (digunakan untuk GUI game)
import random  # Modul random: digunakan untuk memilih pilihan komputer secara acak
import sys     # Modul sys: menyediakan akses ke fungsi/variabel interpreter (mis. sys.exit() untuk keluar aplikasi)

# Versi GUI dari Batu Gunting Kertas menggunakan Pygame
# File ini mandiri (tidak mengimpor `main.py`) sehingga mudah dijalankan.

# Pilihan simbol: B = Batu, G = Gunting, K = Kertas
CHOICES = {"B": "Batu", "G": "Gunting", "K": "Kertas"}

# Pesan hasil yang akan ditampilkan pada layar
RESULT_MESSAGES = {"win": "Kamu menang!", "lose": "Kamu kalah.", "draw": "Seri."}

# Aturan kemenangan: kunci mengalahkan daftar pilihan di value-nya
RULES = {"B": ["G"], "G": ["K"], "K": ["B"]}


def determine_result(player, computer):
    """
    Tentukan hasil ronde.
    - player: pilihan pemain ('B','G','K')
    - computer: pilihan komputer ('B','G','K')
    Mengembalikan: 'win', 'lose', atau 'draw'
    """
    if player == computer:
        return "draw"
    if computer in RULES[player]:
        return "win"
    return "lose"


# Warna yang digunakan pada antarmuka (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK = (30, 30, 30)
ACCENT = (70, 130, 180)  # warna aksen untuk hover / sukses


# Ukuran window GUI
WIDTH, HEIGHT = 600, 420


def run_gui():
    """
    Fungsi utama yang menjalankan loop Pygame.
    - Inisialisasi Pygame dan window
    - Menyiapkan tombol pilihan
    - Menangani input mouse/keyboard
    - Menggambar ulang tampilan setiap frame
    """
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Batu Gunting Kertas - GUI")
    clock = pygame.time.Clock()

    # Font: judul, teks utama, dan teks kecil
    font_title = pygame.font.SysFont(None, 40)
    font_text = pygame.font.SysFont(None, 28)
    font_small = pygame.font.SysFont(None, 20)

    # Definisi tombol: ukuran, jarak, dan posisi pusat
    btn_w, btn_h = 140, 64
    spacing = 30
    total_w = 3 * btn_w + 2 * spacing
    start_x = (WIDTH - total_w) // 2
    y_btn = 160

    # Buat daftar tombol sebagai tuple: (rect, label, key)
    buttons = []
    keys = ["B", "G", "K"]
    labels = ["Batu", "Gunting", "Kertas"]
    for i, key in enumerate(keys):
        rect = pygame.Rect(start_x + i * (btn_w + spacing), y_btn, btn_w, btn_h)
        buttons.append((rect, labels[i], key))

    # Statistik permainan (menang/kalah/seri/total)
    stats = {"win": 0, "lose": 0, "draw": 0, "total": 0}
    last_player = None
    last_computer = None
    last_result = None

    running = True
    while running:
        # Posisi mouse saat ini dan flag klik
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = False

        # Event handling: keluar, klik mouse, atau tekan tombol Q/Escape
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pressed = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    running = False

        # Jika ada klik, periksa tombol mana yang diklik
        if mouse_pressed:
            for rect, label, key in buttons:
                if rect.collidepoint(mouse_pos):
                    # Pilihan pemain berdasarkan tombol
                    player_choice = key
                    # Pilihan komputer acak
                    computer_choice = random.choice(list(CHOICES.keys()))
                    # Hitung hasil ronde
                    result = determine_result(player_choice, computer_choice)

                    # Update statistik sesuai hasil
                    stats[result] += 1
                    stats["total"] += 1

                    # Simpan hasil terakhir untuk ditampilkan
                    last_player = player_choice
                    last_computer = computer_choice
                    last_result = result

        # ---------- Rendering UI ----------
        screen.fill(DARK)  # background

        # Judul permainan
        title_surf = font_title.render("Batu Gunting Kertas", True, WHITE)
        screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 28))

        # Instruksi singkat
        instr = font_small.render("Klik tombol untuk memilih. Tekan Q atau ESC untuk keluar.", True, GRAY)
        screen.blit(instr, (WIDTH // 2 - instr.get_width() // 2, 76))

        # Gambar tombol dengan efek hover (ubah warna saat kursor di atas)
        for rect, label, key in buttons:
            if rect.collidepoint(mouse_pos):
                color = ACCENT
                txt_color = WHITE
            else:
                color = GRAY
                txt_color = BLACK
            pygame.draw.rect(screen, color, rect, border_radius=10)
            txt = font_text.render(label, True, txt_color)
            screen.blit(txt, (rect.x + rect.width // 2 - txt.get_width() // 2, rect.y + rect.height // 2 - txt.get_height() // 2))

        # Tampilkan hasil ronde terakhir (pilihan pemain, komputer, dan teks hasil)
        info_y = y_btn + btn_h + 30
        if last_result is not None:
            player_txt = font_text.render(f"Kamu: {CHOICES[last_player]}", True, WHITE)
            comp_txt = font_text.render(f"Komputer: {CHOICES[last_computer]}", True, WHITE)
            res_txt = font_text.render(RESULT_MESSAGES[last_result], True, ACCENT if last_result == "win" else (255, 100, 100) if last_result == "lose" else WHITE)

            screen.blit(player_txt, (WIDTH // 2 - player_txt.get_width() - 10, info_y))
            screen.blit(comp_txt, (WIDTH // 2 + 10, info_y))
            screen.blit(res_txt, (WIDTH // 2 - res_txt.get_width() // 2, info_y + 36))
        else:
            hint = font_text.render("Ayo mulai: pilih salah satu tombol di atas.", True, GRAY)
            screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, info_y))

        # Kotak statistik di pojok kanan atas
        stats_box = pygame.Rect(WIDTH - 190, 20, 170, 110)
        pygame.draw.rect(screen, (20, 20, 20), stats_box, border_radius=8)
        pygame.draw.rect(screen, (60, 60, 60), stats_box, width=2, border_radius=8)
        s1 = font_small.render(f"Menang: {stats['win']}", True, WHITE)
        s2 = font_small.render(f"Kalah : {stats['lose']}", True, WHITE)
        s3 = font_small.render(f"Seri  : {stats['draw']}", True, WHITE)
        s4 = font_small.render(f"Total : {stats['total']}", True, WHITE)
        screen.blit(s1, (stats_box.x + 12, stats_box.y + 12))
        screen.blit(s2, (stats_box.x + 12, stats_box.y + 36))
        screen.blit(s3, (stats_box.x + 12, stats_box.y + 60))
        screen.blit(s4, (stats_box.x + 12, stats_box.y + 84))

        # Update layar dan batasi frame rate
        pygame.display.flip()
        clock.tick(60)

    # Bersihkan dan keluar saat loop berakhir
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    run_gui()
