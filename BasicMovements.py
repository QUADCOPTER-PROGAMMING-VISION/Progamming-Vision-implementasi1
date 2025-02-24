#ini yang dipakai

import cv2
from time import sleep

cap = cv2.VideoCapture(2)  # 0 untuk webcam utama, bisa diganti sesuai device ID DroidCam
while True:
    ret, frame = cap.read()
    # print("berhasil baca")
    if not ret:
        break
    cv2.imshow("DroidCam", frame)
    #simulasi sleep dari kode Tello
    print("Simulasi: maju selama 2 detik...")
    sleep(2)
    print("Simulasi: putar kanan selama 2 detik...")
    sleep(2)
    print("Simulasi: Berhenti...")
    # q buat keluar dari loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
