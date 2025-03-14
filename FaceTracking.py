import cv2
import numpy as np
import time

# Inisialisasi Kamera DroidCam
cap = cv2.VideoCapture(2)  # Sesuaikan dengan ID DroidCam

w, h = 560, 800
fbRange = [6200, 6800]
pid = [0.4, 0.4, 0]
pError = 0

def trackFace(info, w, pid, pError):
    """Menghitung pergerakan berdasarkan posisi wajah"""
    area = info[1]
    x, y = info[0]
    fb = 0

    error = x - w // 2
    speed = pid[0] * error + pid[1] * (error - pError)
    speed = int(np.clip(speed, -100, 100))

    if area > fbRange[0] and area < fbRange[1]:
        fb = 0
    elif area > fbRange[1]:
        fb = -20
    elif area < fbRange[0] and area != 0:
        fb = 20

    if x == 0:
        speed = 0
        error = 0

    # 🔥 Tambahkan print untuk debugging
    print(f"Rotasi: {speed}, Maju/Mundur: {fb}")

    return error


def findFace(img):
    """Deteksi wajah dalam frame menggunakan OpenCV"""
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)

    myFaceListC = []
    myFaceListArea = []

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

        cx = x + w // 2
        cy = y + h // 2
        area = w * h

        cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)

        myFaceListC.append([cx, cy])
        myFaceListArea.append(area)

    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        return img, [[0, 0], 0]


while True:
    ret, img = cap.read()
    if not ret:
        print("Gagal menangkap gambar dari kamera!")
        break

    img = cv2.resize(img, (w, h))
    img, info = findFace(img)

    # 🔥 Tambahkan pemanggilan trackFace()
    pError = trackFace(info, w, pid, pError)

    cv2.imshow("Output", img)

    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Keluar dari program...")
        break

cap.release()
cv2.destroyAllWindows()
