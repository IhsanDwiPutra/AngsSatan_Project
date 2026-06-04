class AbyssalStack:
    def __init__(self, target_blueprint):
        # Ini adalah Tumpukan Pemain (Stack utama kita)
        self.items = []
        
        # Ini adalah Array Target yang harus disamai oleh pemain
        self.target_blueprint = target_blueprint

    def is_empty(self):
        """Memeriksa apakah tumpukan pemain kosong."""
        return len(self.items) == 0

    def push(self, color_block):
        """
        Operasi LIFO: Memasukkan blok warna ke posisi paling atas (akhir list).
        Kompleksitas Waktu: O(1)
        """
        self.items.append(color_block)
        print(f"[AKSI PUSH] Blok {color_block} ditambahkan. Tumpukan saat ini: {self.items}")

    def pop(self):
        """
        Operasi LIFO: Menghancurkan blok dari posisi paling atas.
        Pemain harus menggunakan ini jika salah memasukkan warna.
        Kompleksitas Waktu: O(1)
        """
        if not self.is_empty():
            removed_block = self.items.pop()
            print(f"[AKSI POP] Blok {removed_block} dihancurkan. Tumpukan saat ini: {self.items}")
            return removed_block
        else:
            print("[PERINGATAN] Tumpukan sudah kosong! Tidak ada yang bisa di-Pop.")
            return None

    def peek(self):
        """Melihat blok paling atas tanpa menghancurkannya."""
        if not self.is_empty():
            return self.items[-1]
        return None

    def check_match(self):
        """
        Validasi Akhir: Membandingkan Tumpukan Pemain dengan Array Target.
        Mengembalikan True jika menang, False jika masih salah atau belum selesai.
        """
        is_identical = self.items == self.target_blueprint
        if is_identical:
            print(f"[VALIDASI] TRUE! Tumpukan {self.items} sempurna sesuai cetak biru.")
        else:
            print(f"[VALIDASI] FALSE. Tumpukan belum sesuai dengan cetak biru {self.target_blueprint}.")
        return is_identical

    def clear_stack(self):
        """Mengosongkan tumpukan untuk level selanjutnya."""
        self.items = []
        
# ==========================================
# UJI COBA LOGIKA (Hanya dieksekusi jika file ini dijalankan langsung)
# ==========================================
if __name__ == "__main__":
    print("=== MEMULAI SIMULASI ABYSSAL STACK ===")
    
    # Target dari Sistem (Misal: Level 1)
    target_level_1 = ["Merah", "Biru", "Kuning"]
    
    # Inisialisasi Stack
    game_stack = AbyssalStack(target_level_1)
    
    # Simulasi Pemain Memasukkan Blok
    game_stack.push("Merah")
    game_stack.push("Hijau") # Ups! Pemain salah input
    game_stack.check_match() # Pasti False
    
    # Simulasi Pemain Panik dan Melakukan Pop
    game_stack.pop() # Hijau hancur
    
    # Pemain melanjutkan dengan benar
    game_stack.push("Biru")
    game_stack.push("Kuning")
    
    # Validasi Akhir
    game_stack.check_match() # Pasti True