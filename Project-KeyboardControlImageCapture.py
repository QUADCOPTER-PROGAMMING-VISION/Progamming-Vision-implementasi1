import cv2
import KeyPressModule as kp
from time import sleep
import time

# Inisialisasi KeyPressModule
kp.init()

# Inisialisasi Kamera DroidCam
cap = cv2.VideoCapture(2)  # Sesuaikan dengan ID DroidCam

def getKeyboardInput():
    """Fungsi menangkap input keyboard untuk simulasi"""
    print("Checking keyboard input")  # Tambahkan ini
    lr, fb, ud, yv = 0,0,0,0
    speed = 50

    keys = ["LEFT", "RIGHT", "UP", "DOWN", "w", "s", "a", "d", "q", "e"]
    for key in keys:
        if kp.getKey(key):
            print(f"{key} key pressed")  # Debugging tombol yang ditekan
        elif kp.getKey('z'):
            cv2.imwrite(f'Resources/Images/{time.time()}.jpg', img)
            time.sleep(0.3)
    return [lr, fb, ud, yv]

while True:
    # Menangkap input keyboard tanpa mengontrol drone
    vals = getKeyboardInput()
    sleep(0.05)
    ret, img = cap.read()
    if not ret:
        break
    img = cv2.resize(img, (640, 480))
    cv2.imshow("DroidCam", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Tekan 'q' untuk keluar
        break

cap.release()
cv2.destroyAllWindows()
