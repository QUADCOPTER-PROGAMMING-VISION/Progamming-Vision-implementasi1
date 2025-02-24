import numpy as np
import cv2

# Gunakan kamera DroidCam
cap = cv2.VideoCapture(2)  # Sesuaikan dengan ID DroidCam

hsvVals = [0, 0, 188, 179, 33, 245]
sensors = 3
threshold = 0.2
width, height = 480, 360
senstivity = 3  # Jika angka tinggi, maka lebih sedikit sensitif
weights = [-25, -15, 0, 15, 25]
fSpeed = 15
curve = 0

def thresholding(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([hsvVals[0], hsvVals[1], hsvVals[2]])
    upper = np.array([hsvVals[3], hsvVals[4], hsvVals[5]])
    mask = cv2.inRange(hsv, lower, upper)
    return mask

def getContours(imgThres, img):
    """Mendeteksi objek berdasarkan thresholding"""
    cx = 0
    contours, hierarchy = cv2.findContours(imgThres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if len(contours) != 0:
        biggest = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(biggest)
        cx = x + w // 2
        cy = y + h // 2
        cv2.drawContours(img, biggest, -1, (255, 0, 255), 7)
        cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

    return cx

def getSensorOutput(imgThres, sensors):
    """Membagi gambar menjadi beberapa sensor dan mengecek apakah ada objek"""
    imgs = np.hsplit(imgThres, sensors)
    totalPixels = (imgThres.shape[1] // sensors) * imgThres.shape[0]
    senOut = []

    for x, im in enumerate(imgs):
        pixelCount = cv2.countNonZero(im)
        if pixelCount > threshold * totalPixels:
            senOut.append(1)
        else:
            senOut.append(0)

    return senOut

def sendCommands(senOut, cx):
    """Menentukan gerakan berdasarkan sensor (tanpa mengontrol drone)"""
    global curve

    # Perhitungan pergerakan kiri/kanan berdasarkan pusat objek
    lr = (cx - width // 2) // senstivity
    lr = int(np.clip(lr, -10, 10))

    if 2 > lr > -2:
        lr = 0

    # Logika pergerakan berdasarkan sensor
    if senOut == [1, 0, 0]:
        curve = weights[0]
    elif senOut == [1, 1, 0]:
        curve = weights[1]
    elif senOut == [0, 1, 0]:
        curve = weights[2]
    elif senOut == [0, 1, 1]:
        curve = weights[3]
    elif senOut == [0, 0, 1]:
        curve = weights[4]
    elif senOut == [0, 0, 0] or senOut == [1, 1, 1] or senOut == [1, 0, 1]:
        curve = weights[2]

    # 🔥 Cetak perintah ke terminal, bukan kirim ke drone
    print(f"Left/Right: {lr}, Speed: {fSpeed}, Curve: {curve}")

while True:
    ret, img = cap.read()
    if not ret:
        print("Gagal menangkap gambar dari kamera!")
        break

    img = cv2.resize(img, (width, height))
    img = cv2.flip(img, 0)

    imgThres = thresholding(img)
    cx = getContours(imgThres, img)  # Untuk Translasi
    senOut = getSensorOutput(imgThres, sensors)  # Untuk Rotasi

    sendCommands(senOut, cx)

    cv2.imshow("Output", img)
    cv2.imshow("Path", imgThres)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Keluar dari program...")
        break

cap.release()
cv2.destroyAllWindows()
