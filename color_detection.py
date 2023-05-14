# ----------------Import Library---------------- #

import pandas as pd
import cv2
import os

# ----------------Judul Program---------------- #

print("\n===========================================\n")
print("PROGRAM KOMPRESI GAMBAR DAN DETEKSI WARNA")
print("\n===========================================\n")

# ----------------Inisiasi---------------- #

img_path = input("Masukkan nama file: ")
csv_path = 'colors.csv'

# ----------------Kompresi Gambar---------------- #

img = cv2.imread(img_path)

quality = 50

filename, ext = os.path.splitext(img_path)

new_filename = f'{filename}_compressed{ext}'

compressed_img = cv2.imwrite(
    new_filename, img, [int(cv2.IMWRITE_JPEG_QUALITY), quality])

size_before = os.path.getsize(img_path)

size_after = os.path.getsize(new_filename)

print(f"Ukuran file sebelum kompresi: {size_before} bytes")
print(f"Ukuran file setelah kompresi: {size_after} bytes")

# -------------------------------Color Detection------------------------------- #

index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
df = pd.read_csv(csv_path, names=index, header=None)

img = cv2.imread(img_path)
img = cv2.resize(img, (700, 700))

clicked = False
r = g = b = xpos = ypos = 0


def get_color_name(R, G, B):
    minimum = 1000
    for i in range(len(df)):
        d = abs(R - int(df.loc[i, 'R'])) + abs(G -
                                               int(df.loc[i, 'G'])) + abs(B - int(df.loc[i, 'B']))
        if d <= minimum:
            minimum = d
            cname = df.loc[i, 'color_name']

    return cname


def draw_function(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global clicked, r, g, b, xpos, ypos
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)


cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

while True:
    cv2.imshow('image', img)
    if clicked:
        cv2.rectangle(img, (20, 20), (600, 60), (b, g, r), -1)
        text = get_color_name(r, g, b) + ' R=' + str(r) + \
            ' G=' + str(g) + ' B=' + str(b)
        cv2.putText(img, text, (50, 50), 2, 0.8,
                    (255, 255, 255), 2, cv2.LINE_AA)
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

    if cv2.waitKey(20) & 0xFF == 27:
        break


cv2.destroyAllWindows()
