import pygame
import random
import os
pygame.init()
pygame.mixer.init()
LEBAR_LAYAR = 400
TINGGI_LAYAR = 600
layar = pygame.display.set_mode((LEBAR_LAYAR, TINGGI_LAYAR), pygame.RESIZABLE)
pygame.display.set_caption('Flappy Bird')
FPS = 60
GRAVITASI = 0.5
TINGGI_LOMPATAN = -8
CELAH_PIPA = 150
LEBAR_PIPA = 80
KECEPATAN_PIPA = 3
FREKUENSI_PIPA = 1500
FILE_SKOR_TERTINGGI = "skor_tertinggi.txt"
PUTIH = (255, 255, 255)
HITAM = (0, 0, 0)
HIJAU = (0, 255, 0)
suara_lompatan = pygame.mixer.Sound('jump.wav')
class Burung:
    def __init__(self):
        self.gambar = pygame.image.load('burung_fixPY.JPG').convert_alpha()  
        self.ukuran = 45 
        self.gambar = pygame.transform.scale(self.gambar, (self.ukuran, self.ukuran))
        self.rect = self.gambar.get_rect()
        self.rect.center = (LEBAR_LAYAR // 4, TINGGI_LAYAR // 2)
        self.kecepatan = 0
    def update(self):
        self.kecepatan += GRAVITASI
        self.rect.y += int(self.kecepatan)
    def lompat(self):
        self.kecepatan = TINGGI_LOMPATAN
    def gambar_burung(self):
        layar.blit(self.gambar, self.rect.topleft)
class Pipa:
    def __init__(self, x, y, is_atas):
        self.lebar = LEBAR_PIPA
        self.tinggi = TINGGI_LAYAR
        self.gambar = pygame.Surface((self.lebar, self.tinggi))
        self.gambar.fill(HIJAU)
        self.rect = self.gambar.get_rect()
        if is_atas:
            self.rect.bottomleft = (x, y)
        else:
            self.rect.topleft = (x, y)
    def update(self):
        self.rect.x -= KECEPATAN_PIPA
    def gambar_pipa(self):
        layar.blit(self.gambar, self.rect.topleft)
def baca_skor_tertinggi():
    if os.path.exists(FILE_SKOR_TERTINGGI):
        with open(FILE_SKOR_TERTINGGI, 'r') as file:
            try:
                return int(file.read())
            except ValueError:
                return 0
    return 0
def tulis_skor_tertinggi(skor):
    with open(FILE_SKOR_TERTINGGI, 'w') as file:
        file.write(str(skor))
def gambar_teks_tengah(teks, font, warna, x_pos=None, y_offset=0):
    permukaan_teks = font.render(teks, True, warna)
    rect_teks = permukaan_teks.get_rect(center=(x_pos if x_pos is not None else LEBAR_LAYAR // 2, TINGGI_LAYAR //  2 + y_offset))
    return permukaan_teks, rect_teks
def reset_skor_tertinggi():
    tulis_skor_tertinggi(0)
def utama():
    global LEBAR_LAYAR, TINGGI_LAYAR, layar
    jam = pygame.time.Clock()
    burung = Burung()
    pipa_pipa = []
    skor = 0
    berjalan = False
    pipa_terakhir = pygame.time.get_ticks()
    skor_tertinggi = baca_skor_tertinggi()
    INFO_PIPA = [
        ["ID Pipa", "Posisi X", "Posisi Y", "Pipa Atas"],
        [1, 400, random.randint(100, 300), True],
        [2, 400, random.randint(100, 300) + CELAH_PIPA, False]
    ]
    def buat_pipa():
        nonlocal skor, skor_tertinggi
        tinggi_pipa = random.randint(100, 300)
        pipa_pipa.append(Pipa(LEBAR_LAYAR, tinggi_pipa, True))
        pipa_pipa.append(Pipa(LEBAR_LAYAR, tinggi_pipa + CELAH_PIPA, False))
        id_pipa = len(INFO_PIPA)
        INFO_PIPA.append([id_pipa, LEBAR_LAYAR, tinggi_pipa, True])
        INFO_PIPA.append([id_pipa + 1, LEBAR_LAYAR, tinggi_pipa + CELAH_PIPA, False])
    def menu_utama():
        nonlocal berjalan
        while not berjalan:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        berjalan = True
                        return
            layar.fill(PUTIH)
            font = pygame.font.Font(None, 36)
            teks_judul, rect_judul = gambar_teks_tengah('Welcome to Flappy Bird Game', font, HITAM, x_pos=LEBAR_LAYAR // 2 + 470, y_offset=50)
            layar.blit(teks_judul, rect_judul)
            teks_instruksi, rect_instruksi = gambar_teks_tengah('Tekan Enter untuk Memulai',  font, HITAM, x_pos=LEBAR_LAYAR // 2 + 470, y_offset=80)
            layar.blit(teks_instruksi, rect_instruksi)
            pygame.display.flip()
            jam.tick(FPS)
    menu_utama()
    INFO_PERMAINAN = {
        'skor': skor,
        'skor_tertinggi': skor_tertinggi
    }
    while berjalan:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                berjalan = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    burung.lompat()
                    suara_lompatan.play()  
                if event.key == pygame.K_r:
                    reset_skor_tertinggi()
                    skor_tertinggi = 0
            if event.type == pygame.VIDEORESIZE:
                lebar_layar_baru, tinggi_layar_baru = event.w, event.h
                layar = pygame.display.set_mode((lebar_layar_baru, tinggi_layar_baru), pygame.RESIZABLE)
                burung.ubah_ukuran(lebar_layar_baru, tinggi_layar_baru)
                LEBAR_LAYAR, TINGGI_LAYAR = lebar_layar_baru, tinggi_layar_baru
                for pipa in pipa_pipa:
                    pipa.ubah_ukuran(lebar_layar_baru, tinggi_layar_baru)
        if not berjalan:
            break
        burung.update()
        waktu_sekarang = pygame.time.get_ticks()
        if waktu_sekarang - pipa_terakhir > FREKUENSI_PIPA:
            buat_pipa()
            pipa_terakhir = waktu_sekarang
        for pipa in pipa_pipa[:]:
            pipa.update()
            if pipa.rect.right < 0:
                pipa_pipa.remove(pipa)
                skor += 0.5
        layar.fill(PUTIH)
        burung.gambar_burung()
        for pipa in pipa_pipa:
            pipa.gambar_pipa()
        INFO_PERMAINAN['skor'] = skor
        if skor > INFO_PERMAINAN['skor_tertinggi']:
            INFO_PERMAINAN['skor_tertinggi'] = skor
        font = pygame.font.Font(None, 36)
        teks_skor = font.render(f'Skor: {int(INFO_PERMAINAN["skor"])}', True, HITAM)
        layar.blit(teks_skor, (10, 10))
        teks_skor_tertinggi = font.render(f'Skor Tertinggi: {int(INFO_PERMAINAN["skor_tertinggi"])}', True, HITAM)
        layar.blit(teks_skor_tertinggi, (10, 50))
        pygame.display.flip()
        jam.tick(FPS)
        if burung.rect.top < 0 or burung.rect.bottom > TINGGI_LAYAR or any(pipa.rect.colliderect(burung.rect) for pipa in pipa_pipa):
            berjalan = False
    if skor > skor_tertinggi:
        skor_tertinggi = int(skor)
        tulis_skor_tertinggi(skor_tertinggi)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    utama()
                    return
                if event.key == pygame.K_r:
                    reset_skor_tertinggi()
                    skor_tertinggi = 0
        layar.fill(PUTIH)
        teks_game_over, rect_game_over = gambar_teks_tengah(f'Permainan Selesai! Skormu: {int(skor)}', font, HITAM, x_pos=LEBAR_LAYAR // 2 + 465)
        layar.blit(teks_game_over, rect_game_over)
        teks_enter, rect_enter = gambar_teks_tengah('Tekan Enter untuk Mulai Ulang atau Tutup Jendela untuk Keluar', font, HITAM, x_pos=LEBAR_LAYAR // 2 + 470, y_offset=50)
        layar.blit(teks_enter, rect_enter)
        teks_reset, rect_reset = gambar_teks_tengah('Tekan R untuk Mereset Skor Tertinggi', font, HITAM, x_pos=LEBAR_LAYAR // 2 + 470, y_offset=80)
        layar.blit(teks_reset, rect_reset)
        pygame.display.flip()
if __name__ == '__main__':
    utama()
