"""
Nama program : vigenerecipher.py
Nama         : Nailatus Sahlah
NPM          : 140810240021
Tanggal      : 22 September 2026
Deskripsi    : Program Vigenere Cipher untuk enkripsi dan dekripsi
               dengan bahasa python
"""

def enkripsi(plaintext, key):
    hasil = ""

    for i in range(len(plaintext)):
        p = ord(plaintext[i].upper()) - 65
        k = ord(key[i % len(key)].upper()) - 65

        c = (p + k) % 26
        hasil += chr(c + 65)

    return hasil


def dekripsi(ciphertext, key):
    hasil = ""

    for i in range(len(ciphertext)):
        c = ord(ciphertext[i].upper()) - 65
        k = ord(key[i % len(key)].upper()) - 65

        p = (c - k) % 26
        hasil += chr(p + 65)

    return hasil


def main():
    plaintext = input("Masukkan plaintext : ")
    key = input("Masukkan key       : ")

    plaintext = plaintext.replace(" ", "")
    key = key.replace(" ", "")

    ciphertext = enkripsi(plaintext, key)
    hasil_dekripsi = dekripsi(ciphertext, key)

    print("\n=== HASIL ===")
    print("Plaintext          :", plaintext.upper())
    print("Key                :", key.upper())
    print("Ciphertext         :", ciphertext)
    print("Hasil Dekripsi     :", hasil_dekripsi)


main()