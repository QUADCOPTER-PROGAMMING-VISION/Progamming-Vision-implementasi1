import cv2
import KeyPressModule as kp
from time import sleep
import time
import os

# Buat folder jika belum ada
folder_path = "Resources/Images"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Inisialisasi KeyPressModule
kp.init()

# Inisialisasi Kamera DroidCam
cap = cv2.VideoCapture(2)  # Sesuaikan dengan ID DroidCam

def getKeyboardInput(img):
    """Fungsi menangkap input keyboard untuk simulasi dan menyimpan gambar"""
    print("Checking keyboard input")  # Debugging
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50

    keys = ["LEFT", "RIGHT", "UP", "DOWN", "w", "s", "a", "d", "q", "e", "z"]
    for key in keys:
        if kp.getKey(key):
            print(f"{key} key pressed")  # Debugging tombol yang ditekan

    # Jika tombol 'z' ditekan, simpan gambar
    if kp.getKey('z'):
        filename = os.path.join(folder_path, f"{time.time()}.jpg")
        success = cv2.imwrite(filename, img)
        if success:
            print(f"Gambar disimpan: {filename}")
        else:
            print("Gagal menyimpan gambar!")
        time.sleep(0.3)

    return [lr, fb, ud, yv]

while True:
    ret, img = cap.read()
    if not ret:
        print("Gagal menangkap gambar dari kamera!")
        break

    img = cv2.resize(img, (640, 480))
    cv2.imshow("DroidCam", img)

    # Menangkap input keyboard tanpa mengontrol drone
    vals = getKeyboardInput(img)
    sleep(0.05)

    # Cek jika tombol 'q' ditekan di Pygame atau OpenCV
    if kp.getKey('q') or cv2.waitKey(1) & 0xFF == ord('q'):
        print("Keluar dari program...")
        break

cap.release()
cv2.destroyAllWindows()
