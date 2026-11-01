import os
import random
import sys

# Pilihan simbol yang tersedia: B = Batu, G = Gunting, K = Kertas
CHOICES = {
    "B": "Batu",
    "G": "Gunting",
    "K": "Kertas"
}

# Pesan hasil untuk setiap kemungkinan outcome
RESULT_MESSAGES = {
    "win": "Kamu menang!",
    "lose": "Kamu kalah.",
    "draw": "Seri."
}

# Aturan permainan: setiap kunci mengalahkan nilai di list-nya
RULES = {
    "B": ["G"],  # Batu mengalahkan Gunting
    "G": ["K"],  # Gunting mengalahkan Kertas
    "K": ["B"]   # Kertas mengalahkan Batu
}


def clear_screen():
    # Bersihkan layar terminal agar tampilan lebih rapi
    # Gunakan "cls" di Windows, "clear" di Unix-like
    if sys.platform.startswith("win"):
        _ = os.system("cls")
    else:
        _ = os.system("clear")


def get_player_choice():
    # Loop meminta input pemain sampai masukan valid atau pemain memilih keluar
    while True:
        choice = input("Pilih [B]atu, [G]unting, [K]ertas, atau [Q] untuk keluar: ").strip().upper()
        # Jika pemain ingin keluar dari permainan
        if choice == "Q":
            return None
        # Jika pilihan valid (B/G/K) kembalikan choice
        if choice in CHOICES:
            return choice
        # Kalau masukan tidak valid, beri tahu dan ulangi
        print("Masukan tidak valid. Silakan pilih B, G, K, atau Q.")


def get_computer_choice():
    # Pilihan komputer diambil acak dari kunci CHOICES
    return random.choice(list(CHOICES.keys()))


def determine_result(player, computer):
    # Tentukan hasil: seri, menang, atau kalah
    if player == computer:
        return "draw"
    # Jika pilihan komputer ada di daftar yang dikalahkan pemain -> pemain menang
    if computer in RULES[player]:
        return "win"
    # Selain itu, pemain kalah
    return "lose"


def format_choice(label, key):
    # Boleh dipakai untuk menampilkan label yang lebih lengkap (tidak digunakan saat ini)
    return f"{label} ({CHOICES[key]})"


def show_intro():
    # Teks pembuka / judul permainan
    print("===================================")
    print("    Batu Gunting Kertas v1.0")
    print("===================================")
    print("Aturan:")
    print("- Batu mengalahkan Gunting")
    print("- Gunting mengalahkan Kertas")
    print("- Kertas mengalahkan Batu")
    print()


def show_stats(stats):
    # Menampilkan statistik singkat: menang, kalah, seri, dan total
    print()
    print("Statistik Permainan")
    print("--------------------")
    print(f"Menang : {stats['win']}")
    print(f"Kalah  : {stats['lose']}")
    print(f"Seri   : {stats['draw']}")
    print(f"Total  : {stats['total']}")
    print("--------------------")
    print()


def main():
    # Inisialisasi statistik permainan
    stats = {"win": 0, "lose": 0, "draw": 0, "total": 0}

    # Bersihkan layar dan tampilkan judul
    clear_screen()
    show_intro()

    # Loop utama permainan: minta input pemain, pilih komputer, tentukan hasil
    while True:
        player_choice = get_player_choice()
        # Jika pemain memilih keluar (Q), hentikan permainan
        if player_choice is None:
            print("Terima kasih telah bermain. Sampai jumpa!")
            break

        # Pilihan komputer dan hasil ronde
        computer_choice = get_computer_choice()
        result = determine_result(player_choice, computer_choice)

        # Update statistik sesuai hasil
        stats[result] += 1
        stats["total"] += 1

        # Tampilkan pilihan dan hasil untuk ronde ini
        print()
        print(f"Kamu memilih: {CHOICES[player_choice]}")
        print(f"Komputer memilih: {CHOICES[computer_choice]}")
        print(RESULT_MESSAGES[result])
        print()

        # Tampilkan statistik terkini
        show_stats(stats)

        # Tanyakan apakah pemain ingin main lagi
        answer = input("Main lagi? (Y/N): ").strip().upper()
        if answer != "Y":
            print("Terima kasih telah bermain.")
            break
        print()


if __name__ == "__main__":
    main()
