"""
Nama program : lsb_steg.py
Nama         : Nailatus Sahlah
NPM          : 140810240021
Tanggal      : 6 Oktober 2026
Deskripsi    : Program python encode dan decode esan rahasia berupa teks 
               ke dalam file gambar menggunakan metode steganografi LSB
"""

from PIL import Image

def encode():
    path = input("Masukkan nama gambar asli: ")
    image = Image.open(path).convert("RGB")

    message = input("Masukkan pesan rahasia: ")
    binary = ''.join(format(ord(c), '08b') for c in message)
    binary += '00000000'

    pixels = list(image.getdata())
    capacity = len(pixels) * 3

    if len(binary) > capacity:
        print("Pesan terlalu panjang untuk gambar!")
        return

    result = []
    index = 0

    for pixel in pixels:
        new_pixel = []

        for value in pixel:
            if index < len(binary):
                value = (value & 254) | int(binary[index])
                index += 1
            new_pixel.append(value)

        result.append(tuple(new_pixel))

    output = Image.new("RGB", image.size)
    output.putdata(result)
    output.save("hasil_encode.png")

    print("Pesan berhasil disisipkan!")
    print("Hasil disimpan sebagai hasil_encode.png")


def decode():
    path = input("Masukkan nama gambar hasil encode: ")
    image = Image.open(path).convert("RGB")

    binary = ""

    for pixel in image.getdata():
        for value in pixel:
            binary += str(value & 1)

    message = ""

    for i in range(0, len(binary) - 7, 8):
        byte = binary[i:i + 8]

        if byte == "00000000":
            break

        message += chr(int(byte, 2))

    print("Pesan rahasia:", message)


while True:
    print("\n=== STEGANOGRAPHY LSB ===")
    print("1. Encode")
    print("2. Decode")
    print("3. Keluar")

    pilihan = input("Pilih menu: ")

    if pilihan == "1":
        encode()
    elif pilihan == "2":
        decode()
    elif pilihan == "3":
        print("Program selesai.")
        break
    else:
        print("Pilihan tidak valid!")
