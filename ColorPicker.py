import cv2
import numpy as np

# Gunakan kamera dari DroidCam
cap = cv2.VideoCapture(2)  # Sesuaikan dengan ID DroidCam

frameWidth = 480
frameHeight = 360

# Fungsi kosong untuk trackbar
def empty(a):
    pass

# Membuat jendela untuk HSV
cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640, 240)

cv2.createTrackbar("HUE Min", "HSV", 0, 179, empty)
cv2.createTrackbar("HUE Max", "HSV", 179, 179, empty)
cv2.createTrackbar("SAT Min", "HSV", 0, 255, empty)
cv2.createTrackbar("SAT Max", "HSV", 255, 255, empty)
cv2.createTrackbar("VALUE Min", "HSV", 0, 255, empty)
cv2.createTrackbar("VALUE Max", "HSV", 255, 255, empty)

while True:
    ret, img = cap.read()
    if not ret:
        print("Gagal menangkap gambar dari kamera!")
        break

    img = cv2.resize(img, (frameWidth, frameHeight))
    img = cv2.flip(img, 0)  # Membalik gambar jika diperlukan

    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Ambil nilai dari trackbar
    h_min = cv2.getTrackbarPos("HUE Min", "HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
    v_max = cv2.getTrackbarPos("VALUE Max", "HSV")

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    mask = cv2.inRange(imgHsv, lower, upper)
    result = cv2.bitwise_and(img, img, mask=mask)

    print(f'[{h_min},{s_min},{v_min},{h_max},{s_max},{v_max}]')

    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    hStack = np.hstack([img, mask, result])

    cv2.imshow('Horizontal Stacking', hStack)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Keluar dari program...")
        break

cap.release()
cv2.destroyAllWindows()
