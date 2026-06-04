import os

class ScoreManager:
    def __init__(self, filename="highscore.txt"):
        self.filename = filename
        # Mengambil skor tertinggi yang tersimpan saat objek diinisialisasi
        self.high_score = self.load_high_score()

    def load_high_score(self):
        """Membaca data dari file lokal. Jika file belum ada, sistem membuat baru dengan skor 0."""
        if not os.path.exists(self.filename):
            self.save_high_score(0)
            return 0
        
        try:
            with open(self.filename, "r") as file:
                content = file.read().strip()
                return int(content) if content.isdigit() else 0
        except IOError:
            print("[PERINGATAN] Gagal membaca file High Score. Menggunakan nilai default 0.")
            return 0

    def save_high_score(self, score):
        """Menulis skor tertinggi baru ke dalam file lokal secara permanen."""
        try:
            with open(self.filename, "w") as file:
                file.write(str(score))
            print(f"[REKOR] File lokal diperbarui. Skor Tertinggi Baru: {score}")
        except IOError:
            print("[EROR] Gagal menulis data skor ke penyimpanan lokal.")

    def update_high_score(self, current_score):
        """Memvalidasi apakah skor pemain saat ini berhasil memecahkan rekor tertinggi."""
        if current_score > self.high_score:
            self.high_score = current_score
            self.save_high_score(self.high_score)
            return True # Mengembalikan True jika terjadi pemecahan rekor
        return False