"""
Nama program : hillcipher.py
Nama         : Nailatus Sahlah
NPM          : 140810240021
Tanggal      : 15 September 2026
Deskripsi    : Program Hill Cipher untuk enkripsi, dekripsi,
               dan mencari kunci dengan brute force.
"""
import string


MOD = 26
ALPHABET = string.ascii_uppercase




def bersihkan_teks(teks):
    return ''.join(ch for ch in teks.upper() if ch in ALPHABET)




def teks_ke_angka(teks):
    return [ALPHABET.index(ch) for ch in teks]




def angka_ke_teks(list_angka):
    return ''.join(ALPHABET[n % MOD] for n in list_angka)




def tambah_padding(teks, ukuran_blok, huruf_padding='X'):
    sisa = len(teks) % ukuran_blok
    if sisa != 0:
        teks += huruf_padding * (ukuran_blok - sisa)
    return teks




def kali_matriks(A, B, mod=MOD):
    baris_A, kolom_A = len(A), len(A[0])
    baris_B, kolom_B = len(B), len(B[0])


    if kolom_A != baris_B:
        raise ValueError("Ukuran matriks tidak cocok untuk perkalian")


    hasil = [[0] * kolom_B for _ in range(baris_A)]


    for i in range(baris_A):
        for j in range(kolom_B):
            total = 0


            for k in range(kolom_A):
                total += A[i][k] * B[k][j]


            hasil[i][j] = total % mod


    return hasil




def ambil_minor(matriks, i, j):
    return [
        baris[:j] + baris[j + 1:]
        for idx, baris in enumerate(matriks)
        if idx != i
    ]




def hitung_determinan(matriks):
    n = len(matriks)


    if n == 1:
        return matriks[0][0]


    if n == 2:
        return matriks[0][0] * matriks[1][1] - matriks[0][1] * matriks[1][0]


    det = 0


    for j in range(n):
        minor = ambil_minor(matriks, 0, j)
        det += ((-1) ** j) * matriks[0][j] * hitung_determinan(minor)


    return det




def matriks_kofaktor(matriks):
    n = len(matriks)
    kofaktor = [[0] * n for _ in range(n)]


    for i in range(n):
        for j in range(n):
            minor = ambil_minor(matriks, i, j)
            kofaktor[i][j] = ((-1) ** (i + j)) * hitung_determinan(minor)


    return kofaktor




def transpos_matriks(matriks):
    return [list(baris) for baris in zip(*matriks)]




def gcd_diperluas(a, b):
    if b == 0:
        return a, 1, 0


    g, x1, y1 = gcd_diperluas(b, a % b)


    x = y1
    y = x1 - (a // b) * y1


    return g, x, y




def invers_modulo(a, mod=MOD):
    a = a % mod
    g, x, _ = gcd_diperluas(a, mod)


    if g != 1:
        return None


    return x % mod




def invers_matriks_modulo(matriks, mod=MOD):
    det = hitung_determinan(matriks) % mod
    det_invers = invers_modulo(det, mod)


    if det_invers is None:
        raise ValueError(
            f"Matriks tidak punya invers mod {mod} "
            f"(determinan = {det}, tidak koprima dengan {mod})"
        )


    kofaktor = matriks_kofaktor(matriks)
    adjugate = transpos_matriks(kofaktor)


    n = len(matriks)


    return [
        [(adjugate[i][j] * det_invers) % mod for j in range(n)]
        for i in range(n)
    ]




def enkripsi(plaintext, matriks_kunci):
    m = len(matriks_kunci)
    plaintext = tambah_padding(bersihkan_teks(plaintext), m)
    angka = teks_ke_angka(plaintext)


    hasil = []


    for i in range(0, len(angka), m):
        blok = [[angka[i + k]] for k in range(m)]
        blok_terenkripsi = kali_matriks(matriks_kunci, blok)
        hasil.extend(baris[0] for baris in blok_terenkripsi)


    return angka_ke_teks(hasil)




def dekripsi(ciphertext, matriks_kunci):
    m = len(matriks_kunci)
    ciphertext = bersihkan_teks(ciphertext)
    kunci_invers = invers_matriks_modulo(matriks_kunci)
    angka = teks_ke_angka(ciphertext)


    hasil = []


    for i in range(0, len(angka), m):
        blok = [[angka[i + k]] for k in range(m)]
        blok_terdekripsi = kali_matriks(kunci_invers, blok)
        hasil.extend(baris[0] for baris in blok_terdekripsi)


    return angka_ke_teks(hasil)




def cari_kunci(plaintext, ciphertext, m):
    plaintext = bersihkan_teks(plaintext)
    ciphertext = bersihkan_teks(ciphertext)


    if len(plaintext) < m * m or len(ciphertext) < m * m:
        raise ValueError(
            f"Butuh minimal {m * m} karakter plaintext dan ciphertext"
        )


    angka_plain = teks_ke_angka(plaintext[:m * m])
    angka_cipher = teks_ke_angka(ciphertext[:m * m])


    P = [
        [
            angka_plain[kolom * m + baris]
            for kolom in range(m)
        ]
        for baris in range(m)
    ]


    C = [
        [
            angka_cipher[kolom * m + baris]
            for kolom in range(m)
        ]
        for baris in range(m)
    ]


    P_invers = invers_matriks_modulo(P)


    return kali_matriks(C, P_invers)




def input_matriks_kunci(m):
    print(
        f"Masukkan matriks kunci berukuran {m}x{m} "
        f"(per baris, pisahkan dengan spasi):"
    )


    matriks = []


    for i in range(m):
        while True:
            try:
                baris = list(
                    map(int, input(f"Baris {i + 1}: ").split())
                )


                if len(baris) != m:
                    print(f"Baris harus berisi {m} angka!")
                    continue


                matriks.append(baris)
                break


            except ValueError:
                print("Input harus berupa angka, pisahkan dengan spasi!")


    return matriks




def tampilkan_matriks(matriks, nama="Matriks"):
    print(f"{nama}:")


    for baris in matriks:
        print(baris)




def menu_utama():
    while True:
        print("\n=== PROGRAM HILL CIPHER ===")
        print("1. Enkripsi")
        print("2. Dekripsi")
        print("3. Cari Kunci (Known-Plaintext Attack)")
        print("4. Keluar")


        pilihan = input("Pilih menu (1-4): ").strip()


        if pilihan == '1':
            teks = input("Masukkan plaintext: ")


            try:
                m = int(input("Ukuran matriks kunci (2/3/dst): "))
                kunci = input_matriks_kunci(m)
                hasil = enkripsi(teks, kunci)
                print(f"\nHasil Enkripsi: {hasil}")


            except Exception as e:
                print(f"Error: {e}")


        elif pilihan == '2':
            teks = input("Masukkan ciphertext: ")


            try:
                m = int(input("Ukuran matriks kunci (2/3/dst): "))
                kunci = input_matriks_kunci(m)
                hasil = dekripsi(teks, kunci)
                print(f"\nHasil Dekripsi: {hasil}")


            except Exception as e:
                print(f"Error: {e}")


        elif pilihan == '3':
            pt = input("Masukkan plaintext yang diketahui: ")
            ct = input("Masukkan ciphertext yang sesuai: ")


            try:
                m = int(input("Ukuran matriks kunci (2/3/dst): "))
                kunci = cari_kunci(pt, ct, m)
                tampilkan_matriks(kunci, "Kunci K yang ditemukan")


            except Exception as e:
                print(f"Error: {e}")


        elif pilihan == '4':
            print("Program selesai.")
            break


        else:
            print("Pilihan tidak valid!")




if __name__ == "__main__":
    menu_utama()