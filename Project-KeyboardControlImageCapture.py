import KeyPressModule as kp
import numpy as np
from time import sleep
import cv2
import math
import time

### PARAMETERS ###
fSpeed = 117 / 10  # Forward Speed in cm/s
aSpeed = 360 / 10  # Angular Speed Degrees/s
interval = 0.25

dInterval = fSpeed * interval
aInterval = aSpeed * interval

###############################################
x, y = 500, 500
a = 0
yaw = 0

kp.init()
points = [(x, y)]  # Mulai dari tengah canvas

# Inisialisasi Kamera DroidCam
cap = cv2.VideoCapture(2)  # Sesuaikan dengan ID DroidCam

def getKeyboardInput():
    """Fungsi menangkap input keyboard untuk simulasi"""
    print("Checking keyboard input")  # Debugging awal
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50
    global x, y, yaw, a  # Pastikan x dan y diperbarui dalam fungsi ini

    d = 0  # Jarak yang akan ditempuh

    # Daftar tombol yang ingin di-handle
    keys = ["LEFT", "RIGHT", "UP", "DOWN", "w", "s", "a", "d", "x", "e", "z"]

    for key in keys:
        if kp.getKey(key):
            if key == "LEFT":
                lr = -speed
                d = dInterval
                a = -180
                print("LEFT key pressed → Bergerak ke kiri")
            elif key == "RIGHT":
                lr = speed
                d = -dInterval
                a = 180
                print("RIGHT key pressed → Bergerak ke kanan")
            elif key == "UP":
                fb = speed
                d = dInterval
                a = 270
                print("UP key pressed → Maju")
            elif key == "DOWN":
                fb = -speed
                d = -dInterval
                a = -90
                print("DOWN key pressed → Mundur")
            elif key == "w":
                ud = speed
                print("W key pressed → Naik")
            elif key == "s":
                ud = -speed
                print("S key pressed → Turun")
            elif key == "a":
                yv = speed
                yaw -= aInterval
                print("A key pressed → Rotasi ke kiri")
            elif key == "d":
                yv = -speed
                yaw += aInterval
                print("D key pressed → Rotasi ke kanan")
            elif key == "x":
                print("X key pressed → Mendarat")
            elif key == "e":
                print("E key pressed → Lepas landas")
            elif key == "z":
                filename = f'Resources/Images/{time.time()}.jpg'
                cv2.imwrite(filename, None)  # Gantilah `None` dengan gambar dari kamera
                print(f"Z key pressed → Gambar disimpan: {filename}")

    sleep(interval)
    a += yaw  # Update sudut berdasarkan rotasi
    x += int(d * math.cos(math.radians(a)))  # Hitung perubahan posisi x
    y += int(d * math.sin(math.radians(a)))  # Hitung perubahan posisi y

    return [lr, fb, ud, yv, x, y]

def drawPoints(img, points):
    """Menggambar titik pergerakan di layar"""
    for point in points:
        cv2.circle(img, point, 5, (0, 0, 255), cv2.FILLED)

    cv2.circle(img, points[-1], 8, (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'({(points[-1][0] - 500) / 100},{(points[-1][1] - 500) / 100})m',
                (points[-1][0] + 10, points[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1,
                (255, 0, 255), 1)


while True:
    # Ambil gambar dari DroidCam
    ret, frame = cap.read()
    if not ret:
        print("Gagal menangkap gambar dari kamera!")
        break

    frame = cv2.resize(frame, (640, 480))
    cv2.imshow("DroidCam", frame)

    vals = getKeyboardInput()

    img = np.zeros((1000, 1000, 3), np.uint8)

    if points[-1][0] != vals[4] or points[-1][1] != vals[5]:
        points.append((vals[4], vals[5]))

    drawPoints(img, points)

    cv2.imshow("Output", img)

    # Tekan 'q' untuk keluar
    if kp.getKey("q") or cv2.waitKey(1) & 0xFF == ord("q"):
        print("Keluar dari program...")
        break

cap.release()
cv2.destroyAllWindows()
